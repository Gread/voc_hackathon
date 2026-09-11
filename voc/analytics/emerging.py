"""Emerging-issue score (DESIGN 7.2): pure functions over weekly counts, reusable on filtered row sets."""
from __future__ import annotations

import math
from datetime import date, timedelta
from typing import Iterable, Mapping

RECENT_WEEKS = 4
BASELINE_WEEKS = 16
RECENT_WEEKS_8W = 8
BASELINE_WEEKS_8W = 24
MIN_RECENT = 5
Z_CUT = 2.5
RATIO_CUT = 1.5
SMALL_SHARE = 0.05
NEW_WINDOW = 7            # first_seen_week >= A-7
FADING_MIN_BASELINE = 10
FALSE_POSITIVE_RATE = 0.006   # one-sided normal tail at z = 2.5
POSITIVE_STATUSES = ("new", "emerging", "growing")


# --- ISO week arithmetic ------------------------------------------------------------------

def parse_week(week: str) -> date:
    """Monday of an ISO week given as YYYY-Www."""
    year, num = week.split("-W")
    return date.fromisocalendar(int(year), int(num), 1)


def format_week(day: date) -> str:
    year, num, _ = day.isocalendar()
    return f"{year}-W{num:02d}"


def week_add(week: str, delta: int) -> str:
    return format_week(parse_week(week) + timedelta(weeks=delta))


def weeks_between(start: str, end: str) -> list[str]:
    """Every ISO week from start to end inclusive, ascending; empty when end < start."""
    out: list[str] = []
    day = parse_week(start)
    last = parse_week(end)
    while day <= last:
        out.append(format_week(day))
        day += timedelta(weeks=1)
    return out


def previous_weeks(week: str, n: int) -> list[str]:
    """The n weeks strictly before `week`, ascending."""
    return weeks_between(week_add(week, -n), week_add(week, -1)) if n > 0 else []


def recent_weeks(as_of_week: str, recent: int = RECENT_WEEKS) -> list[str]:
    """The `recent` weeks ending at as_of_week inclusive."""
    return weeks_between(week_add(as_of_week, -(recent - 1)), as_of_week)


def baseline_weeks(as_of_week: str, recent: int = RECENT_WEEKS, baseline: int = BASELINE_WEEKS) -> list[str]:
    """The `baseline` weeks that end just before the recent window."""
    return previous_weeks(week_add(as_of_week, -(recent - 1)), baseline)


# --- counts -------------------------------------------------------------------------------

def weekly_totals(call_weeks: Iterable[str]) -> dict[str, int]:
    """Calls per week from one week value per call."""
    out: dict[str, int] = {}
    for week in call_weeks:
        out[week] = out.get(week, 0) + 1
    return out


def entity_weekly_counts(rows: Iterable[tuple[str, str, str]]) -> dict[str, dict[str, int]]:
    """(entity_id, call_id, week) rows -> {entity_id: {week: n_calls}}; a call counts once per entity."""
    seen: set[tuple[str, str]] = set()
    out: dict[str, dict[str, int]] = {}
    for entity_id, call_id, week in rows:
        if (entity_id, call_id) in seen:
            continue
        seen.add((entity_id, call_id))
        counts = out.setdefault(entity_id, {})
        counts[week] = counts.get(week, 0) + 1
    return out


def first_seen(entity_weekly: Mapping[str, int]) -> str | None:
    weeks = [w for w, n in entity_weekly.items() if n > 0]
    return min(weeks) if weeks else None


# --- scoring ------------------------------------------------------------------------------

def status_of(n_recent: int, n_baseline: int, z: float, ratio: float, weeks_recent: int, share_recent: float,
              first_seen_week: str | None, as_of_week: str, min_recent: int = MIN_RECENT) -> str:
    """First matching rule wins, in the order of DESIGN 7.2."""
    if n_recent < min_recent:
        return "insufficient"
    if n_baseline <= 1 and first_seen_week is not None and first_seen_week >= week_add(as_of_week, -NEW_WINDOW) \
            and weeks_recent >= 2:
        return "new"
    if z >= Z_CUT and ratio >= RATIO_CUT and weeks_recent >= 2:
        return "emerging" if share_recent < SMALL_SHARE else "growing"
    if z <= -Z_CUT and n_baseline >= FADING_MIN_BASELINE:
        return "fading"
    return "stable"


def score_entity(entity_weekly: Mapping[str, int], total_weekly: Mapping[str, int], as_of_week: str,
                 first_seen_week: str | None = None, recent: int = RECENT_WEEKS, baseline: int = BASELINE_WEEKS,
                 min_recent: int = MIN_RECENT) -> dict:
    """Score one entity at one as-of week from {week: n} maps (entity and all calls)."""
    r_weeks = recent_weeks(as_of_week, recent)
    b_weeks = baseline_weeks(as_of_week, recent, baseline)
    n_r = sum(entity_weekly.get(w, 0) for w in r_weeks)
    big_n_r = sum(total_weekly.get(w, 0) for w in r_weeks)
    n_b = sum(entity_weekly.get(w, 0) for w in b_weeks)
    big_n_b = sum(total_weekly.get(w, 0) for w in b_weeks)
    p_b = (n_b + 0.5) / (big_n_b + 1.0)
    expected = p_b * big_n_r
    z = (n_r - expected) / math.sqrt(expected + 0.5)
    ratio = ((n_r + 0.5) / (big_n_r + 1.0)) / p_b
    weeks_r = sum(1 for w in r_weeks if entity_weekly.get(w, 0) > 0)
    share_r = n_r / big_n_r if big_n_r else 0.0
    if first_seen_week is None:
        first_seen_week = first_seen(entity_weekly)
    status = status_of(n_r, n_b, z, ratio, weeks_r, share_r, first_seen_week, as_of_week, min_recent)
    return {
        "n_recent": n_r, "expected_recent": expected, "n_baseline": n_b, "z": z, "ratio": ratio,
        "weeks_recent": weeks_r, "share_recent": share_r, "n_total_recent": big_n_r, "n_total_baseline": big_n_b,
        "first_seen_week": first_seen_week, "status": status, "emerging_score": z * math.log1p(n_r),
    }


def score_entities(entities: Mapping[str, Mapping[str, int]], total_weekly: Mapping[str, int], as_of_week: str,
                   first_seen_weeks: Mapping[str, str | None] | None = None, min_recent: int = MIN_RECENT) -> dict[str, dict]:
    """Score every entity at one as-of week, with the 8/24-week sensitivity run and the false-positive line."""
    first_seen_weeks = first_seen_weeks or {}
    out: dict[str, dict] = {}
    for entity_id, weekly in entities.items():
        fsw = first_seen_weeks.get(entity_id)
        row = score_entity(weekly, total_weekly, as_of_week, fsw, min_recent=min_recent)
        row_8w = score_entity(weekly, total_weekly, as_of_week, fsw, RECENT_WEEKS_8W, BASELINE_WEEKS_8W, min_recent)
        row["status_8w"] = row_8w["status"]
        row["robust"] = row["status"] in POSITIVE_STATUSES and row_8w["status"] in POSITIVE_STATUSES
        out[entity_id] = row
    n_tested = sum(1 for r in out.values() if r["n_recent"] >= min_recent)
    for row in out.values():
        row["n_tested"] = n_tested
        row["expected_false_positives"] = n_tested * FALSE_POSITIVE_RATE
    return out


def rank_emerging(scores: Mapping[str, dict]) -> list[tuple[str, dict]]:
    """new/emerging/growing rows by emerging_score descending (z-based; growth ratio is never the key)."""
    rows = [(k, v) for k, v in scores.items() if v["status"] in POSITIVE_STATUSES]
    return sorted(rows, key=lambda kv: (-kv[1]["emerging_score"], kv[0]))
