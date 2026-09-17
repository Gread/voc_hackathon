"""The weekly customer review: one week of contacts answered as four questions.

Assembled from the same queries the tools and the dashboard run, so every number here is one a
reader can open. The four sections are deliberately in the order a reader needs them:

  1. what changed          volume and mix against the week before and the four before that
  2. what drove feeling    the specific moments, in the customers' own words
  3. what needs attention  ranked by growth and by reported impact, not by volume alone
  4. what the calls say    verbatim, with distinct call counts and what the evidence cannot bear

Section 4 states the limits out loud because a weekly review is read quickly and acted on, which is
exactly when an unstated caveat does damage.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from voc.analytics.emerging import week_add
from voc.schemas.filters import Filters
from voc.store import queries as Q

RECENT_WEEKS = 4          # the comparison window behind the reviewed week
TOP_REASONS = 6
TOP_DRIVERS = 5
MAX_QUOTES = 6
NEW_THEME_LOOKBACK = 8    # a theme absent this many weeks before counts as new to the week


def _week_filters(base: Filters, week: str) -> Filters:
    """`base` narrowed to one ISO week."""
    monday = Q.week_monday(week)
    sunday = Q.week_sunday(week)
    return base.model_copy(update={"date_from": monday, "date_to": sunday})


def _range_filters(base: Filters, first_week: str, last_week: str) -> Filters:
    return base.model_copy(update={"date_from": Q.week_monday(first_week),
                                   "date_to": Q.week_sunday(last_week)})


def _delta(now: float | None, before: float | None) -> dict[str, Any]:
    """Change expressed both ways, with direction, or unknown when there is nothing to compare."""
    if now is None or before is None:
        return {"direction": "unknown", "points": None, "ratio": None}
    points = round(now - before, 1)
    ratio = round(now / before, 2) if before else None
    direction = "up" if points > 0.2 else "down" if points < -0.2 else "flat"
    return {"direction": direction, "points": points, "ratio": ratio}


def _reason_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {r["reason"]: r for r in payload.get("rows", [])}


def what_changed(con: sqlite3.Connection, base: Filters, week: str) -> dict[str, Any]:
    """Section 1: volume, the reason mix, and what is new to this week."""
    this_week = _week_filters(base, week)
    prev_week = _week_filters(base, week_add(week, -1))
    prior = _range_filters(base, week_add(week, -RECENT_WEEKS), week_add(week, -1))

    now = Q.contact_reasons(con, this_week, compare_with_previous=False)
    before = Q.contact_reasons(con, prev_week, compare_with_previous=False)
    baseline = Q.contact_reasons(con, prior, compare_with_previous=False)

    n_now = now["scope"]["n_calls_in_scope"]
    n_before = before["scope"]["n_calls_in_scope"]
    n_baseline = baseline["scope"]["n_calls_in_scope"]
    weekly_average = round(n_baseline / RECENT_WEEKS, 1) if n_baseline else 0.0

    before_by = _reason_map(before)
    baseline_by = _reason_map(baseline)
    rows = []
    for r in now.get("rows", [])[:TOP_REASONS]:
        prev = before_by.get(r["reason"])
        base_row = baseline_by.get(r["reason"])
        base_share = round(100 * base_row["n_calls"] / n_baseline, 1) if base_row and n_baseline else None
        rows.append({
            "reason": r["reason"], "label": r["label"],
            "n_calls": r["n_calls"], "share_pct": r["share_pct"],
            "n_previous_week": prev["n_calls"] if prev else 0,
            "vs_previous_week": _delta(r["share_pct"], prev["share_pct"] if prev else None),
            "vs_four_week_average": _delta(r["share_pct"], base_share),
            "top_specific": [s["text"] for s in (r.get("top_specific_reasons") or [])[:2]],
            "call_ids": (r.get("sample_call_ids") or [])[:20],
        })

    # New to the week: a theme with calls now and none in the weeks just before it.
    seen_before = {t["theme_id"] for t in Q.list_themes(
        con, _range_filters(base, week_add(week, -NEW_THEME_LOOKBACK), week_add(week, -1)),
        sort_by="n_calls", limit=500).get("rows", [])}
    new_rows = [t for t in Q.list_themes(con, this_week, sort_by="n_calls", limit=500).get("rows", [])
                if t["theme_id"] not in seen_before]

    return {
        "week": week, "week_start": Q.week_monday(week), "week_end": Q.week_sunday(week),
        "n_calls": n_now, "n_calls_previous_week": n_before,
        "four_week_average": weekly_average,
        "vs_previous_week": _delta(float(n_now), float(n_before)),
        "vs_four_week_average": _delta(float(n_now), weekly_average),
        "reasons": rows,
        "new_this_week": [{"theme_id": t["theme_id"], "name": t["name"], "n_calls": t["n_calls"],
                           "driver_category": t.get("driver_category")} for t in new_rows[:5]],
        "n_new_this_week": len(new_rows),
    }


def what_drove_feeling(con: sqlite3.Connection, base: Filters, week: str) -> dict[str, Any]:
    """Section 2: the specific moments behind frustration and satisfaction, in the customers' words."""
    scope = _week_filters(base, week)
    out: dict[str, Any] = {"week": week}
    for polarity in ("negative", "positive"):
        payload = Q.sentiment_drivers(con, polarity, "theme", scope, limit=TOP_DRIVERS)
        rows = []
        for r in payload.get("rows", []):
            key = r.get("key")
            rows.append({
                "key": key, "name": r.get("name") or key,
                "theme_id": key if str(key).startswith("thm_") else None,
                "n_calls": r.get("n_calls"), "mean_sentiment": r.get("mean_sentiment"),
                "root_cause": r.get("root_cause"),
                "triggers": [t["text"] for t in (r.get("top_specific_drivers") or [])[:3]],
                "quotes": [{"quote": q["quote"], "call_id": q["call_id"],
                            "evidence_id": q.get("evidence_id")}
                           for q in (r.get("quotes") or [])[:2]],
            })
        out[polarity] = rows
        out[f"n_{polarity}_calls"] = sum(r["n_calls"] or 0 for r in rows)
    # On a complaint corpus positive topics rarely clear support; the moments carry it instead.
    moments = Q.sentiment_drivers(con, "positive", "driver_category", scope, limit=TOP_DRIVERS)
    out["positive_moments"] = (moments.get("data") or {}).get("positive_moments_by_category") or []
    return out


def needs_attention(con: sqlite3.Connection, base: Filters, week: str) -> dict[str, Any]:
    """Section 3: ranked by growth and by what customers say it cost them, not by volume alone."""
    emerging = Q.emerging_themes(con, week, base, min_recent=Q.MIN_SUPPORT, only_new=False, limit=8)
    scope = _week_filters(base, week)
    rows = []
    for r in emerging.get("rows", []):
        detail = Q.theme_detail(con, r["theme_id"], scope)
        data = detail.get("data") or {}
        rows.append({
            "theme_id": r["theme_id"], "name": r.get("name"), "status": r.get("status"),
            "n_recent": r.get("n_recent"), "expected_recent": r.get("expected_recent"),
            "z": r.get("z"), "robust_8w": r.get("robust_8w"),
            "first_seen_week": r.get("first_seen_week"),
            "n_calls_this_week": data.get("n_calls"),
            "unresolved_share": (data.get("resolution_split") or {}).get("unresolved_share"),
            "customer_asks": (data.get("customer_ask_split") or [])[:2],
            "root_cause": data.get("root_cause"),
            "call_ids": (detail.get("call_ids") or [])[:20],
        })
    data = emerging.get("data") or {}
    return {
        "week": week, "rows": rows,
        "n_tested": data.get("n_tested"),
        "expected_false_positives": data.get("expected_false_positives"),
        "status_counts": data.get("status_counts") or {},
        "fading": data.get("fading") or [],
    }


def supporting_calls(con: sqlite3.Connection, base: Filters, week: str,
                     sections: dict[str, Any]) -> dict[str, Any]:
    """Section 4: verbatim excerpts, distinct call counts, and what the evidence cannot bear."""
    scope = _week_filters(base, week)
    wanted: list[tuple[str, str]] = []
    for row in sections["needs_attention"]["rows"][:2]:
        wanted.append((row["theme_id"], row.get("name") or row["theme_id"]))
    for row in sections["drove_feeling"].get("negative", [])[:2]:
        if row.get("theme_id") and row["theme_id"] not in {w[0] for w in wanted}:
            wanted.append((row["theme_id"], row.get("name") or row["theme_id"]))

    recent = _range_filters(base, week_add(week, -(RECENT_WEEKS - 1)), week)
    groups = []
    for theme_id, name in wanted[:3]:
        window, used = week, scope
        quotes = Q.get_quotes(con, "theme", theme_id, None, used, n=MAX_QUOTES,
                              polarity="any", diverse=True)
        rows = quotes.get("rows", [])
        if len(rows) < 2:
            # One week is often too thin to read. Widen, and name the window rather than pretend.
            window, used = f"{week_add(week, -(RECENT_WEEKS - 1))}..{week}", recent
            quotes = Q.get_quotes(con, "theme", theme_id, None, used, n=MAX_QUOTES,
                                  polarity="any", diverse=True)
            rows = quotes.get("rows", [])
        groups.append({
            "theme_id": theme_id, "name": name, "window": window,
            "n_distinct_calls": len({r["call_id"] for r in rows}),
            "n_calls_in_window": quotes["scope"].get("n_calls_in_scope"),
            "quotes": [{"quote": r["quote"], "call_id": r["call_id"], "date": r.get("date"),
                        "product": r.get("product"), "evidence_id": r.get("evidence_id")}
                       for r in rows],
        })

    n_week = sections["changed"]["n_calls"]
    limits = [
        f"Every count here is contacts in {week} only, and one contact counts once per theme.",
        f"Nothing is ranked below {Q.MIN_SUPPORT} contacts, so a real problem seen {Q.MIN_SUPPORT - 1} "
        f"times this week is deliberately absent from these lists.",
        "Quotes are exact substrings of what the customer wrote or said; anything that did not verify "
        "was dropped rather than paraphrased.",
    ]
    widened = [g["name"] for g in groups if g["window"] != week]
    if widened:
        limits.append(f"{len(widened)} of these groups had fewer than two verified quotes inside the "
                      f"week, so their excerpts are drawn from the last {RECENT_WEEKS} weeks; each "
                      f"group states the window it used.")
    if n_week and n_week < 40:
        limits.append(f"Only {n_week} contacts landed in this week, so week-on-week movement here is "
                      f"noisy and a single day's intake can swing it.")
    return {"week": week, "groups": groups, "limits": limits}


def weekly_review(con: sqlite3.Connection, week: str | None, filters: Filters | None = None) -> dict[str, Any]:
    """All four sections for one week. `week` defaults to the index's as-of week."""
    base = filters or Filters()
    week = week or Q.as_of_or_meta(con, None)
    if not week:
        raise Q.QueryError("no week available: the index has no as_of_week")
    if week not in set(Q.available_weeks(con)):
        raise Q.NotFound(f"no contacts in {week}")
    changed = what_changed(con, base, week)
    drove = what_drove_feeling(con, base, week)
    attention = needs_attention(con, base, week)
    sections = {"changed": changed, "drove_feeling": drove, "needs_attention": attention}
    sections["supporting"] = supporting_calls(con, base, week, sections)
    return {
        "week": week,
        "week_start": changed["week_start"], "week_end": changed["week_end"],
        "filters": base.canonical(),
        "sections": sections,
    }
