"""`voc build-db`: drop and recreate data/voc.sqlite from the files under data/ (DESIGN 4), then run trends."""
from __future__ import annotations

import json
import os
import sqlite3
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from voc.analytics.materialize import materialize
from voc.config import get_settings
from voc.paths import Paths, get_paths
from voc.schemas.call import CallRecord
from voc.store.db import compute_data_version, connect, create_schema, set_meta
from voc.taxonomy import loader as tx
from voc.theme.wordings import distinct_wordings, select_wordings

AS_OF_MIN_CALLS = 20
COUNTED_STATUSES = ("active", "catch_all")


class BuildRefused(RuntimeError):
    """The input files must not be indexed (e.g. fake extractions outside VOC_LLM=fake)."""


# --- file readers -------------------------------------------------------------------------

def read_jsonl(path: Path) -> Iterator[dict]:
    if not path.exists():
        return
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def load_calls(paths: Paths) -> list[CallRecord]:
    if not paths.calls.exists():
        raise BuildRefused(f"{paths.calls} not found; run `voc ingest sample` first")
    return [CallRecord.model_validate(r) for r in read_jsonl(paths.calls)]


def check_provenance(extractions: list[dict], llm_mode: str) -> None:
    n_fake = sum(1 for e in extractions if e.get("produced_by") == "fake")
    if n_fake and llm_mode != "fake":
        raise BuildRefused(f"{n_fake} extractions were produced by the fake client; set VOC_LLM=fake to index them")


def resolve_effective(themes: list[dict]) -> dict[str, str]:
    """theme_id -> effective theme id following merged_into chains (catch_all counts as active)."""
    parent = {t["theme_id"]: (t.get("merged_into") if t.get("status") == "merged" and t.get("merged_into") else None)
              for t in themes}

    def find(tid: str) -> str:
        seen: list[str] = []
        while parent.get(tid) and tid not in seen:
            seen.append(tid)
            tid = parent[tid]
        return tid

    return {tid: find(tid) for tid in parent}


# --- inserts ------------------------------------------------------------------------------

def _json(value: Any) -> str | None:
    return None if value is None else json.dumps(value, ensure_ascii=False)


def insert_calls(con: sqlite3.Connection, calls: list[CallRecord]) -> None:
    rows = [(c.call_id, c.source, c.shape, c.date, c.week, c.month, c.text, c.text_sha, c.product, c.product_raw,
             c.sub_product_raw, c.issue_raw, c.sub_issue_raw, c.region, c.region_group, c.channel, c.segment,
             c.company, c.sampling_fraction, c.n_turns, _json(c.customer_char_ranges), _json(c.meta)) for c in calls]
    con.executemany(f"INSERT INTO calls VALUES ({','.join('?' * 22)})", rows)


def insert_extractions(con: sqlite3.Connection, extractions: list[dict], call_ids: set[str]) -> dict[str, int]:
    ex_rows, reasons, products, services, topics, evidence, positives = [], [], [], [], [], [], []
    skipped = 0
    for e in extractions:
        cid = e.get("call_id")
        if cid not in call_ids:
            skipped += 1
            continue
        x = e.get("extraction") if e.get("status") == "ok" else None
        if not x:
            ex_rows.append((cid, e.get("status", "error"), e.get("produced_by"), e.get("model"), e.get("prompt_version"),
                            e.get("schema_version"), e.get("extracted_at"), None, None, None, None, None, None, None,
                            None, None, _json(e.get("flags") or []), _json({"error": e.get("error")})))
            continue
        ex_rows.append((cid, "ok", e.get("produced_by"), e.get("model"), e.get("prompt_version"), e.get("schema_version"),
                        e.get("extracted_at"), x.get("overall_sentiment"), x.get("resolution_status"), x.get("customer_ask"),
                        x.get("stated_reason"), x.get("underlying_driver"), int(bool(x.get("reason_differs"))),
                        int(bool(x.get("redaction_heavy"))), x.get("summary"), e.get("quote_verify_rate"),
                        _json(e.get("flags") or []), _json(x)))
        seen_reasons: set[str] = set()
        for r in x.get("contact_reasons") or []:
            if r["reason"] not in seen_reasons:
                seen_reasons.add(r["reason"])
                reasons.append((cid, r["reason"], r.get("specific_reason"), int(bool(r.get("is_primary")))))
        products += [(cid, p) for p in dict.fromkeys(x.get("products") or [])]
        services += [(cid, s) for s in dict.fromkeys(x.get("services") or [])]
        for idx, t in enumerate(x.get("topics") or []):
            tid = f"{cid}:{idx}"
            ev = t.get("evidence") or []
            ok = t.get("evidence_ok")
            if ok is None:
                ok = any(q.get("verified") for q in ev)
            topics.append((tid, cid, idx, t.get("topic_label"), t["issue_statement"], t["product"], int(t["sentiment"]),
                           t["driver_category"], t.get("driver"), t.get("outcome"), int(bool(ok))))
            for k, q in enumerate(ev):
                evidence.append((f"{tid}:{k}", tid, cid, q["quote"], q.get("char_start"), q.get("char_end"),
                                 q.get("speaker"), int(bool(q.get("verified"))), q.get("match_kind")))
        for k, p in enumerate(x.get("positive_moments") or []):
            positives.append((f"{cid}:pm{k}", cid, p.get("what"), p.get("category"), p.get("quote"), p.get("char_start"),
                              p.get("char_end"), p.get("speaker"), int(bool(p.get("verified")))))
    con.executemany(f"INSERT INTO extractions VALUES ({','.join('?' * 18)})", ex_rows)
    con.executemany("INSERT INTO call_reasons VALUES (?,?,?,?)", reasons)
    con.executemany("INSERT INTO call_products VALUES (?,?)", products)
    con.executemany("INSERT INTO call_services VALUES (?,?)", services)
    con.executemany("INSERT INTO topics VALUES (?,?,?,?,?,?,?,?,?,?,?)", topics)
    con.executemany("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?)", evidence)
    con.executemany("INSERT INTO positive_moments VALUES (?,?,?,?,?,?,?,?,?)", positives)
    return {"n_extracted": sum(1 for r in ex_rows if r[1] == "ok"), "n_error": sum(1 for r in ex_rows if r[1] != "ok"),
            "n_topics": len(topics), "n_evidence": len(evidence), "skipped": skipped}


def insert_themes(con: sqlite3.Connection, paths: Paths) -> dict[str, int]:
    registry = read_json(paths.registry, {"themes": []})
    themes = registry.get("themes") or []
    effective = resolve_effective(themes)
    con.executemany(f"INSERT INTO themes VALUES ({','.join('?' * 17)})", [
        (t["theme_id"], t["name"], t.get("problem_statement"), t.get("root_cause"), t.get("polarity", "negative"),
         t.get("driver_category"), t.get("bucket"), t.get("status", "active"), t.get("merged_into"),
         effective[t["theme_id"]], t.get("created_pass"), t.get("codebook_version", 1), 0, 0, 0, None,
         t.get("grouping_quality", "ok")) for t in themes])
    merges = read_json(paths.merges, {"merges": []}).get("merges") or []
    con.executemany("INSERT OR REPLACE INTO theme_merges VALUES (?,?,?,?,?,?)", [
        (m["from_theme"], m["into_theme"], m.get("pass"), m.get("reason"), m.get("judged_by"), m.get("created_at"))
        for m in merges])
    topic_ids = {r[0] for r in con.execute("SELECT topic_id FROM topics")}
    members, unknown, orphan = [], 0, 0
    for m in read_jsonl(paths.members):
        if m["topic_id"] not in topic_ids:
            orphan += 1
            continue
        if m["theme_id"] not in effective:
            unknown += 1
        members.append((m["topic_id"], m["theme_id"], effective.get(m["theme_id"], m["theme_id"]), m.get("confidence"),
                        m.get("pass"), m.get("batch_id")))
    con.executemany("INSERT OR REPLACE INTO theme_members VALUES (?,?,?,?,?,?)", members)
    if orphan or unknown:
        print(f"warning: {orphan} members without a topic, {unknown} members with an unknown theme")
    return {"n_themes": len(themes), "n_members": len(members),
            "n_active": sum(1 for t in themes if t.get("status", "active") in COUNTED_STATUSES)}


def insert_wordings(con: sqlite3.Connection) -> int:
    """theme_wordings via the maximal-diversity selection, plus n_calls/n_wordings/n_products/first_seen_week."""
    by_theme: dict[str, list[dict]] = {}
    for r in con.execute(
            "SELECT tm.effective_theme_id AS theme_id, t.topic_id, t.call_id, t.issue_statement, c.product, c.date, c.week "
            "FROM theme_members tm JOIN topics t ON t.topic_id = tm.topic_id JOIN calls c ON c.call_id = t.call_id"):
        by_theme.setdefault(r["theme_id"], []).append(dict(r))
    rows, stats = [], []
    for theme_id, cands in by_theme.items():
        for rank, w in enumerate(select_wordings(cands)):
            rows.append((theme_id, rank, w["topic_id"], w["call_id"], w["issue_statement"], w["product"], w["date"]))
        stats.append((len({c["call_id"] for c in cands}), len(distinct_wordings(cands)),
                      len({c["product"] for c in cands}), min(c["week"] for c in cands), theme_id))
    con.executemany("INSERT INTO theme_wordings VALUES (?,?,?,?,?,?,?)", rows)
    con.executemany("UPDATE themes SET n_calls = ?, n_wordings = ?, n_products = ?, first_seen_week = ? WHERE theme_id = ?", stats)
    return len(rows)


def insert_totals(con: sqlite3.Connection, calls: list[CallRecord], profile: dict) -> None:
    population = profile.get("population_by_month") or {}
    for kind in ("week", "month"):
        counts: dict[str, int] = {}
        for c in calls:
            counts[getattr(c, kind)] = counts.get(getattr(c, kind), 0) + 1
        con.executemany("INSERT INTO period_totals VALUES (?,?,?,?)", [
            (kind, p, n, population.get(p) if kind == "month" else None) for p, n in counts.items()])
    for dim in ("product", "channel", "region_group", "region", "segment", "company", "month", "week"):
        counts = {}
        for c in calls:
            counts[getattr(c, dim)] = counts.get(getattr(c, dim), 0) + 1
        con.executemany("INSERT INTO dim_totals VALUES (?,?,?)", [(dim, v, n) for v, n in counts.items()])


def insert_fts(con: sqlite3.Connection) -> None:
    con.execute("INSERT INTO calls_fts(rowid, text) SELECT rowid, text FROM calls")
    con.execute("INSERT INTO topics_fts(rowid, issue_statement, topic_label, driver) "
                "SELECT rowid, issue_statement, topic_label, driver FROM topics")


# --- meta ---------------------------------------------------------------------------------

def compute_as_of_week(con: sqlite3.Connection, min_calls: int = AS_OF_MIN_CALLS) -> str | None:
    """Latest complete ISO week with >= min_calls calls.

    A corpus that ends mid-week leaves a partial last week; using it as the as-of point would put a
    half-empty week inside the four-week recent window and understate every emerging signal."""
    last = con.execute("SELECT MAX(date) AS d FROM calls").fetchone()
    last_date = date.fromisoformat(last["d"]) if last and last["d"] else None
    rows = con.execute("SELECT period, n_calls FROM period_totals WHERE period_kind = 'week' "
                       "ORDER BY period DESC").fetchall()
    fallback = rows[0]["period"] if rows else None
    for row in rows:
        if row["n_calls"] < min_calls:
            continue
        if last_date is not None:
            year, week = row["period"].split("-W")
            week_end = date.fromisocalendar(int(year), int(week), 7)
            if week_end > last_date:      # the corpus stops inside this week
                continue
        return row["period"]
    return fallback


def qa_invariants(con: sqlite3.Connection) -> dict[str, Any]:
    """Free QA metrics (DESIGN 5.7) over the ok extractions."""
    n_ok = con.execute("SELECT COUNT(*) FROM extractions WHERE status = 'ok'").fetchone()[0]
    if not n_ok:
        return {}
    agree = tested = other = 0
    for r in con.execute("SELECT r.reason, c.issue_raw, c.sub_issue_raw FROM call_reasons r JOIN calls c ON c.call_id = r.call_id "
                         "WHERE r.is_primary = 1"):
        other += r["reason"] == "other_or_unclear"
        expected = tx.map_issue_to_reasons(r["issue_raw"], r["sub_issue_raw"])
        if expected:
            tested += 1
            agree += r["reason"] in expected
    prod_agree = con.execute("SELECT COUNT(*) FROM calls c WHERE EXISTS (SELECT 1 FROM call_products p "
                             "WHERE p.call_id = c.call_id AND p.product = c.product)").fetchone()[0]
    n_ev, n_ver = con.execute("SELECT COUNT(*), COALESCE(SUM(verified), 0) FROM evidence").fetchone()
    n_topics = con.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
    hist = {str(r[0]): r[1] for r in con.execute(
        "SELECT overall_sentiment, COUNT(*) FROM extractions WHERE status = 'ok' GROUP BY overall_sentiment")}
    n_neg = sum(n for s, n in hist.items() if int(s) <= -1)
    n_red = con.execute("SELECT COUNT(*) FROM extractions WHERE status = 'ok' AND redaction_heavy = 1").fetchone()[0]
    return {
        "qa_reason_agreement": round(agree / tested, 4) if tested else None, "qa_reason_agreement_n": tested,
        "qa_product_agreement": round(prod_agree / n_ok, 4), "qa_other_share": round(other / n_ok, 4),
        "qa_quote_verify_rate": round(n_ver / n_ev, 4) if n_ev else None, "qa_topics_per_call": round(n_topics / n_ok, 3),
        "qa_sentiment_hist": hist, "qa_negative_share": round(n_neg / n_ok, 4), "qa_redaction_heavy_share": round(n_red / n_ok, 4),
    }


def write_meta_json(paths: Paths, meta: dict[str, Any]) -> None:
    tmp = paths.meta.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, paths.meta)


# --- entry point ---------------------------------------------------------------------------

def _remove_db_files(path: Path) -> None:
    for p in (path, Path(str(path) + "-wal"), Path(str(path) + "-shm")):
        if p.exists():
            p.unlink()


def build(paths: Paths | None = None, run_trends: bool = True, quiet: bool = False) -> dict[str, Any]:
    """Rebuild the index from the files. Returns the meta dict that was stored."""
    t0 = time.perf_counter()
    settings = get_settings()
    paths = paths or get_paths()
    calls = load_calls(paths)
    extractions = list(read_jsonl(paths.extractions))
    check_provenance(extractions, settings.llm_mode)
    profile = read_json(paths.profile, {})

    tmp_db = paths.sqlite.with_name(paths.sqlite.name + ".tmp")
    _remove_db_files(tmp_db)
    con = connect(tmp_db)
    try:
        create_schema(con)
        insert_calls(con, calls)
        ex = insert_extractions(con, extractions, {c.call_id for c in calls})
        th = insert_themes(con, paths)
        n_wordings = insert_wordings(con)
        insert_totals(con, calls, profile)
        insert_fts(con)
        con.commit()
        if not quiet:
            print(f"build-db: {len(calls)} calls, {ex['n_extracted']} extractions ok ({ex['n_error']} errors), "
                  f"{ex['n_topics']} topics, {th['n_themes']} themes ({th['n_active']} counted), {n_wordings} wordings")
        if run_trends:
            materialize(con, quiet=quiet)
        meta: dict[str, Any] = {
            "data_version": compute_data_version(paths), "as_of_week": compute_as_of_week(con),
            "llm_mode": settings.llm_mode, "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "n_calls": len(calls), "n_extracted": ex["n_extracted"], "n_errors": ex["n_error"],
            "n_topics": ex["n_topics"], "n_themes": th["n_active"], "n_members": th["n_members"],
            "company": settings.company, "taxonomy_version": tx.version(),
            "extraction_prompt_version": next((e.get("prompt_version") for e in extractions if e.get("prompt_version")), None),
            "theme_prompt_version": read_json(paths.registry, {}).get("theme_prompt_version"),
            "sampling_fraction": profile.get("sampling_fraction"), "source": profile.get("source"),
        }
        meta.update(qa_invariants(con))
        for key, value in meta.items():
            set_meta(con, key, value)
        con.commit()
        con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    finally:
        con.close()
    _remove_db_files(paths.sqlite)
    os.replace(tmp_db, paths.sqlite)
    _remove_db_files(Path(str(tmp_db)))  # leftover -wal/-shm of the tmp file, if any
    write_meta_json(paths, meta)
    if not quiet:
        print(f"build-db: {paths.sqlite} ready in {time.perf_counter() - t0:.2f}s "
              f"(data_version {meta['data_version']}, as_of {meta['as_of_week']}, llm_mode {meta['llm_mode']})")
    return meta
