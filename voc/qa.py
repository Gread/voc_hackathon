"""`voc qa`: extraction quality metrics. The free metrics come from the index (agreement with the
customers' own complaint category, quote verification, abstention share); the golden metrics come from
a hand-reviewed sample when one exists."""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path
from typing import Any

from voc.paths import get_paths
from voc.store.db import connect, set_meta
from voc.taxonomy import loader as tx

GOLDEN_SIZE = 40


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("qa", help="Extraction quality: free metrics and the golden-set review")
    sub = p.add_subparsers(dest="qa_cmd")
    r = sub.add_parser("report", help="print the metrics and store them in meta (default)")
    r.set_defaults(func=report)
    e = sub.add_parser("export-golden", help="write a stratified review sample")
    e.add_argument("--n", type=int, default=GOLDEN_SIZE)
    e.add_argument("--seed", type=int, default=7)
    e.set_defaults(func=export_golden)
    s = sub.add_parser("score-golden", help="score a completed review CSV")
    s.set_defaults(func=score_golden)
    p.set_defaults(func=report)


def free_metrics(con) -> dict[str, Any]:
    """Metrics that need no human review: agreement with the complaint form, coverage, verification."""
    rows = con.execute("""
        SELECT c.call_id, c.product, c.issue_raw, c.sub_issue_raw,
               (SELECT r.reason FROM call_reasons r WHERE r.call_id = c.call_id AND r.is_primary = 1) AS primary_reason,
               (SELECT COUNT(*) FROM call_products p WHERE p.call_id = c.call_id AND p.product = c.product) AS product_hit,
               (SELECT COUNT(*) FROM topics t WHERE t.call_id = c.call_id) AS n_topics,
               e.overall_sentiment, e.redaction_heavy, e.quote_verify_rate
        FROM calls c JOIN extractions e ON e.call_id = c.call_id WHERE e.status = 'ok'""").fetchall()
    if not rows:
        return {}
    reason_hits = reason_total = 0
    product_hits = 0
    other = 0
    topics = 0
    sentiments: dict[int, int] = {}
    verify: list[float] = []
    redacted = 0
    for r in rows:
        mapped = tx.map_issue_to_reasons(r["issue_raw"], r["sub_issue_raw"])
        if mapped:
            reason_total += 1
            reason_hits += int(r["primary_reason"] in mapped)
        product_hits += int(bool(r["product_hit"]))
        other += int(r["primary_reason"] == "other_or_unclear")
        topics += r["n_topics"] or 0
        s = r["overall_sentiment"]
        if s is not None:
            sentiments[int(s)] = sentiments.get(int(s), 0) + 1
        if r["quote_verify_rate"] is not None:
            verify.append(float(r["quote_verify_rate"]))
        redacted += int(bool(r["redaction_heavy"]))
    n = len(rows)
    ev = con.execute("SELECT COUNT(*) AS n, SUM(verified) AS v FROM evidence").fetchone()
    return {
        "n_extracted": n,
        "reason_agreement": round(reason_hits / reason_total, 3) if reason_total else None,
        "reason_agreement_base": reason_total,
        "product_agreement": round(product_hits / n, 3),
        "other_or_unclear_share": round(other / n, 3),
        "topics_per_call": round(topics / n, 2),
        "sentiment_histogram": {str(k): sentiments[k] for k in sorted(sentiments)},
        "negative_share": round(sum(v for k, v in sentiments.items() if k < 0) / n, 3),
        "quote_verify_rate": round((ev["v"] or 0) / ev["n"], 4) if ev and ev["n"] else None,
        "per_call_quote_verify_rate": round(sum(verify) / len(verify), 3) if verify else None,
        "redaction_heavy_share": round(redacted / n, 3),
    }


def report(args: argparse.Namespace) -> int:
    paths = get_paths()
    if not paths.sqlite.exists():
        print("no index found: run `voc build-db` first", file=sys.stderr)
        return 2
    con = connect(paths.sqlite)
    metrics = free_metrics(con)
    if not metrics:
        print("no successful extractions in the index", file=sys.stderr)
        return 1
    golden = score_file(paths.golden / "golden_review.csv")
    if golden:
        metrics.update({f"golden_{k}": v for k, v in golden.items()})
    for key, value in metrics.items():
        set_meta(con, f"qa_{key}", value)
    con.commit()
    width = max(len(k) for k in metrics)
    print("extraction quality")
    for key, value in metrics.items():
        print(f"  {key:<{width}}  {value}")
    expect = []
    if metrics.get("reason_agreement") is not None and not 0.55 <= metrics["reason_agreement"] <= 0.95:
        expect.append(f"reason agreement {metrics['reason_agreement']} is outside the expected 0.55-0.95")
    if metrics.get("other_or_unclear_share", 0) > 0.15:
        expect.append(f"abstention share {metrics['other_or_unclear_share']} is high (> 0.15)")
    if metrics.get("quote_verify_rate") is not None and metrics["quote_verify_rate"] < 0.9:
        expect.append(f"quote verification {metrics['quote_verify_rate']} is low (< 0.90)")
    if not 1.2 <= metrics.get("topics_per_call", 0) <= 3.5:
        expect.append(f"topics per call {metrics['topics_per_call']} is outside the expected 1.2-3.5")
    for line in expect:
        print(f"  ! {line}")
    return 0


def export_golden(args: argparse.Namespace) -> int:
    """Stratified sample by product and month for two reviewers."""
    paths = get_paths().ensure()
    con = connect(paths.sqlite)
    rows = con.execute("""
        SELECT c.call_id, c.month, c.product, c.text, e.json
        FROM calls c JOIN extractions e ON e.call_id = c.call_id WHERE e.status = 'ok'""").fetchall()
    if not rows:
        print("no extractions to review", file=sys.stderr)
        return 1
    strata: dict[tuple[str, str], list[Any]] = {}
    for r in rows:
        strata.setdefault((r["product"], r["month"]), []).append(r)
    rng = random.Random(args.seed)
    picked: list[Any] = []
    keys = sorted(strata)
    while len(picked) < min(args.n, len(rows)) and keys:
        for key in list(keys):
            bucket = strata[key]
            if not bucket:
                keys.remove(key)
                continue
            picked.append(bucket.pop(rng.randrange(len(bucket))))
            if len(picked) >= args.n:
                break
    out = paths.golden / "extraction_golden.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in picked:
            f.write(json.dumps({"call_id": r["call_id"], "month": r["month"], "product": r["product"],
                                "text": r["text"], "extraction": json.loads(r["json"])}, ensure_ascii=False) + "\n")
    csv_path = paths.golden / "golden_review.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["call_id", "reviewer", "primary_reason_verdict", "products_verdict", "sentiment_delta",
                    "driver_faithful", "quote_verbatim", "notes"])
        for r in picked:
            w.writerow([r["call_id"], "", "", "", "", "", "", ""])
    print(f"wrote {len(picked)} records to {out}\nreview template: {csv_path}\n"
          f"verdicts: primary_reason_verdict = correct|partial|wrong; products_verdict = correct|partial|wrong; "
          f"sentiment_delta = integer; driver_faithful = y|n; quote_verbatim = y|n")
    return 0


def score_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("primary_reason_verdict") or "").strip()]
    if not rows:
        return {}
    n = len(rows)
    correct = sum(1 for r in rows if r["primary_reason_verdict"].strip() == "correct")
    partial = sum(1 for r in rows if r["primary_reason_verdict"].strip() == "partial")
    prod = sum(1 for r in rows if (r.get("products_verdict") or "").strip() == "correct")
    deltas = [abs(int(r["sentiment_delta"])) for r in rows if (r.get("sentiment_delta") or "").strip().lstrip("-").isdigit()]
    driver = sum(1 for r in rows if (r.get("driver_faithful") or "").strip().lower() == "y")
    quote = sum(1 for r in rows if (r.get("quote_verbatim") or "").strip().lower() == "y")
    return {"n_reviewed": n, "primary_accuracy": round(correct / n, 3),
            "primary_accuracy_lenient": round((correct + partial) / n, 3),
            "product_accuracy": round(prod / n, 3),
            "sentiment_mae": round(sum(deltas) / len(deltas), 2) if deltas else None,
            "sentiment_within_1": round(sum(1 for d in deltas if d <= 1) / len(deltas), 3) if deltas else None,
            "driver_faithful": round(driver / n, 3), "quote_verbatim": round(quote / n, 3)}


def score_golden(args: argparse.Namespace) -> int:
    metrics = score_file(get_paths().golden / "golden_review.csv")
    if not metrics:
        print("no completed reviews found in data/golden/golden_review.csv", file=sys.stderr)
        return 1
    print(json.dumps(metrics, indent=1))
    return 0
