"""Typed query functions over the SQLite index. Every function returns a dict with rows/data,
the list of statements it ran (`sql`) and the FULL distinct list of call ids behind the result,
so the agent tools, the REST API and the `voc tool` CLI share one path. SQL lives here only."""
from __future__ import annotations

import math
import re
import sqlite3
from datetime import date, timedelta
from typing import Any

from voc.schemas.filters import DIMENSIONS, Filters
from voc.store.db import get_meta
from voc.taxonomy import loader as tx

MIN_SUPPORT = 5          # no ranking below this many calls
MIN_SLICE = 50           # segment rows need at least this many calls in the slice
Z95 = 1.96
FALSE_POSITIVE_RATE = 0.006   # one-sided normal tail at z = 2.5
RANKED_STATUSES = ("new", "emerging", "growing")
ENUM_DIMS = {"product": "products", "channel": "channel", "region_group": "region_group", "segment": "segment"}
BREAKDOWN_DIMS = ("product", "channel", "region_group", "region", "segment", "company", "month", "week")
ENTITY_TYPES = ("theme", "reason", "driver_category", "customer_ask")


class QueryError(ValueError):
    """Invalid arguments (unknown enum value, bad date, ...)."""


class NotFound(QueryError):
    """A theme or call id that does not exist."""


# --- statistics helpers (kept local so this module never depends on voc/analytics) --------------

def wilson(n: int, total: int, z: float = Z95) -> tuple[float, float]:
    """Wilson 95 % interval for a share n / total; (0, 0) when the slice is empty."""
    if total <= 0:
        return (0.0, 0.0)
    p = n / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))


def wls_direction(xs: list[float], ys: list[float], ws: list[float]) -> dict[str, Any]:
    """Weighted least squares of y on x; direction by |t| >= 2 (DESIGN 7.4)."""
    pts = [(x, y, w) for x, y, w in zip(xs, ys, ws) if w > 0]
    if len(pts) < 3 or sum(w for _, _, w in pts) < MIN_SUPPORT:
        return {"direction": "insufficient", "slope": 0.0, "t_stat": 0.0, "n_points": len(pts)}
    total_w = sum(w for _, _, w in pts)
    xbar = sum(w * x for x, _, w in pts) / total_w
    ybar = sum(w * y for _, y, w in pts) / total_w
    sxx = sum(w * (x - xbar) ** 2 for x, _, w in pts)
    if sxx == 0:
        return {"direction": "flat", "slope": 0.0, "t_stat": 0.0, "n_points": len(pts)}
    slope = sum(w * (x - xbar) * (y - ybar) for x, y, w in pts) / sxx
    intercept = ybar - slope * xbar
    rss = sum(w * (y - intercept - slope * x) ** 2 for x, y, w in pts)
    se = math.sqrt(rss / (len(pts) - 2) / sxx) if rss > 0 else 0.0
    t = slope / se if se > 0 else (0.0 if slope == 0 else math.copysign(99.0, slope))
    direction = "rising" if t >= 2 else "falling" if t <= -2 else "flat"
    return {"direction": direction, "slope": round(slope, 6), "t_stat": round(t, 2), "n_points": len(pts)}


def week_shift(week: str, delta: int) -> str:
    """ISO week string shifted by delta weeks (YYYY-Www)."""
    y, w = int(week[:4]), int(week[6:])
    d = date.fromisocalendar(y, w, 1) + timedelta(weeks=delta)
    iy, iw, _ = d.isocalendar()
    return f"{iy}-W{iw:02d}"


def emerging_stats(n_recent: int, total_recent: int, n_baseline: int, total_baseline: int,
                   weeks_recent: int, first_seen_week: str | None, as_of_week: str) -> dict[str, Any]:
    """Poisson z with Jeffreys pseudo-count and the status ladder of DESIGN 7.2."""
    p_b = (n_baseline + 0.5) / (total_baseline + 1)
    expected = p_b * total_recent
    z = (n_recent - expected) / math.sqrt(expected + 0.5)
    ratio = ((n_recent + 0.5) / (total_recent + 1)) / p_b
    share = n_recent / total_recent if total_recent else 0.0
    is_new = n_baseline <= 1 and bool(first_seen_week) and first_seen_week >= week_shift(as_of_week, -7)
    accelerating = z >= 2.5 and ratio >= 1.5 and weeks_recent >= 2
    if n_recent < MIN_SUPPORT:
        status = "insufficient"
    elif is_new and weeks_recent >= 2:
        status = "new"
    elif accelerating:
        status = "emerging" if share < 0.05 else "growing"
    elif z <= -2.5 and n_baseline >= 10:
        status = "fading"
    else:
        status = "stable"
    return {"n_recent": n_recent, "expected_recent": round(expected, 2), "n_baseline": n_baseline,
            "z": round(z, 2), "ratio": round(ratio, 2), "weeks_recent": weeks_recent,
            "share_recent": round(share, 4), "status": status,
            "emerging_score": round(z * math.log(1 + n_recent), 3)}


def score_from_weekly(entity_weekly: dict[str, int], total_weekly: dict[str, int], as_of_week: str,
                      first_seen_week: str | None, recent: int = 4, baseline: int = 16) -> dict[str, Any]:
    """Emerging statistics from weekly counts: R = A-(recent-1)..A, B = the `baseline` weeks before."""
    r_weeks = [week_shift(as_of_week, -i) for i in range(recent)]
    b_weeks = [week_shift(as_of_week, -i) for i in range(recent, recent + baseline)]
    n_r = sum(entity_weekly.get(w, 0) for w in r_weeks)
    n_b = sum(entity_weekly.get(w, 0) for w in b_weeks)
    total_r = sum(total_weekly.get(w, 0) for w in r_weeks)
    total_b = sum(total_weekly.get(w, 0) for w in b_weeks)
    weeks_r = sum(1 for w in r_weeks if entity_weekly.get(w, 0) > 0)
    return emerging_stats(n_r, total_r, n_b, total_b, weeks_r, first_seen_week, as_of_week)


# --- filters -> SQL ------------------------------------------------------------------------------

def _iso_date(value: str, field: str) -> str:
    try:
        return date.fromisoformat(str(value)[:10]).isoformat()
    except ValueError as exc:
        raise QueryError(f"{field} must be an ISO date (YYYY-MM-DD): {value}") from exc


def filters_where(filters: Filters | None, alias: str = "c") -> tuple[str, list[Any]]:
    """WHERE fragment over the dimension columns of `calls` plus the date range; '1=1' when empty."""
    f = filters or Filters()
    clauses: list[str] = []
    params: list[Any] = []
    for dim in DIMENSIONS:
        vals = getattr(f, dim)
        if not vals:
            continue
        vals = sorted(set(str(v) for v in vals))
        if dim in ENUM_DIMS:
            bad = [v for v in vals if v not in tx.codes(ENUM_DIMS[dim])]
            if bad:
                raise QueryError(f"unknown {dim} value(s): {', '.join(bad)}")
        clauses.append(f"{alias}.{dim} IN ({', '.join('?' * len(vals))})")
        params.extend(vals)
    if f.date_from:
        clauses.append(f"{alias}.date >= ?")
        params.append(_iso_date(f.date_from, "date_from"))
    if f.date_to:
        clauses.append(f"{alias}.date <= ?")
        params.append(_iso_date(f.date_to, "date_to"))
    return (" AND ".join(clauses) or "1=1", params)


# --- statement tracker ---------------------------------------------------------------------------

def _squash(sql: str) -> str:
    return re.sub(r"\s+", " ", sql).strip()


class Q:
    """Runs statements on one connection and records each one plus the call ids it yields."""

    def __init__(self, con: sqlite3.Connection):
        self.con = con
        self.sql: list[dict[str, Any]] = []
        self.call_ids: dict[str, None] = {}   # insertion-ordered set

    def rows(self, sql: str, params: list[Any] | tuple = ()) -> list[sqlite3.Row]:
        self.sql.append({"sql": _squash(sql), "params": list(params)})
        return self.con.execute(sql, list(params)).fetchall()

    def one(self, sql: str, params: list[Any] | tuple = ()) -> sqlite3.Row | None:
        rows = self.rows(sql, params)
        return rows[0] if rows else None

    def calls(self, sql: str, params: list[Any] | tuple = ()) -> list[sqlite3.Row]:
        """A statement whose rows carry a call_id column; its ids become part of the result's call ids."""
        rows = self.rows(sql, params)
        self.sql[-1]["purpose"] = "call_ids"
        for r in rows:
            self.call_ids.setdefault(r["call_id"])
        return rows

    def result(self, **payload: Any) -> dict[str, Any]:
        payload.setdefault("rows", [])
        payload.setdefault("data", {})
        payload["sql"] = self.sql
        payload["call_ids"] = list(self.call_ids)
        return payload


def _placeholders(values: list[Any]) -> str:
    return ", ".join("?" * len(values))


def _pct(n: int, total: int) -> float:
    return round(100.0 * n / total, 1) if total else 0.0


def _share(n: int, total: int) -> float:
    return round(n / total, 4) if total else 0.0


def _norm_text(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip().rstrip(".!;,")


def _top_texts(pairs: list[tuple[str, str]], k: int) -> list[dict[str, Any]]:
    """Group (text, call_id) pairs by normalised text; top k by distinct calls with an example."""
    groups: dict[str, dict[str, Any]] = {}
    for text, call_id in pairs:
        key = _norm_text(text)
        if not key:
            continue
        g = groups.setdefault(key, {"text": text.strip(), "calls": set()})
        g["calls"].add(call_id)
    ranked = sorted(groups.values(), key=lambda g: (-len(g["calls"]), g["text"]))
    return [{"text": g["text"], "n": len(g["calls"])} for g in ranked[:k]]


def scope(q: Q, filters: Filters) -> dict[str, Any]:
    where, params = filters_where(filters)
    r = q.one(f"SELECT COUNT(*) AS n, MIN(c.date) AS d0, MAX(c.date) AS d1 FROM calls c WHERE {where}", params)
    return {"n_calls_in_scope": int(r["n"]), "date_from": filters.date_from or r["d0"],
            "date_to": filters.date_to or r["d1"]}


def as_of_or_meta(con: sqlite3.Connection, as_of_week: str | None) -> str | None:
    return as_of_week or get_meta(con, "as_of_week")


# --- entities ------------------------------------------------------------------------------------

def resolve_theme_id(con: sqlite3.Connection, theme_id: str) -> str:
    """Follow merged_into chains to the effective theme; NotFound for unknown ids."""
    if not theme_id:
        raise QueryError("a theme id is required")
    seen: set[str] = set()
    current = theme_id
    while current not in seen:
        seen.add(current)
        row = con.execute("SELECT status, merged_into, effective_theme_id FROM themes WHERE theme_id = ?", (current,)).fetchone()
        if row is None:
            raise NotFound(f"unknown theme_id {theme_id}")
        if row["status"] != "merged":
            return current
        current = row["effective_theme_id"] or row["merged_into"] or current
    return current


def entity_type_of(con: sqlite3.Connection, entity_id: str) -> str:
    if entity_id.startswith("thm_"):
        return "theme"
    if entity_id in tx.codes("contact_reasons"):
        return "reason"
    if entity_id in tx.codes("driver_categories"):
        return "driver_category"
    if entity_id in tx.codes("customer_asks"):
        return "customer_ask"
    raise NotFound(f"unknown entity id {entity_id}")


def _entity_join(con: sqlite3.Connection, entity_type: str, entity_id: str | None) -> tuple[str, str, list[Any]]:
    """JOIN fragment (alias x, joined to calls c) and the condition selecting one entity."""
    if entity_type == "all" or entity_id is None:
        return ("", "1=1", [])
    if entity_type == "theme":
        return ("JOIN v_theme_calls x ON x.call_id = c.call_id", "x.theme_id = ?", [resolve_theme_id(con, entity_id)])
    if entity_type == "reason":
        return ("JOIN call_reasons x ON x.call_id = c.call_id", "x.reason = ?", [entity_id])
    if entity_type == "driver_category":
        return ("JOIN topics x ON x.call_id = c.call_id", "x.driver_category = ?", [entity_id])
    if entity_type == "customer_ask":
        return ("JOIN extractions x ON x.call_id = c.call_id", "x.customer_ask = ?", [entity_id])
    raise QueryError(f"unknown entity type {entity_type}")


def _entity_name(con: sqlite3.Connection, entity_type: str, entity_id: str) -> str:
    if entity_type == "theme":
        row = con.execute("SELECT name FROM themes WHERE theme_id = ?", (entity_id,)).fetchone()
        return row["name"] if row else entity_id
    kind = {"reason": "contact_reasons", "driver_category": "driver_categories", "customer_ask": "customer_asks"}[entity_type]
    return tx.labels(kind).get(entity_id, entity_id)


# --- shared row builders -------------------------------------------------------------------------

def _theme_rows(q: Q, filters: Filters, sort_by: str, polarity: str, driver_category: str | None,
                limit: int, as_of_week: str | None) -> list[dict[str, Any]]:
    """Active themes ranked in the filtered scope (catch-alls and weak groupings excluded)."""
    where, params = filters_where(filters)
    conds, cparams = ["th.status = 'active'", "COALESCE(th.grouping_quality, 'ok') != 'weak'"], []
    if polarity != "any":
        conds.append("th.polarity = ?")
        cparams.append(polarity)
    if driver_category:
        conds.append("th.driver_category = ?")
        cparams.append(driver_category)
    order = {"n_calls": "n_calls DESC", "neg_mass": "neg_mass DESC", "pos_mass": "pos_mass DESC",
             "emerging_score": "COALESCE(es.emerging_score, -1e9) DESC", "n_wordings": "th.n_wordings DESC"}[sort_by]
    rows = q.rows(f"""
        SELECT th.theme_id, th.name, th.problem_statement, th.root_cause, th.polarity, th.driver_category,
               th.n_wordings, th.n_products, COALESCE(th.grouping_quality, 'ok') AS grouping_quality,
               th.first_seen_week, es.status AS status_at_as_of, es.emerging_score,
               COUNT(DISTINCT s.call_id) AS n_calls,
               SUM(CASE WHEN s.min_sentiment < 0 THEN -s.min_sentiment ELSE 0 END) AS neg_mass,
               SUM(CASE WHEN s.max_sentiment > 0 THEN s.max_sentiment ELSE 0 END) AS pos_mass,
               AVG(CASE WHEN th.polarity = 'positive' THEN s.max_sentiment ELSE s.min_sentiment END) AS mean_sentiment
        FROM themes th
        JOIN v_theme_call_sentiment s ON s.theme_id = th.theme_id
        JOIN calls c ON c.call_id = s.call_id
        LEFT JOIN emerging_scores es ON es.entity_type = 'theme' AND es.entity_id = th.theme_id AND es.as_of_week = ?
        WHERE {where} AND {' AND '.join(conds)}
        GROUP BY th.theme_id HAVING n_calls >= ?
        ORDER BY {order}, th.theme_id LIMIT ?""", [as_of_week, *params, *cparams, MIN_SUPPORT, limit])
    out = [dict(r) for r in rows]
    if not out:
        return out
    ids = [r["theme_id"] for r in out]
    samples = q.calls(f"""
        SELECT tc.theme_id, tc.call_id FROM v_theme_calls tc JOIN calls c ON c.call_id = tc.call_id
        WHERE {where} AND tc.theme_id IN ({_placeholders(ids)}) ORDER BY c.date DESC, tc.call_id""", [*params, *ids])
    by_theme: dict[str, list[str]] = {}
    for s in samples:
        by_theme.setdefault(s["theme_id"], []).append(s["call_id"])
    for r in out:
        r["mean_sentiment"] = round(r["mean_sentiment"], 2) if r["mean_sentiment"] is not None else None
        r["emerging_score"] = round(r["emerging_score"], 3) if r["emerging_score"] is not None else None
        r["sample_call_ids"] = by_theme.get(r["theme_id"], [])[:5]
    return out


def _previous_period(sc: dict[str, Any]) -> tuple[str, str] | None:
    if not sc.get("date_from") or not sc.get("date_to"):
        return None
    d0, d1 = date.fromisoformat(sc["date_from"]), date.fromisoformat(sc["date_to"])
    length = (d1 - d0).days + 1
    prev_to = d0 - timedelta(days=1)
    return ((prev_to - timedelta(days=length - 1)).isoformat(), prev_to.isoformat())


def _reason_rows(q: Q, filters: Filters, sc: dict[str, Any], compare_with_previous: bool) -> list[dict[str, Any]]:
    where, params = filters_where(filters)
    total = sc["n_calls_in_scope"]
    counts = {r["reason"]: r["n"] for r in q.rows(f"""
        SELECT r.reason, COUNT(DISTINCT r.call_id) AS n FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
        WHERE {where} GROUP BY r.reason""", params)}
    month_totals = q.rows(f"SELECT c.month, COUNT(*) AS n FROM calls c WHERE {where} GROUP BY c.month ORDER BY c.month", params)
    monthly: dict[str, dict[str, int]] = {}
    for r in q.rows(f"""
        SELECT r.reason, c.month, COUNT(DISTINCT r.call_id) AS n FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
        WHERE {where} GROUP BY r.reason, c.month""", params):
        monthly.setdefault(r["reason"], {})[r["month"]] = r["n"]
    specifics: dict[str, list[tuple[str, str]]] = {}
    for r in q.rows(f"""
        SELECT r.reason, r.specific_reason, r.call_id FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
        WHERE {where}""", params):
        specifics.setdefault(r["reason"], []).append((r["specific_reason"] or "", r["call_id"]))
    samples: dict[str, list[str]] = {}
    for r in q.calls(f"""
        SELECT r.reason, r.call_id FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
        WHERE {where} ORDER BY c.date DESC, r.call_id""", params):
        samples.setdefault(r["reason"], []).append(r["call_id"])
    prev_counts: dict[str, int] = {}
    prev_total = 0
    prev = _previous_period(sc) if compare_with_previous else None
    if prev:
        pf = filters.model_copy(update={"date_from": prev[0], "date_to": prev[1]})
        pwhere, pparams = filters_where(pf)
        prev_total = int(q.one(f"SELECT COUNT(*) AS n FROM calls c WHERE {pwhere}", pparams)["n"])
        prev_counts = {r["reason"]: r["n"] for r in q.rows(f"""
            SELECT r.reason, COUNT(DISTINCT r.call_id) AS n FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
            WHERE {pwhere} GROUP BY r.reason""", pparams)}
    last_months = [r["month"] for r in month_totals][-6:]
    weights = {r["month"]: r["n"] for r in month_totals}
    labels = tx.labels("contact_reasons")
    rows = []
    for reason, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if n < MIN_SUPPORT:
            continue
        fit = wls_direction(list(range(len(last_months))),
                            [_share(monthly.get(reason, {}).get(m, 0), weights[m]) for m in last_months],
                            [weights[m] for m in last_months])
        row: dict[str, Any] = {"reason": reason, "label": labels.get(reason, reason), "n_calls": n,
                               "share": _share(n, total), "share_pct": _pct(n, total),
                               "direction": fit["direction"], "t_stat": fit["t_stat"],
                               "top_specific_reasons": _top_texts(specifics.get(reason, []), 3),
                               "sample_call_ids": samples.get(reason, [])[:5]}
        if prev:
            pn = prev_counts.get(reason, 0)
            row.update({"n_previous": pn, "delta_n": n - pn,
                        "delta_share_pts": round(_pct(n, total) - _pct(pn, prev_total), 1)})
        rows.append(row)
    return rows


def _breakdown_rows(q: Q, filters: Filters, entity_type: str, entity_id: str | None, by: str,
                    min_n: int = MIN_SUPPORT, limit: int | None = None) -> dict[str, Any]:
    if by not in BREAKDOWN_DIMS:
        raise QueryError(f"cannot break down by {by}")
    where, params = filters_where(filters)
    join, cond, cparams = _entity_join(q.con, entity_type, entity_id)
    slices = {r["value"]: r["n_slice"] for r in q.rows(
        f"SELECT c.{by} AS value, COUNT(*) AS n_slice FROM calls c WHERE {where} GROUP BY value", params)}
    total = sum(slices.values())
    if join:
        hits = {r["value"]: r["n"] for r in q.rows(f"""
            SELECT c.{by} AS value, COUNT(DISTINCT c.call_id) AS n FROM calls c {join}
            WHERE {where} AND {cond} GROUP BY value""", [*params, *cparams])}
        n_entity = len(q.calls(f"SELECT DISTINCT c.call_id FROM calls c {join} WHERE {where} AND {cond}", [*params, *cparams]))
    else:
        hits = dict(slices)
        n_entity = len(q.calls(f"SELECT c.call_id FROM calls c WHERE {where}", params))
    overall_share = _share(n_entity, total)
    rows = []
    for value, n_slice in slices.items():
        n = hits.get(value, 0)
        share = _share(n, n_slice)
        lo, hi = wilson(n, n_slice)
        rows.append({"value": value, "n_calls": n, "n_slice": n_slice, "share": share, "share_pct": _pct(n, n_slice),
                     "ci_lo": lo, "ci_hi": hi,
                     "lift": round(share / overall_share, 2) if overall_share else None,
                     "suppressed": n_slice < MIN_SLICE or n < min_n})
    rows.sort(key=(lambda r: r["value"]) if by in ("month", "week") else (lambda r: (-r["n_calls"], r["value"])))
    if limit:
        rows = rows[:limit]
    return {"overall_share": overall_share, "n_entity": n_entity, "n_scope": total, "rows": rows}


def period_series(q: Q, filters: Filters, entity_type: str, entity_id: str, grain: str) -> list[dict[str, Any]]:
    if grain not in ("week", "month"):
        raise QueryError("grain must be week or month")
    where, params = filters_where(filters)
    join, cond, cparams = _entity_join(q.con, entity_type, entity_id)
    totals = q.rows(f"SELECT c.{grain} AS period, COUNT(*) AS n FROM calls c WHERE {where} GROUP BY period ORDER BY period", params)
    counts: dict[str, int] = {}
    for r in q.calls(f"""
        SELECT c.{grain} AS period, c.call_id FROM calls c {join}
        WHERE {where} AND {cond} GROUP BY period, c.call_id""", [*params, *cparams]):
        counts[r["period"]] = counts.get(r["period"], 0) + 1
    series = []
    for t in totals:
        n, total = counts.get(t["period"], 0), t["n"]
        lo, hi = wilson(n, total)
        series.append({"period": t["period"], "n_calls": n, "n_period": total, "share": _share(n, total),
                       "ci_lo": lo, "ci_hi": hi})
    return series


def _direction_of(series: list[dict[str, Any]], grain: str) -> dict[str, Any]:
    window = 6 if grain == "month" else 26
    recent = series[-window:]
    fit = wls_direction(list(range(len(recent))), [p["share"] for p in recent], [p["n_period"] for p in recent])
    half = 3 if grain == "month" else 13
    cur, prev = series[-half:], series[-2 * half:-half]

    def _agg(chunk: list[dict[str, Any]]) -> dict[str, Any]:
        n, total = sum(p["n_calls"] for p in chunk), sum(p["n_period"] for p in chunk)
        return {"periods": [p["period"] for p in chunk], "n_calls": n, "n_period": total, "share_pct": _pct(n, total)}

    c, p = _agg(cur), _agg(prev)
    return {"direction": fit["direction"], "t_stat": fit["t_stat"], "slope": fit["slope"],
            "change_pts": round(c["share_pct"] - p["share_pct"], 1) if prev else None,
            "change": {"current": c, "previous": p}}


# --- tool-facing query functions ----------------------------------------------------------------

def get_overview(con: sqlite3.Connection, filters: Filters, as_of_week: str | None = None) -> dict[str, Any]:
    q = Q(con)
    sc = scope(q, filters)
    where, params = filters_where(filters)
    as_of = as_of_or_meta(con, as_of_week)
    q.calls(f"SELECT c.call_id FROM calls c WHERE {where}", params)
    t = q.one(f"""
        SELECT (SELECT COUNT(*) FROM topics t JOIN calls c ON c.call_id = t.call_id WHERE {where}) AS n_topics,
               (SELECT COUNT(DISTINCT tc.theme_id) FROM v_theme_calls tc JOIN calls c ON c.call_id = tc.call_id
                 JOIN themes th ON th.theme_id = tc.theme_id WHERE th.status = 'active' AND {where}) AS n_themes,
               (SELECT COALESCE(SUM(1.0 / c.sampling_fraction), 0) FROM calls c WHERE {where}) AS population_estimate""",
              [*params, *params, *params])
    per_month = [dict(r) for r in q.rows(f"""
        SELECT c.month, COUNT(*) AS n_calls, ROUND(SUM(1.0 / c.sampling_fraction)) AS population_estimate
        FROM calls c WHERE {where} GROUP BY c.month ORDER BY c.month""", params)]
    if filters.is_empty():
        pop = {r["period"]: r["population_n"] for r in q.rows("SELECT period, population_n FROM period_totals WHERE period_kind = 'month'")}
        for m in per_month:
            m["population_n"] = pop.get(m["month"])
    reasons = _reason_rows(q, filters, sc, compare_with_previous=True)[:8]
    themes = _theme_rows(q, filters, "n_calls", "any", None, 8, as_of)
    total = sc["n_calls_in_scope"]

    def _split(col: str, table: str = "extractions") -> list[dict[str, Any]]:
        return [{"value": r["v"], "n_calls": r["n"], "share_pct": _pct(r["n"], total)} for r in q.rows(f"""
            SELECT e.{col} AS v, COUNT(*) AS n FROM {table} e JOIN calls c ON c.call_id = e.call_id
            WHERE {where} GROUP BY v ORDER BY n DESC, v""", params)]

    data = {"totals": {"n_calls": total, "n_topics": t["n_topics"], "n_active_themes": t["n_themes"],
                       "population_estimate": int(round(t["population_estimate"] or 0)),
                       "date_from": sc["date_from"], "date_to": sc["date_to"], "as_of_week": as_of},
            "calls_per_month": per_month, "top_reasons": reasons, "top_themes": themes,
            "sentiment_distribution": sorted(_split("overall_sentiment"), key=lambda r: r["value"] if r["value"] is not None else 0),
            "resolution_split": _split("resolution_status"), "customer_ask_split": _split("customer_ask")}
    return q.result(data=data, scope=sc)


def contact_reasons(con: sqlite3.Connection, filters: Filters, compare_with_previous: bool = True) -> dict[str, Any]:
    q = Q(con)
    sc = scope(q, filters)
    rows = _reason_rows(q, filters, sc, compare_with_previous)
    data: dict[str, Any] = {"n_scope": sc["n_calls_in_scope"], "min_support": MIN_SUPPORT}
    if compare_with_previous:
        data["previous_period"] = _previous_period(sc)
    return q.result(rows=rows, data=data, scope=sc)


def list_themes(con: sqlite3.Connection, filters: Filters, sort_by: str = "n_calls", polarity: str = "any",
                driver_category: str | None = None, limit: int = 10, as_of_week: str | None = None) -> dict[str, Any]:
    q = Q(con)
    sc = scope(q, filters)
    as_of = as_of_or_meta(con, as_of_week)
    rows = _theme_rows(q, filters, sort_by, polarity, driver_category, limit, as_of)
    total = sc["n_calls_in_scope"]
    for r in rows:
        r["share"] = _share(r["n_calls"], total)
        r["share_pct"] = _pct(r["n_calls"], total)
    return q.result(rows=rows, data={"sort_by": sort_by, "polarity": polarity, "as_of_week": as_of,
                                     "n_scope": total, "min_support": MIN_SUPPORT}, scope=sc)


def theme_detail(con: sqlite3.Connection, theme_id: str, filters: Filters, as_of_week: str | None = None) -> dict[str, Any]:
    q = Q(con)
    tid = resolve_theme_id(con, theme_id)
    th = q.one("SELECT * FROM themes WHERE theme_id = ?", [tid])
    sc = scope(q, filters)
    where, params = filters_where(filters)
    as_of = as_of_or_meta(con, as_of_week)
    calls = q.calls(f"""
        SELECT tc.call_id, c.date, c.week, c.month, c.region FROM v_theme_calls tc JOIN calls c ON c.call_id = tc.call_id
        WHERE tc.theme_id = ? AND {where} ORDER BY c.date""", [tid, *params])
    member_src = f"""FROM theme_members tm JOIN topics t ON t.topic_id = tm.topic_id JOIN calls c ON c.call_id = t.call_id
                     WHERE tm.effective_theme_id = ? AND {where}"""
    mix = [{"driver_category": r["driver_category"], "n_calls": r["n"]} for r in q.rows(
        f"SELECT t.driver_category, COUNT(DISTINCT t.call_id) AS n {member_src} GROUP BY t.driver_category ORDER BY n DESC", [tid, *params])]
    drivers = _top_texts([(r["driver"] or "", r["call_id"]) for r in q.rows(f"SELECT t.driver, t.call_id {member_src}", [tid, *params])], 5)
    wordings = [dict(r) for r in q.rows(f"""
        SELECT w.rank, w.issue_statement, w.call_id, w.date, w.product FROM theme_wordings w JOIN calls c ON c.call_id = w.call_id
        WHERE w.theme_id = ? AND {where} ORDER BY w.rank LIMIT 12""", [tid, *params])]
    by_product = _breakdown_rows(q, filters, "theme", tid, "product", limit=5)["rows"]
    by_channel = _breakdown_rows(q, filters, "theme", tid, "channel", limit=5)["rows"]
    weekly = period_series(q, filters, "theme", tid, "week")
    merges = [dict(r) for r in q.rows("""
        SELECT m.from_theme, f.name AS from_name, m.into_theme, m.pass, m.reason, m.judged_by, m.created_at
        FROM theme_merges m JOIN themes f ON f.theme_id = m.from_theme
        WHERE m.into_theme = ? OR f.effective_theme_id = ? ORDER BY m.created_at, m.from_theme""", [tid, tid])]
    es = q.one("SELECT * FROM emerging_scores WHERE entity_type = 'theme' AND entity_id = ? AND as_of_week = ?", [tid, as_of])
    n = len(calls)
    total = sc["n_calls_in_scope"]
    data = {"theme_id": tid, "requested_theme_id": theme_id, "name": th["name"], "problem_statement": th["problem_statement"],
            "root_cause": th["root_cause"], "polarity": th["polarity"], "driver_category": th["driver_category"],
            "theme_status": th["status"], "grouping_quality": th["grouping_quality"] or "ok",
            "n_calls": n, "share": _share(n, total), "share_pct": _pct(n, total), "n_scope": total,
            "n_wordings": th["n_wordings"], "n_products": th["n_products"],
            "n_states": len({r["region"] for r in calls} - {"unknown", None}),
            "months_active": sorted({r["month"] for r in calls}),
            "first_seen_week": min((r["week"] for r in calls), default=th["first_seen_week"]),
            "status": es["status"] if es else None, "as_of_week": as_of,
            "emerging": dict(es) if es else None,
            "driver_category_mix": mix, "top_specific_drivers": drivers, "wordings": wordings,
            "by_product": by_product, "by_channel": by_channel, "weekly_series": weekly,
            "trend": _direction_of(weekly, "week") if weekly else None, "merge_history": merges}
    return q.result(data=data, scope=sc)


def theme_trend(con: sqlite3.Connection, entity_ids: list[str], grain: str, filters: Filters) -> dict[str, Any]:
    if not entity_ids:
        raise QueryError("entity_ids must not be empty")
    q = Q(con)
    sc = scope(q, filters)
    rows = []
    for eid in entity_ids[:6]:
        etype = entity_type_of(con, eid)
        rid = resolve_theme_id(con, eid) if etype == "theme" else eid
        series = period_series(q, filters, etype, rid, grain)
        n = sum(p["n_calls"] for p in series)
        rows.append({"entity_id": rid, "entity_type": etype, "name": _entity_name(con, etype, rid),
                     "n_calls": n, "series": series, **(_direction_of(series, grain) if series else
                                                      {"direction": "insufficient", "t_stat": 0.0, "slope": 0.0, "change_pts": None, "change": {}})})
    return q.result(rows=rows, data={"grain": grain, "n_scope": sc["n_calls_in_scope"]}, scope=sc)


def _emerging_precomputed(q: Q, as_of: str) -> list[dict[str, Any]]:
    rows = q.rows("""
        SELECT es.*, th.name FROM emerging_scores es JOIN themes th ON th.theme_id = es.entity_id
        WHERE es.entity_type = 'theme' AND es.as_of_week = ? AND th.status = 'active'""", [as_of])
    out = []
    for r in rows:
        d = dict(r)
        d["theme_id"] = d.pop("entity_id")
        d["robust_8w"] = d["status"] in RANKED_STATUSES and (d.get("status_8w") in RANKED_STATUSES)
        out.append(d)
    return out


def _emerging_local(q: Q, filters: Filters, as_of: str) -> list[dict[str, Any]]:
    """Recompute the 4/16- and 8/24-week statistics from filtered weekly counts."""
    where, params = filters_where(filters)
    start = week_shift(as_of, -31)
    totals = {r["week"]: r["n"] for r in q.rows(
        f"SELECT c.week, COUNT(*) AS n FROM calls c WHERE {where} AND c.week BETWEEN ? AND ? GROUP BY c.week", [*params, start, as_of])}
    weekly: dict[str, dict[str, int]] = {}
    for r in q.rows(f"""
        SELECT tc.theme_id, c.week, COUNT(DISTINCT tc.call_id) AS n FROM v_theme_calls tc
        JOIN calls c ON c.call_id = tc.call_id JOIN themes th ON th.theme_id = tc.theme_id
        WHERE th.status = 'active' AND {where} AND c.week BETWEEN ? AND ? GROUP BY tc.theme_id, c.week""", [*params, start, as_of]):
        weekly.setdefault(r["theme_id"], {})[r["week"]] = r["n"]
    first = {r["theme_id"]: r["w"] for r in q.rows(f"""
        SELECT tc.theme_id, MIN(c.week) AS w FROM v_theme_calls tc JOIN calls c ON c.call_id = tc.call_id
        WHERE {where} AND c.week <= ? GROUP BY tc.theme_id""", [*params, as_of])}
    names = {r["theme_id"]: r["name"] for r in q.rows("SELECT theme_id, name FROM themes WHERE status = 'active'")}
    out = []
    for tid, counts in weekly.items():
        s4 = score_from_weekly(counts, totals, as_of, first.get(tid), 4, 16)
        s8 = score_from_weekly(counts, totals, as_of, first.get(tid), 8, 24)
        out.append({"theme_id": tid, "name": names.get(tid, tid), "as_of_week": as_of, **s4,
                    "first_seen_week": first.get(tid), "status_8w": s8["status"],
                    "robust_8w": s4["status"] in RANKED_STATUSES and s8["status"] in RANKED_STATUSES,
                    "novel_vocabulary": 0})
    return out


def emerging_themes(con: sqlite3.Connection, as_of_week: str | None, filters: Filters, min_recent: int = MIN_SUPPORT,
                    only_new: bool = False, limit: int = 10) -> dict[str, Any]:
    q = Q(con)
    sc = scope(q, filters)
    as_of = as_of_or_meta(con, as_of_week)
    if not as_of:
        raise QueryError("no as_of_week available (meta.as_of_week missing)")
    source = "precomputed"
    rows = _emerging_precomputed(q, as_of) if filters.is_empty() else []
    if not rows:
        source = "recomputed"
        rows = _emerging_local(q, filters, as_of)
    n_tested = sum(1 for r in rows if (r["n_recent"] or 0) >= MIN_SUPPORT)
    status_counts: dict[str, int] = {}
    for r in rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
    ranked = [r for r in rows if (r["n_recent"] or 0) >= max(min_recent, MIN_SUPPORT) and r["status"] in RANKED_STATUSES
              and (not only_new or r["status"] == "new")]
    ranked.sort(key=lambda r: (-(r["emerging_score"] or 0), r["theme_id"]))
    ranked = ranked[:limit]
    recent_weeks = [week_shift(as_of, -i) for i in range(3, -1, -1)]
    if ranked:
        where, params = filters_where(filters)
        ids = [r["theme_id"] for r in ranked]
        recent: dict[str, list[str]] = {}
        for r in q.calls(f"""
            SELECT tc.theme_id, tc.call_id FROM v_theme_calls tc JOIN calls c ON c.call_id = tc.call_id
            WHERE tc.theme_id IN ({_placeholders(ids)}) AND c.week IN ({_placeholders(recent_weeks)}) AND {where}
            ORDER BY c.date DESC, tc.call_id""", [*ids, *recent_weeks, *params]):
            recent.setdefault(r["theme_id"], []).append(r["call_id"])
        for r in ranked:
            r["call_ids_recent"] = recent.get(r["theme_id"], [])[:20]
    fading = sorted((r for r in rows if r["status"] == "fading"), key=lambda r: r["z"] or 0)[:3]
    data = {"as_of_week": as_of, "recent_weeks": recent_weeks, "source": source, "n_tested": n_tested,
            "expected_false_positives": round(n_tested * FALSE_POSITIVE_RATE, 2), "status_counts": status_counts,
            "fading": [{k: r[k] for k in ("theme_id", "name", "status", "n_recent", "expected_recent", "z")} for r in fading],
            "min_recent": min_recent, "only_new": only_new}
    return q.result(rows=ranked, data=data, scope=sc)


def _group_topics_sql(group_by: str, where: str) -> tuple[str, str]:
    """(key expression, FROM/WHERE fragment with alias t for topics and c for calls) per group_by."""
    if group_by == "theme":
        return ("tm.effective_theme_id", f"FROM topics t JOIN calls c ON c.call_id = t.call_id "
                                         f"JOIN theme_members tm ON tm.topic_id = t.topic_id WHERE {where}")
    if group_by == "driver_category":
        return ("t.driver_category", f"FROM topics t JOIN calls c ON c.call_id = t.call_id WHERE {where}")
    if group_by == "reason":
        return ("r.reason", f"FROM topics t JOIN calls c ON c.call_id = t.call_id "
                            f"JOIN call_reasons r ON r.call_id = t.call_id WHERE {where}")
    raise QueryError(f"unknown group_by {group_by}")


def sentiment_drivers(con: sqlite3.Connection, polarity: str, group_by: str, filters: Filters, limit: int = 10) -> dict[str, Any]:
    if polarity not in ("negative", "positive"):
        raise QueryError("polarity must be negative or positive")
    q = Q(con)
    sc = scope(q, filters)
    where, params = filters_where(filters)
    total = sc["n_calls_in_scope"]
    neg = polarity == "negative"
    key_expr, src = _group_topics_sql(group_by, where)
    if group_by == "theme":
        base = _theme_rows(q, filters, "neg_mass" if neg else "pos_mass", polarity, None, limit, as_of_or_meta(con, None))
        heads = [{"key": r["theme_id"], "name": r["name"], "n_calls": r["n_calls"], "share": _share(r["n_calls"], total),
                  "share_pct": _pct(r["n_calls"], total), "mass": r["neg_mass"] if neg else r["pos_mass"],
                  "mean_sentiment": r["mean_sentiment"], "problem_statement": r["problem_statement"],
                  "root_cause": r["root_cause"], "driver_category": r["driver_category"]} for r in base]
    else:
        mass = "SUM(CASE WHEN mn < 0 THEN -mn ELSE 0 END)" if neg else "SUM(CASE WHEN mx > 0 THEN mx ELSE 0 END)"
        agg = q.rows(f"""
            SELECT key, COUNT(*) AS n_calls, {mass} AS mass, AVG({'mn' if neg else 'mx'}) AS mean_sentiment
            FROM (SELECT {key_expr} AS key, t.call_id, MIN(t.sentiment) AS mn, MAX(t.sentiment) AS mx {src} GROUP BY key, t.call_id)
            GROUP BY key HAVING n_calls >= ? AND mass > 0 ORDER BY mass DESC, key LIMIT ?""", [*params, MIN_SUPPORT, limit])
        kind = "driver_categories" if group_by == "driver_category" else "contact_reasons"
        heads = [{"key": r["key"], "name": tx.labels(kind).get(r["key"], r["key"]), "n_calls": r["n_calls"],
                  "share": _share(r["n_calls"], total), "share_pct": _pct(r["n_calls"], total),
                  "mass": r["mass"], "mean_sentiment": round(r["mean_sentiment"], 2)} for r in agg]
    keys = [h["key"] for h in heads]
    sign = "t.sentiment < 0" if neg else "t.sentiment > 0"
    if keys:
        topics = q.calls(f"""
            SELECT {key_expr} AS key, t.topic_id, t.call_id, t.sentiment, t.driver_category, t.driver
            {src} AND {key_expr} IN ({_placeholders(keys)}) AND {sign}""", [*params, *keys])
        quotes = q.rows(f"""
            SELECT {key_expr} AS key, e.evidence_id, e.call_id, e.quote, t.sentiment
            {src.replace('FROM topics t', 'FROM evidence e JOIN topics t ON t.topic_id = e.topic_id')}
              AND e.verified = 1 AND {key_expr} IN ({_placeholders(keys)}) AND {sign}
            ORDER BY {'t.sentiment ASC' if neg else 't.sentiment DESC'}, c.date DESC, e.evidence_id""", [*params, *keys])
        by_key: dict[str, list[sqlite3.Row]] = {}
        for t in topics:
            by_key.setdefault(t["key"], []).append(t)
        quotes_by_key: dict[str, list[dict[str, Any]]] = {}
        for qr in quotes:
            lst = quotes_by_key.setdefault(qr["key"], [])
            if len(lst) < 2 and all(x["call_id"] != qr["call_id"] for x in lst):
                lst.append({"evidence_id": qr["evidence_id"], "call_id": qr["call_id"], "quote": qr["quote"], "sentiment": qr["sentiment"]})
        for h in heads:
            ts = by_key.get(h["key"], [])
            cats: dict[str, set[str]] = {}
            for t in ts:
                cats.setdefault(t["driver_category"], set()).add(t["call_id"])
            h["top_driver_categories"] = [{"driver_category": k, "n_calls": len(v)} for k, v in
                                          sorted(cats.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:3]]
            h["top_specific_drivers"] = _top_texts([(t["driver"] or "", t["call_id"]) for t in ts], 3)
            h["quotes"] = quotes_by_key.get(h["key"], [])
    data: dict[str, Any] = {"polarity": polarity, "group_by": group_by, "n_scope": total, "min_support": MIN_SUPPORT,
                            "mass_definition": "sum over calls of max(0, -strongest sentiment)" if neg else
                                               "sum over calls of max(0, strongest sentiment)"}
    if not neg:
        pms = q.rows(f"""
            SELECT pm.category, COUNT(DISTINCT pm.call_id) AS n_calls FROM positive_moments pm JOIN calls c ON c.call_id = pm.call_id
            WHERE pm.verified = 1 AND {where} GROUP BY pm.category ORDER BY n_calls DESC, pm.category""", params)
        # q.calls so these call ids join the result: on a complaint corpus the moments, not the
        # positive topics, are what a satisfaction claim actually rests on.
        ex = q.calls(f"""
            SELECT pm.category, pm.pm_id, pm.call_id, pm.quote, pm.what FROM positive_moments pm JOIN calls c ON c.call_id = pm.call_id
            WHERE pm.verified = 1 AND {where} ORDER BY c.date DESC""", params)
        examples: dict[str, list[dict[str, Any]]] = {}
        for r in ex:
            lst = examples.setdefault(r["category"], [])
            if len(lst) < 2:
                lst.append({"evidence_id": r["pm_id"], "call_id": r["call_id"], "quote": r["quote"], "what": r["what"]})
        data["positive_moments_by_category"] = [{"category": r["category"], "n_calls": r["n_calls"],
                                                 "share_pct": _pct(r["n_calls"], total),
                                                 "quotes": examples.get(r["category"], [])} for r in pms]
        data["corpus_note"] = "positive moments inside complaints (complaint corpus)"
    return q.result(rows=heads, data=data, scope=sc)


def breakdown(con: sqlite3.Connection, entity_type: str, entity_id: str | None, by: str, filters: Filters,
              min_n: int = MIN_SUPPORT) -> dict[str, Any]:
    if entity_type not in ENTITY_TYPES + ("all",):
        raise QueryError(f"unknown entity type {entity_type}")
    if entity_type != "all" and not entity_id:
        raise QueryError("entity id required unless type is 'all'")
    q = Q(con)
    sc = scope(q, filters)
    res = _breakdown_rows(q, filters, entity_type, entity_id, by, min_n=min_n)
    rid = resolve_theme_id(con, entity_id) if entity_type == "theme" and entity_id else entity_id
    data = {"entity": {"type": entity_type, "id": rid,
                       "name": _entity_name(con, entity_type, rid) if entity_type != "all" else "all calls"},
            "by": by, "overall_share": res["overall_share"], "overall_share_pct": round(100 * res["overall_share"], 1),
            "n_entity": res["n_entity"], "n_scope": res["n_scope"], "min_n": min_n, "min_slice": MIN_SLICE,
            "n_suppressed": sum(1 for r in res["rows"] if r["suppressed"])}
    return q.result(rows=res["rows"], data=data, scope=sc)


def compare(con: sqlite3.Connection, filters_a: Filters, filters_b: Filters, label_a: str = "A", label_b: str = "B",
            limit: int = 8) -> dict[str, Any]:
    q = Q(con)

    def _side(filters: Filters) -> tuple[int, dict[str, tuple[str, int]], dict[str, tuple[str, int]]]:
        where, params = filters_where(filters)
        n = len(q.calls(f"SELECT c.call_id FROM calls c WHERE {where}", params))
        themes = {r["id"]: (r["name"], r["n"]) for r in q.rows(f"""
            SELECT th.theme_id AS id, th.name, COUNT(DISTINCT tc.call_id) AS n FROM themes th
            JOIN v_theme_calls tc ON tc.theme_id = th.theme_id JOIN calls c ON c.call_id = tc.call_id
            WHERE th.status = 'active' AND {where} GROUP BY th.theme_id""", params)}
        labels = tx.labels("contact_reasons")
        reasons = {r["id"]: (labels.get(r["id"], r["id"]), r["n"]) for r in q.rows(f"""
            SELECT r.reason AS id, COUNT(DISTINCT r.call_id) AS n FROM call_reasons r JOIN calls c ON c.call_id = r.call_id
            WHERE {where} GROUP BY r.reason""", params)}
        return n, themes, reasons

    n_a, th_a, re_a = _side(filters_a)
    n_b, th_b, re_b = _side(filters_b)
    supported = n_a >= MIN_SLICE and n_b >= MIN_SLICE

    def _diff(a: dict[str, tuple[str, int]], b: dict[str, tuple[str, int]]) -> list[dict[str, Any]]:
        out = []
        for key in set(a) | set(b):
            name, na = a.get(key, (b.get(key, ("", 0))[0], 0))
            nb = b.get(key, ("", 0))[1]
            if max(na, nb) < MIN_SUPPORT:
                continue
            sa, sb = _share(na, n_a), _share(nb, n_b)
            out.append({"id": key, "name": name, "n_a": na, "share_a": sa, "n_b": nb, "share_b": sb,
                        "diff_pts": round(100 * (sa - sb), 1), "ci_a": list(wilson(na, n_a)), "ci_b": list(wilson(nb, n_b)),
                        "rate_ratio": round(sa / sb, 2) if sb else None, "suppressed": not supported})
        out.sort(key=lambda r: (-abs(r["diff_pts"]), r["id"]))
        return out[:limit]

    data = {"label_a": label_a, "label_b": label_b, "filters_a": filters_a.canonical(), "filters_b": filters_b.canonical(),
            "n_a": n_a, "n_b": n_b, "supported": supported, "min_slice": MIN_SLICE,
            "note": None if supported else f"both sides need at least {MIN_SLICE} calls; differences are shown but not rankable",
            "themes": _diff(th_a, th_b), "reasons": _diff(re_a, re_b)}
    return q.result(rows=data["themes"] + data["reasons"], data=data,
                    scope={"n_calls_in_scope": n_a + n_b, "date_from": None, "date_to": None})


def _pick_quotes(rows: list[sqlite3.Row], n: int, diverse: bool) -> list[dict[str, Any]]:
    seen: set[str] = set()
    candidates = []
    for r in rows:
        if r["call_id"] in seen:
            continue
        seen.add(r["call_id"])
        candidates.append(dict(r))
    if not diverse:
        return candidates[:n]
    chosen: list[dict[str, Any]] = []
    months: set[str] = set()
    products: set[str] = set()
    while candidates and len(chosen) < n:
        best = max(candidates, key=lambda c: (2 * (c["month"] not in months) + (c["product"] not in products), -candidates.index(c)))
        candidates.remove(best)
        chosen.append(best)
        months.add(best["month"])
        products.add(best["product"])
    return chosen


def get_quotes(con: sqlite3.Connection, entity_type: str, entity_id: str | None, call_ids: list[str] | None,
               filters: Filters, n: int = 5, polarity: str = "any", diverse: bool = True) -> dict[str, Any]:
    q = Q(con)
    sc = scope(q, filters)
    where, params = filters_where(filters)
    join, cond, cparams = "", "1=1", []
    if entity_type == "theme":
        join, cond, cparams = "JOIN theme_members tm ON tm.topic_id = t.topic_id", "tm.effective_theme_id = ?", [resolve_theme_id(con, entity_id or "")]
    elif entity_type == "reason":
        join, cond, cparams = "JOIN call_reasons r ON r.call_id = c.call_id", "r.reason = ?", [entity_id]
    elif entity_type == "driver_category":
        cond, cparams = "t.driver_category = ?", [entity_id]
    elif entity_type == "call_list":
        if not call_ids:
            raise QueryError("call_list needs call_ids")
        cond, cparams = f"c.call_id IN ({_placeholders(call_ids)})", list(call_ids)
    else:
        raise QueryError(f"unknown entity type {entity_type}")
    sign = {"negative": "AND t.sentiment < 0", "positive": "AND t.sentiment > 0", "any": ""}.get(polarity)
    if sign is None:
        raise QueryError("polarity must be negative, positive or any")
    order = {"negative": "t.sentiment ASC", "positive": "t.sentiment DESC", "any": "ABS(t.sentiment) DESC"}[polarity]
    pool = q.calls(f"""
        SELECT e.evidence_id, e.call_id, c.date, c.month, c.product, c.region, c.region_group, c.channel, c.segment,
               t.sentiment, e.quote, e.speaker, t.topic_label, t.driver, e.char_start, e.char_end, e.match_kind
        FROM evidence e JOIN topics t ON t.topic_id = e.topic_id JOIN calls c ON c.call_id = e.call_id {join}
        WHERE e.verified = 1 AND {cond} AND {where} {sign}
        ORDER BY {order}, c.date DESC, e.evidence_id""", [*cparams, *params])
    rows = _pick_quotes(pool, n, diverse)
    data = {"entity": {"type": entity_type, "id": entity_id, "call_ids": call_ids}, "polarity": polarity, "diverse": diverse,
            "n_pool_calls": len(q.call_ids), "n_pool_quotes": len(pool), "verified_only": True}
    return q.result(rows=rows, data=data, scope=sc)


def fts_query(query: str) -> str:
    """Sanitised FTS5 MATCH expression: each alphanumeric token quoted (prefix match), joined with OR."""
    tokens = [t.lower() for t in re.findall(r"[A-Za-z0-9]+", query or "") if len(t) >= 2]
    return " OR ".join(f'"{t}"*' for t in dict.fromkeys(tokens))


def search_calls(con: sqlite3.Connection, query: str, filters: Filters, limit: int = 10) -> dict[str, Any]:
    q = Q(con)
    sc = scope(q, filters)
    where, params = filters_where(filters)
    match = fts_query(query)
    data: dict[str, Any] = {"query": query, "match": match, "n_hits": 0}
    if not match:
        return q.result(rows=[], data=data, scope=sc)
    hits: dict[str, dict[str, Any]] = {}
    for r in q.calls(f"""
        SELECT c.call_id, c.date, c.product, snippet(calls_fts, 0, '[', ']', ' … ', 14) AS snippet, bm25(calls_fts) AS rank
        FROM calls_fts JOIN calls c ON c.rowid = calls_fts.rowid
        WHERE calls_fts MATCH ? AND {where} ORDER BY rank""", [match, *params]):
        hits[r["call_id"]] = {"call_id": r["call_id"], "date": r["date"], "product": r["product"], "snippet": r["snippet"],
                              "rank": r["rank"], "matched": ["text"]}
    for r in q.calls(f"""
        SELECT t.call_id, c.date, c.product, t.issue_statement, bm25(topics_fts) AS rank
        FROM topics_fts JOIN topics t ON t.rowid = topics_fts.rowid JOIN calls c ON c.call_id = t.call_id
        WHERE topics_fts MATCH ? AND {where} ORDER BY rank""", [match, *params]):
        h = hits.get(r["call_id"])
        if h is None:
            hits[r["call_id"]] = {"call_id": r["call_id"], "date": r["date"], "product": r["product"],
                                  "snippet": r["issue_statement"], "rank": r["rank"], "matched": ["topics"]}
        else:
            h["rank"] = min(h["rank"], r["rank"])
            h["matched"].append("topics")
    ranked = sorted(hits.values(), key=lambda h: (h["rank"], h["call_id"]))[:limit]
    data["n_hits"] = len(hits)
    if ranked:
        ids = [h["call_id"] for h in ranked]
        primary = {r["call_id"]: r["reason"] for r in q.rows(
            f"SELECT call_id, reason FROM call_reasons WHERE is_primary = 1 AND call_id IN ({_placeholders(ids)})", ids)}
        themes: dict[str, list[str]] = {}
        for r in q.rows(f"SELECT DISTINCT call_id, theme_id FROM v_theme_calls WHERE call_id IN ({_placeholders(ids)}) ORDER BY theme_id", ids):
            themes.setdefault(r["call_id"], []).append(r["theme_id"])
        for h in ranked:
            h["primary_reason"] = primary.get(h["call_id"])
            h["theme_ids"] = themes.get(h["call_id"], [])
            h["rank"] = round(h["rank"], 4)
    return q.result(rows=ranked, data=data, scope=sc)


def get_call(con: sqlite3.Connection, call_id: str) -> dict[str, Any]:
    q = Q(con)
    c = q.one("SELECT * FROM calls WHERE call_id = ?", [call_id])
    if c is None:
        raise NotFound(f"unknown call_id {call_id}")
    q.calls("SELECT call_id FROM calls WHERE call_id = ?", [call_id])
    ex = q.one("SELECT * FROM extractions WHERE call_id = ?", [call_id])
    reasons = [dict(r) for r in q.rows("SELECT reason, specific_reason, is_primary FROM call_reasons WHERE call_id = ? ORDER BY is_primary DESC, reason", [call_id])]
    products = [r["product"] for r in q.rows("SELECT product FROM call_products WHERE call_id = ? ORDER BY product", [call_id])]
    services = [r["service"] for r in q.rows("SELECT service FROM call_services WHERE call_id = ? ORDER BY service", [call_id])]
    topics = [dict(r) for r in q.rows("SELECT * FROM topics WHERE call_id = ? ORDER BY idx", [call_id])]
    evidence = q.rows("SELECT * FROM evidence WHERE call_id = ? ORDER BY evidence_id", [call_id])
    pms = [dict(r) for r in q.rows("SELECT * FROM positive_moments WHERE call_id = ? AND verified = 1 ORDER BY pm_id", [call_id])]
    members = {r["topic_id"]: dict(r) for r in q.rows("""
        SELECT tm.topic_id, tm.theme_id AS assigned_theme_id, tm.effective_theme_id AS theme_id, tm.confidence,
               th.name, th.status, th.polarity
        FROM theme_members tm JOIN topics t ON t.topic_id = tm.topic_id LEFT JOIN themes th ON th.theme_id = tm.effective_theme_id
        WHERE t.call_id = ?""", [call_id])}
    ev_by_topic: dict[str, list[dict[str, Any]]] = {}
    n_unverified = 0
    for e in evidence:
        if e["verified"]:
            ev_by_topic.setdefault(e["topic_id"], []).append(
                {k: e[k] for k in ("evidence_id", "quote", "char_start", "char_end", "speaker", "match_kind")})
        else:
            n_unverified += 1
    themes: dict[str, dict[str, Any]] = {}
    for t in topics:
        t["evidence"] = ev_by_topic.get(t["topic_id"], [])
        m = members.get(t["topic_id"])
        t["theme"] = {k: m[k] for k in ("theme_id", "assigned_theme_id", "name", "status", "polarity", "confidence")} if m else None
        if m and m["theme_id"]:
            themes.setdefault(m["theme_id"], {"theme_id": m["theme_id"], "name": m["name"], "status": m["status"],
                                              "polarity": m["polarity"], "topic_ids": []})["topic_ids"].append(t["topic_id"])
    metadata = {k: c[k] for k in ("call_id", "source", "shape", "date", "week", "month", "product", "product_raw", "sub_product_raw",
                                  "issue_raw", "sub_issue_raw", "region", "region_group", "channel", "segment", "company",
                                  "sampling_fraction", "n_turns")}
    extraction = None
    if ex is not None:
        extraction = {"status": ex["status"], "produced_by": ex["produced_by"], "model": ex["model"],
                      "prompt_version": ex["prompt_version"], "contact_reasons": reasons, "products": products,
                      "services": services, "customer_ask": ex["customer_ask"], "stated_reason": ex["stated_reason"],
                      "underlying_driver": ex["underlying_driver"], "reason_differs": bool(ex["reason_differs"]),
                      "overall_sentiment": ex["overall_sentiment"], "resolution_status": ex["resolution_status"],
                      "redaction_heavy": bool(ex["redaction_heavy"]), "summary": ex["summary"],
                      "quote_verify_rate": ex["quote_verify_rate"], "n_unverified_evidence": n_unverified}
    data = {"call_id": call_id, "text": c["text"], "metadata": metadata, "extraction": extraction, "topics": topics,
            "positive_moments": pms, "themes": list(themes.values())}
    return q.result(data=data, scope={"n_calls_in_scope": 1, "date_from": c["date"], "date_to": c["date"]})


# --- stored tool results -------------------------------------------------------------------------

def rerun_call_ids(con: sqlite3.Connection, statements: list[dict[str, Any]]) -> list[str]:
    """Re-execute the stored call-id statements of a tool result and return the distinct ids."""
    ids: dict[str, None] = {}
    for st in statements:
        if st.get("purpose") != "call_ids":
            continue
        for r in con.execute(st["sql"], list(st.get("params") or [])):
            ids.setdefault(r["call_id"])
    return list(ids)


def call_list(con: sqlite3.Connection, call_ids: list[str]) -> list[dict[str, Any]]:
    """Compact call rows (date, dimensions, primary reason, opening text) for a list of ids."""
    out: list[dict[str, Any]] = []
    for i in range(0, len(call_ids), 500):
        chunk = call_ids[i:i + 500]
        out.extend(dict(r) for r in con.execute(f"""
            SELECT c.call_id, c.date, c.product, c.region, c.region_group, c.channel, c.segment,
                   (SELECT reason FROM call_reasons r WHERE r.call_id = c.call_id AND r.is_primary = 1) AS primary_reason,
                   (SELECT overall_sentiment FROM extractions e WHERE e.call_id = c.call_id) AS overall_sentiment,
                   substr(c.text, 1, 200) AS snippet
            FROM calls c WHERE c.call_id IN ({_placeholders(chunk)})""", chunk))
    out.sort(key=lambda r: (r["date"], r["call_id"]), reverse=True)
    return out
