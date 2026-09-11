"""`voc trends`: materialise entity_period, entity_dim and emerging_scores from the SQLite index.

Entity types: theme (effective, active + catch_all), reason, driver_category, customer_ask. A call counts once per
entity; its sentiment for the entity is the strongest of its relevant topics (min for negative mass, max for
positive mass). Everything here is plain Python over dict rows so the same functions run on filtered row sets.
"""
from __future__ import annotations

import sqlite3
import time
from datetime import datetime, timezone
from typing import Iterable, Mapping

from voc.analytics import emerging as em
from voc.analytics import novelty
from voc.analytics.segments import breakdown
from voc.store.db import set_meta
from voc.taxonomy import loader as tx

ENTITY_TYPES = ("theme", "reason", "driver_category", "customer_ask")
DIMS = ("product", "channel", "region_group", "region", "segment", "company", "month")
FIRST_AS_OF_INDEX = 20          # scores start at the 21st week of the window
EntityKey = tuple[str, str]
CallSent = dict[str, tuple[int, int]]   # call_id -> (min_sentiment, max_sentiment)


# --- loading ------------------------------------------------------------------------------

def load_calls(con: sqlite3.Connection) -> dict[str, dict]:
    cols = ("call_id", "week", "month") + DIMS[:-1]
    sql = f"SELECT {', '.join(cols)} FROM calls"
    return {r["call_id"]: dict(r) for r in con.execute(sql)}


def _merge(target: dict[EntityKey, CallSent], key: EntityKey, call_id: str, s_min: int, s_max: int) -> None:
    calls = target.setdefault(key, {})
    cur = calls.get(call_id)
    calls[call_id] = (s_min, s_max) if cur is None else (min(cur[0], s_min), max(cur[1], s_max))


def load_entity_calls(con: sqlite3.Connection) -> dict[EntityKey, CallSent]:
    """Per entity, the calls that mention it with their strongest topic sentiment."""
    out: dict[EntityKey, CallSent] = {}
    for r in con.execute(
            "SELECT tm.effective_theme_id AS eid, t.call_id, t.sentiment FROM theme_members tm "
            "JOIN topics t ON t.topic_id = tm.topic_id JOIN themes th ON th.theme_id = tm.effective_theme_id "
            "WHERE th.status IN ('active', 'catch_all')"):
        _merge(out, ("theme", r["eid"]), r["call_id"], r["sentiment"], r["sentiment"])
    for r in con.execute("SELECT driver_category AS eid, call_id, sentiment FROM topics"):
        _merge(out, ("driver_category", r["eid"]), r["call_id"], r["sentiment"], r["sentiment"])
    call_sent = {r["call_id"]: (r["s_min"], r["s_max"]) for r in con.execute(
        "SELECT call_id, MIN(sentiment) AS s_min, MAX(sentiment) AS s_max FROM topics GROUP BY call_id")}
    for r in con.execute("SELECT call_id, reason AS eid FROM call_reasons"):
        s = call_sent.get(r["call_id"], (0, 0))
        _merge(out, ("reason", r["eid"]), r["call_id"], s[0], s[1])
    for r in con.execute("SELECT call_id, customer_ask AS eid FROM extractions WHERE status = 'ok' AND customer_ask IS NOT NULL"):
        s = call_sent.get(r["call_id"], (0, 0))
        _merge(out, ("customer_ask", r["eid"]), r["call_id"], s[0], s[1])
    return out


def load_polarities(con: sqlite3.Connection) -> dict[EntityKey, str]:
    pol = {("theme", r["theme_id"]): r["polarity"] for r in con.execute("SELECT theme_id, polarity FROM themes")}
    for code in tx.codes("driver_categories"):
        pol[("driver_category", code)] = tx.polarity_of_driver(code)
    return pol


# --- pure computations --------------------------------------------------------------------

def sentiment_stats(values: Iterable[tuple[int, int]], polarity: str) -> tuple[float, float, float | None]:
    """(neg_mass, pos_mass, mean_sentiment) over per-call (min, max) pairs."""
    neg = pos = total = 0.0
    n = 0
    for s_min, s_max in values:
        neg += max(0, -s_min)
        pos += max(0, s_max)
        total += s_max if polarity == "positive" else s_min
        n += 1
    return neg, pos, (total / n if n else None)


def period_rows(entity_calls: Mapping[EntityKey, CallSent], calls: Mapping[str, dict],
                polarities: Mapping[EntityKey, str], period_kind: str, totals: Mapping[str, int]) -> list[tuple]:
    rows: list[tuple] = []
    for (etype, eid), members in entity_calls.items():
        groups: dict[str, list[tuple[int, int]]] = {}
        for call_id, sent in members.items():
            call = calls.get(call_id)
            if call is not None:
                groups.setdefault(call[period_kind], []).append(sent)
        polarity = polarities.get((etype, eid), "negative")
        for period, sents in groups.items():
            total = totals.get(period, 0)
            neg, pos, mean = sentiment_stats(sents, polarity)
            rows.append((etype, eid, period_kind, period, len(sents), len(sents) / total if total else None, neg, pos, mean))
    return rows


def dim_rows(entity_calls: Mapping[EntityKey, CallSent], calls: Mapping[str, dict]) -> list[tuple]:
    rows: list[tuple] = []
    values_by_dim = {dim: {cid: str(c[dim]) for cid, c in calls.items()} for dim in DIMS}
    for (etype, eid), members in entity_calls.items():
        ids = set(members)
        for dim in DIMS:
            _, brk = breakdown(ids, values_by_dim[dim])
            for r in brk:
                rows.append((etype, eid, dim, r["value"], r["n_calls"], r["n_slice"], r["share"], r["ci_lo"],
                             r["ci_hi"], r["lift"], int(r["suppressed"])))
    return rows


def as_of_weeks(all_weeks: list[str], first_index: int = FIRST_AS_OF_INDEX) -> list[str]:
    return all_weeks[first_index:]


def emerging_rows(entity_calls: Mapping[EntityKey, CallSent], calls: Mapping[str, dict],
                  novel_by_entity: Mapping[EntityKey, frozenset[str]] | None = None,
                  token_index: Mapping[str, str] | None = None) -> list[tuple]:
    """Scores for every as-of week from the 21st week of the window to the last week with calls."""
    total_weekly = em.weekly_totals(c["week"] for c in calls.values())
    if not total_weekly:
        return []
    all_weeks = em.weeks_between(min(total_weekly), max(total_weekly))
    weekly: dict[EntityKey, dict[str, int]] = {}
    for key, members in entity_calls.items():
        weekly[key] = em.weekly_totals(calls[c]["week"] for c in members if c in calls)
    first_seen = {key: em.first_seen(w) for key, w in weekly.items()}
    rows: list[tuple] = []
    for as_of in as_of_weeks(all_weeks):
        window = set(em.recent_weeks(as_of) + em.baseline_weeks(as_of, em.RECENT_WEEKS_8W, em.BASELINE_WEEKS_8W))
        novel = novelty.novel_tokens(token_index, as_of) if token_index else set()
        for etype in ENTITY_TYPES:
            active = {eid: w for (t, eid), w in weekly.items()
                      if t == etype and any(w.get(wk, 0) for wk in window)}
            scores = em.score_entities(active, total_weekly, as_of, {eid: first_seen[(etype, eid)] for eid in active})
            for eid, s in scores.items():
                flag = 0
                if novel_by_entity and novel:
                    flag = int(bool(novel_by_entity.get((etype, eid), frozenset()) & novel))
                rows.append((etype, eid, as_of, s["n_recent"], s["expected_recent"], s["n_baseline"], s["z"],
                             s["ratio"], s["weeks_recent"], s["share_recent"], s["first_seen_week"], s["status"],
                             s["status_8w"], s["emerging_score"], flag, s["n_tested"], s["expected_false_positives"]))
    return rows


# --- novelty inputs -----------------------------------------------------------------------

def theme_wording_tokens(con: sqlite3.Connection) -> dict[EntityKey, frozenset[str]]:
    out: dict[str, set[str]] = {}
    for r in con.execute("SELECT theme_id, issue_statement FROM theme_wordings"):
        out.setdefault(r["theme_id"], set()).update(novelty.tokenize(r["issue_statement"]))
    return {("theme", k): frozenset(v) for k, v in out.items()}


def statement_token_index(con: sqlite3.Connection) -> dict[str, str]:
    rows = con.execute("SELECT c.week, t.issue_statement FROM topics t JOIN calls c ON c.call_id = t.call_id")
    return novelty.build_token_index((r["week"], r["issue_statement"]) for r in rows)


# --- entry point ---------------------------------------------------------------------------

def materialize(con: sqlite3.Connection, quiet: bool = False) -> dict[str, int]:
    """Recompute the three analytics tables in place and return row counts."""
    t0 = time.perf_counter()
    calls = load_calls(con)
    entity_calls = load_entity_calls(con)
    polarities = load_polarities(con)
    totals = {kind: {r["period"]: r["n_calls"] for r in con.execute(
        "SELECT period, n_calls FROM period_totals WHERE period_kind = ?", (kind,))} for kind in ("week", "month")}

    con.execute("DELETE FROM entity_period")
    con.execute("DELETE FROM entity_dim")
    con.execute("DELETE FROM emerging_scores")
    ep = period_rows(entity_calls, calls, polarities, "week", totals["week"]) + \
        period_rows(entity_calls, calls, polarities, "month", totals["month"])
    con.executemany("INSERT INTO entity_period VALUES (?,?,?,?,?,?,?,?,?)", ep)
    ed = dim_rows(entity_calls, calls)
    con.executemany("INSERT INTO entity_dim VALUES (?,?,?,?,?,?,?,?,?,?,?)", ed)
    es = emerging_rows(entity_calls, calls, theme_wording_tokens(con), statement_token_index(con))
    con.executemany("INSERT INTO emerging_scores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", es)
    set_meta(con, "trends_built_at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    con.commit()
    counts = {"entities": len(entity_calls), "entity_period": len(ep), "entity_dim": len(ed), "emerging_scores": len(es)}
    if not quiet:
        print(f"trends: {counts['entities']} entities -> entity_period {counts['entity_period']}, "
              f"entity_dim {counts['entity_dim']}, emerging_scores {counts['emerging_scores']} "
              f"({time.perf_counter() - t0:.2f}s)")
    return counts
