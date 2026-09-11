"""Data profile and the sampling gate (DESIGN §2.3, adapted to the single-bank CFPB corpus)."""
from __future__ import annotations

import calendar
import time
from collections import Counter
from typing import Any, Callable

import httpx

from voc.ingest.cfpb import PRODUCTS, fetch_aggregations, make_client, read_raw_window
from voc.ingest.normalize import month_range, read_json, write_json_atomic
from voc.ingest.sample import DEFAULT_MIN_WORDS, eligible_rows, implied_fraction
from voc.paths import Paths
from voc.schemas.call import iso_week
from voc.taxonomy.loader import map_product, map_region_group, map_segment

GATE = {"weekly_min": 30, "weekly_coverage": 0.90, "product_min": 300, "product_count": 2,
        "segment_min": 100, "segment_count": 2}


def _sampled(n: int, f: float) -> int:
    return round(n * f)


def counts_from_rows(rows: list[dict]) -> dict[str, dict[str, int]]:
    """Eligible counts by month, ISO week, product code, segment and region group."""
    keys = {
        "month": lambda p: p["_date"][:7],
        "week": lambda p: iso_week(p["_date"]),
        "product": lambda p: map_product(p.get("product"), p.get("sub_product")),
        "segment": lambda p: map_segment(p.get("tags")),
        "region_group": lambda p: map_region_group(p.get("state")),
        "channel": lambda p: (p.get("submitted_via") or "unknown"),
    }
    return {name: dict(sorted(Counter(fn(p) for p in rows).items())) for name, fn in keys.items()}


def evaluate_gate(counts: dict[str, dict[str, int]], fraction: float, months: list[str]) -> dict[str, Any]:
    weeks = counts["week"]
    weeks_ok = sum(1 for n in weeks.values() if _sampled(n, fraction) >= GATE["weekly_min"])
    coverage = weeks_ok / len(weeks) if weeks else 0.0
    products_ok = [k for k, n in counts["product"].items() if _sampled(n, fraction) >= GATE["product_min"]]
    segments_ok = [k for k, n in counts["segment"].items() if _sampled(n, fraction) >= GATE["segment_min"]]
    missing = [m for m in months if counts["month"].get(m, 0) == 0]
    checks = {
        "weekly_support": {"pass": coverage >= GATE["weekly_coverage"], "weeks_ok": weeks_ok,
                           "weeks_total": len(weeks), "coverage": round(coverage, 3)},
        "products": {"pass": len(products_ok) >= GATE["product_count"], "ok": products_ok},
        "segments": {"pass": len(segments_ok) >= GATE["segment_count"], "ok": segments_ok},
        "months_present": {"pass": not missing, "missing": missing},
    }
    return {"pass": all(c["pass"] for c in checks.values()), "thresholds": GATE, "checks": checks}


def profile_from_raw(raw: dict[str, list[dict]], months: list[str], target: int,
                     min_words: int) -> dict[str, Any]:
    rows = eligible_rows(raw, min_words)
    counts = counts_from_rows(rows)
    fraction = implied_fraction(target, len(rows))
    raw_by_month = {m: len(raw.get(m, [])) for m in months}
    return {
        "source": "cfpb_api_raw",
        "n_raw": sum(raw_by_month.values()),
        "n_eligible": len(rows),
        "min_words": min_words,
        "implied_fraction": fraction,
        "months": [{"month": m, "raw": raw_by_month[m], "eligible": counts["month"].get(m, 0),
                    "sampled_est": _sampled(counts["month"].get(m, 0), fraction)} for m in months],
        "counts": counts,
        "gate": evaluate_gate(counts, fraction, months),
    }


# --- API aggregation fallback (no raw files yet) ----------------------------------------

def _bucket_counts(aggs: dict, name: str) -> dict[str, int]:
    buckets = aggs.get(name, {}).get(name, {}).get("buckets", []) or aggs.get(name, {}).get("buckets", [])
    return {b["key"]: int(b["doc_count"]) for b in buckets}


def profile_from_api(client: httpx.Client, company: str, months: list[str], target: int,
                     *, sleep: Callable[[float], None] = time.sleep) -> dict[str, Any]:
    """Approximate profile from per-month aggregations; weeks are spread uniformly within the month."""
    month_n: dict[str, int] = {}
    totals: dict[str, Counter] = {"product": Counter(), "segment": Counter(), "region_group": Counter(),
                                  "channel": Counter()}
    for m in months:
        page = fetch_aggregations(client, company, PRODUCTS, m, sleep=sleep)
        total = page.get("hits", {}).get("total", 0)
        month_n[m] = int(total["value"] if isinstance(total, dict) else total)
        aggs = page.get("aggregations", {})
        for k, n in _bucket_counts(aggs, "product").items():
            totals["product"][map_product(k)] += n
        for k, n in _bucket_counts(aggs, "tags").items():
            totals["segment"][map_segment(k)] += n
        for k, n in _bucket_counts(aggs, "state").items():
            totals["region_group"][map_region_group(k)] += n
        for k, n in _bucket_counts(aggs, "submitted_via").items():
            totals["channel"][k] += n
        print(f"{m}  {month_n[m]:6d}  (aggregations)")
        sleep(1.0)
    weeks: Counter = Counter()
    for m, n in month_n.items():
        y, mo = (int(x) for x in m.split("-"))
        days = calendar.monthrange(y, mo)[1]
        for d in range(1, days + 1):
            weeks[iso_week(f"{m}-{d:02d}")] += n / days
    counts = {"month": month_n, "week": {k: round(v) for k, v in sorted(weeks.items())}}
    counts.update({k: dict(sorted(v.items())) for k, v in totals.items()})
    n_total = sum(month_n.values())
    fraction = implied_fraction(target, n_total)
    return {
        "source": "cfpb_api_aggregations",
        "n_raw": n_total, "n_eligible": n_total, "min_words": 0, "implied_fraction": fraction,
        "months": [{"month": m, "raw": n, "eligible": n, "sampled_est": _sampled(n, fraction)}
                   for m, n in month_n.items()],
        "counts": counts,
        "gate": evaluate_gate(counts, fraction, months),
        "note": "aggregation fallback: no dedupe/min-words; weekly counts are uniform-within-month estimates",
    }


def build_profile(paths: Paths, company: str, start: str, end: str, *, target: int,
                  min_words: int = DEFAULT_MIN_WORDS, client: httpx.Client | None = None) -> dict[str, Any]:
    months = month_range(start, end)
    raw = read_raw_window(paths, company, start, end)
    if raw:
        body = profile_from_raw(raw, months, target, min_words)
    else:
        print("no raw files found; falling back to API aggregations")
        own = client is None
        client = client or make_client()
        try:
            body = profile_from_api(client, company, months, target)
        finally:
            if own:
                client.close()
    profile = read_json(paths.profile, default={}) or {}
    profile.update({"company": company, "window": {"start": start, "end": end}, "target": target, **body})
    write_json_atomic(paths.profile, profile)
    return profile


# --- printing ---------------------------------------------------------------------------

def format_table(profile: dict[str, Any]) -> str:
    f = profile.get("implied_fraction", profile.get("sampling_fraction", 0.0))
    lines = [f"company: {profile.get('company')}   window: {profile.get('window', {}).get('start')}.."
             f"{profile.get('window', {}).get('end')}   source: {profile.get('source')}",
             f"raw {profile.get('n_raw')}   eligible {profile.get('n_eligible')}   target {profile.get('target')}"
             f"   implied f = {f:.4f}", "", f"{'month':8} {'raw':>7} {'eligible':>9} {'sampled~':>9}"]
    for row in profile.get("months", []):
        lines.append(f"{row['month']:8} {row['raw']:7d} {row['eligible']:9d} {row['sampled_est']:9d}")
    counts = profile.get("counts", {})
    for dim in ("product", "segment", "region_group", "channel"):
        items = sorted(counts.get(dim, {}).items(), key=lambda kv: -kv[1])
        lines.append("")
        lines.append(f"{dim}:")
        for k, n in items:
            lines.append(f"  {k:32} {n:7d}  ~{_sampled(n, f):5d} sampled")
    gate = profile.get("gate", {})
    lines.append("")
    lines.append(f"gate: {'PASS' if gate.get('pass') else 'FAIL'}")
    for name, check in gate.get("checks", {}).items():
        detail = {k: v for k, v in check.items() if k != "pass"}
        lines.append(f"  [{'ok' if check['pass'] else 'FAIL'}] {name}: {detail}")
    return "\n".join(lines)
