"""Server-side verification of an agent answer: recount from call ids, check numbers and quotes,
compute confidence. The model proposes; this module decides what is shown as verified."""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import date, timedelta
from typing import Any, Iterable

from voc.schemas.answer import Answer, Chart, Confidence, Quote, VerifiedAnswer, VerifiedClaim

SHARE_TOLERANCE = 0.5
MAX_CALL_IDS_SHOWN = 50   # mirrors voc.agent.tools.MAX_CALL_IDS_SHOWN


# --- helpers ------------------------------------------------------------------------------

def _norm(s: str) -> str:
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def _numbers_in(obj: Any, out: set[float] | None = None) -> set[float]:
    """Every numeric value inside a tool result (rows, data, scope)."""
    out = set() if out is None else out
    if isinstance(obj, bool):
        return out
    if isinstance(obj, (int, float)):
        out.add(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            _numbers_in(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _numbers_in(v, out)
    return out


def _number_matches(value: float, pool: set[float]) -> tuple[bool, float | None]:
    """A model number matches a tool number exactly (counts), within 0.5 points (shares as %),
    or as the percent form of a fraction. Returns (ok, closest tool number)."""
    if not pool:
        return False, None
    best = min(pool, key=lambda x: min(abs(x - value), abs(x * 100 - value), abs(x - value / 100)))
    for x in pool:
        if abs(x - value) < 1e-9:
            return True, x
        if abs(x - value) <= SHARE_TOLERANCE and not float(value).is_integer():
            return True, x
        if abs(x * 100 - value) <= SHARE_TOLERANCE:
            return True, x
        if abs(x - value / 100) <= SHARE_TOLERANCE / 100:
            return True, x
    return False, best


def full_call_ids(con: sqlite3.Connection, result_id: str, envelope: dict[str, Any] | None,
                  qhash: str = "") -> list[str]:
    """Full call-id list of a tool result: the persisted record first, the envelope as fallback.

    Result ids restart at r1 for every question, so the lookup is scoped by qhash. A row belonging
    to another question is never used: recounting a claim against a stranger's calls is worse than
    reporting the claim as unsupported.
    """
    try:
        row = con.execute("SELECT call_ids FROM tool_results WHERE result_id = ? AND qhash = ?",
                          (result_id, qhash)).fetchone() if qhash else None
    except sqlite3.Error:
        row = None
    if row and row["call_ids"]:
        try:
            ids = json.loads(row["call_ids"])
            if isinstance(ids, list):
                return [str(x) for x in ids]
        except json.JSONDecodeError:
            pass
    if envelope:
        if isinstance(envelope.get("call_ids_full"), list):
            return [str(x) for x in envelope["call_ids_full"]]
        ids = envelope.get("call_ids")
        # An envelope shows at most MAX_CALL_IDS_SHOWN ids. Recounting a truncated list would
        # report a confident wrong number, so treat it as no evidence at all.
        if isinstance(ids, list) and int(envelope.get("n_call_ids") or len(ids)) <= len(ids):
            return [str(x) for x in ids]
    return []


def ids_for_themes(con: sqlite3.Connection, call_ids: list[str], theme_ids: list[str]) -> list[str]:
    """The calls in `call_ids` that belong to any of `theme_ids`, order preserved."""
    if not call_ids or not theme_ids:
        return []
    keep: set[str] = set()
    for i in range(0, len(call_ids), 500):
        chunk = call_ids[i:i + 500]
        marks, tmarks = ",".join("?" * len(chunk)), ",".join("?" * len(theme_ids))
        try:
            rows = con.execute(f"SELECT DISTINCT call_id FROM v_theme_calls "
                               f"WHERE call_id IN ({marks}) AND theme_id IN ({tmarks})",
                               [*chunk, *theme_ids]).fetchall()
        except sqlite3.Error:
            return []
        keep.update(r[0] for r in rows)
    return [i for i in call_ids if i in keep]


def _week_start(week: str) -> date:
    y, w = week.split("-W")
    return date.fromisocalendar(int(y), int(w), 1)


def call_facts(con: sqlite3.Connection, call_ids: Iterable[str], as_of_week: str) -> dict[str, Any]:
    ids = list(dict.fromkeys(call_ids))
    if not ids:
        return {"n": 0, "months": 0, "products": 0, "states": 0, "recent_share": 0.0, "evidence_share": 0.0}
    months, products, states, recent, with_evidence = set(), set(), set(), 0, 0
    try:
        recent_from = (_week_start(as_of_week) - timedelta(weeks=3)).isoformat()
    except (ValueError, AttributeError):
        recent_from = "9999-12-31"
    for i in range(0, len(ids), 500):
        chunk = ids[i:i + 500]
        marks = ",".join("?" * len(chunk))
        rows = con.execute(
            f"SELECT c.call_id, c.month, c.product, c.region, c.date, "
            f"EXISTS(SELECT 1 FROM evidence e WHERE e.call_id = c.call_id AND e.verified = 1) AS has_ev "
            f"FROM calls c WHERE c.call_id IN ({marks})", chunk).fetchall()
        for r in rows:
            months.add(r["month"])
            products.add(r["product"])
            if r["region"] and r["region"] != "unknown":
                states.add(r["region"])
            if r["date"] >= recent_from:
                recent += 1
            if r["has_ev"]:
                with_evidence += 1
    n = len(ids)
    return {"n": n, "months": len(months), "products": len(products), "states": len(states),
            "recent_share": recent / n if n else 0.0, "evidence_share": with_evidence / n if n else 0.0}


def theme_status(con: sqlite3.Connection, theme_ids: Iterable[str], as_of_week: str) -> str | None:
    for tid in theme_ids:
        try:
            row = con.execute("SELECT status FROM emerging_scores WHERE entity_type='theme' AND entity_id=? AND as_of_week=?",
                              (tid, as_of_week)).fetchone()
        except sqlite3.Error:
            row = None
        if row and row["status"]:
            return row["status"]
    return None


def compute_confidence(facts: dict[str, Any], status: str | None = None) -> Confidence:
    """DESIGN section 9 tiers, computed from recounted call ids only."""
    n, months, products, states = facts["n"], facts["months"], facts["products"], facts["states"]
    recent_share, evidence_share = facts["recent_share"], facts["evidence_share"]
    concentrated = False
    if n == 0:
        tier = "unverified"
    elif n >= 50 and months >= 3 and (products >= 2 or states >= 5):
        tier = "broad_pattern"
    elif n >= 15 and months >= 2:
        tier = "moderate"
    elif n >= 15:
        tier, concentrated = "moderate", True
    elif n >= 5 and (status in ("emerging", "new") or recent_share >= 0.6):
        tier = "emerging_signal"
    else:
        tier = "anecdotal"
    thin = n > 0 and evidence_share < 0.5
    label = {"broad_pattern": "broad pattern", "moderate": "moderate", "emerging_signal": "emerging signal",
             "anecdotal": "anecdotal", "unverified": "not supported by retrieved data"}[tier]
    parts = [label]
    if n:
        parts.append(f"{n:,} call" + ("s" if n != 1 else ""))
    if tier == "emerging_signal":
        parts.append("recent weeks")
    elif n and tier != "anecdotal":
        parts.append(f"{months} month" + ("s" if months != 1 else ""))
        if products > 1:
            parts.append(f"{products} products")
        if states > 1 and tier == "broad_pattern":
            parts.append(f"{states} states")
    if concentrated:
        parts.append("concentrated in one month")
    badge = " · ".join(parts) + (" (thin evidence)" if thin else "")
    return Confidence(tier=tier, n=n, months=months, products=products, states=states,
                      recent_share=round(recent_share, 3), thin_evidence=thin, concentrated=concentrated, badge=badge)


def weakest(tiers: Iterable[str]) -> str:
    order = ["broad_pattern", "moderate", "emerging_signal", "anecdotal", "unverified"]
    worst = "broad_pattern"
    for t in tiers:
        if order.index(t) > order.index(worst):
            worst = t
    return worst


# --- verification -------------------------------------------------------------------------

def verify_quote(con: sqlite3.Connection, q: Quote) -> Quote | None:
    """Keep a quote only if a verified evidence row (or positive moment) of that call matches it."""
    target = _norm(q.quote)
    if not target:
        return None
    rows = con.execute("SELECT evidence_id AS id, quote FROM evidence WHERE call_id = ? AND verified = 1", (q.call_id,)).fetchall()
    rows += con.execute("SELECT pm_id AS id, quote FROM positive_moments WHERE call_id = ? AND verified = 1", (q.call_id,)).fetchall()
    for r in rows:
        stored = _norm(r["quote"])
        if stored == target or (len(target) >= 20 and (target in stored or stored in target)):
            return Quote(evidence_id=r["id"], call_id=q.call_id, quote=r["quote"], why=q.why)
    return None


def verify_answer(
    answer: Answer,
    results: dict[str, dict[str, Any]],
    con: sqlite3.Connection,
    *,
    as_of_week: str,
    data_version: str,
    mode: str,
    model: str,
    qhash: str = "",
    footnote: str = "",
    scope_note: str = "",
) -> VerifiedAnswer:
    report: dict[str, Any] = {"unverified_claims": [], "number_mismatches": [], "dropped_quotes": [],
                              "dropped_charts": [], "unlinked_numbers": []}
    claims: list[VerifiedClaim] = []
    for c in answer.claims:
        vc = VerifiedClaim(**c.model_dump())
        vc.model_n = c.n_calls
        known = [rid for rid in c.result_ids if rid in results]
        missing = [rid for rid in c.result_ids if rid not in results]
        if missing:
            vc.flags.append(f"unknown_result_ids:{','.join(missing)}")
        union: list[str] = []
        for rid in known:
            union.extend(full_call_ids(con, rid, results.get(rid), qhash))
        ids = list(dict.fromkeys(union))
        # A short list of call_ids is ambiguous: it can be a deliberate subset, or a handful of
        # examples for a claim about far more calls. The model's own n_calls settles it - a claim of
        # 312 calls citing 5 ids means "312, here are five of them". Narrowing those to 5 would make
        # verification understate the evidence, which is the one failure mode worse than silence
        # here: a 312-call finding would print as anecdotal and read as a thin corpus.
        examples = bool(c.call_ids) and bool(c.n_calls) and c.n_calls > len(c.call_ids)
        if c.call_ids and not examples and len(c.call_ids) < MAX_CALL_IDS_SHOWN:
            given = set(c.call_ids)
            narrowed = [i for i in ids if i in given]
            ids = narrowed if narrowed else ids
        elif examples and c.theme_ids:
            # The result may span several themes while the claim is about one, so count that theme
            # inside the result rather than the whole result. Only ever narrow: a recount coming out
            # ABOVE the model's own number means the claim is about a slice of the theme we cannot
            # rebuild from a theme_id alone - "older Americans hit this 2.26x more often" is 25 calls
            # inside a 312-call theme - and widening it there would overclaim, which is the failure
            # this recount exists to prevent. Those fall back to the cited examples and read thin,
            # which is the honest answer when the evidence set cannot be reconstructed.
            scoped = ids_for_themes(con, ids, c.theme_ids)
            if scoped and len(scoped) <= c.n_calls:
                ids = scoped
            else:
                given = set(c.call_ids)
                ids = [i for i in ids if i in given] or ids
        if not known or not ids:
            vc.verified = False
            vc.verified_n = 0
            vc.confidence = compute_confidence({"n": 0, "months": 0, "products": 0, "states": 0,
                                                "recent_share": 0.0, "evidence_share": 0.0})
            vc.flags.append("not_supported_by_retrieved_data")
            report["unverified_claims"].append(c.id)
        else:
            facts = call_facts(con, ids, as_of_week)
            vc.verified_n = facts["n"]
            vc.call_ids = ids[:50]
            vc.confidence = compute_confidence(facts, theme_status(con, c.theme_ids, as_of_week))
            if c.n_calls and c.n_calls != facts["n"]:
                vc.flags.append("n_calls_recounted")
                vc.corrections.append({"field": "n_calls", "model": c.n_calls, "server": facts["n"]})
        vc.n_calls = vc.verified_n
        pool: set[float] = set()
        for rid in known:
            _numbers_in({k: v for k, v in results[rid].items() if k in ("rows", "data", "scope", "summary_numbers")}, pool)
        for kn in c.key_numbers:
            src = results.get(kn.result_id)
            local_pool = _numbers_in({k: v for k, v in src.items() if k in ("rows", "data", "scope")}) if src else pool
            ok, closest = _number_matches(kn.value, local_pool)
            if not ok:
                vc.flags.append(f"number_not_from_tools:{kn.label}")
                vc.corrections.append({"field": kn.label, "model": kn.value, "server": closest})
                report["number_mismatches"].append({"claim": c.id, "label": kn.label, "model": kn.value, "closest": closest})
        claims.append(vc)

    quotes: list[Quote] = []
    for q in answer.quotes:
        vq = verify_quote(con, q)
        if vq is None:
            report["dropped_quotes"].append({"call_id": q.call_id, "quote": q.quote[:80]})
        else:
            quotes.append(vq)

    charts: list[Chart] = []
    for ch in answer.charts:
        src = results.get(ch.result_id)
        if src is None:
            report["dropped_charts"].append(ch.result_id)
            continue
        if ch.series_key and ch.series_key not in json.dumps(src, ensure_ascii=False, default=str):
            report["dropped_charts"].append(f"{ch.result_id}:{ch.series_key}")
            continue
        charts.append(ch)

    claim_numbers: set[float] = set()
    for c in answer.claims:
        claim_numbers.add(float(c.n_calls))
        for kn in c.key_numbers:
            claim_numbers.add(float(kn.value))
    for m in re.finditer(r"(\d[\d,]*\.?\d*)\s*(%|calls?\b)", answer.answer_markdown):
        try:
            v = float(m.group(1).replace(",", ""))
        except ValueError:
            continue
        if not any(abs(v - x) <= SHARE_TOLERANCE for x in claim_numbers):
            report["unlinked_numbers"].append(m.group(0))

    headline = [c for c in claims if c.headline] or claims
    tier = weakest(c.confidence.tier for c in headline if c.confidence) if headline else "unverified"
    lead = max(headline, key=lambda c: c.verified_n) if headline else None
    overall = lead.confidence if lead and lead.confidence and lead.confidence.tier == tier else \
        next((c.confidence for c in headline if c.confidence and c.confidence.tier == tier), compute_confidence({"n": 0, "months": 0, "products": 0, "states": 0, "recent_share": 0.0, "evidence_share": 0.0}))

    coverage = scope_note
    if lead and lead.verified_n:
        coverage = (coverage + "; " if coverage else "") + f"the headline finding rests on {lead.verified_n:,} calls"
    report["ok"] = not report["unverified_claims"] and not report["number_mismatches"]
    return VerifiedAnswer(
        answer_markdown=answer.answer_markdown, claims=claims, quotes=quotes, charts=charts,
        caveats=answer.caveats, followups=answer.followups, confidence=overall, coverage_line=coverage,
        footnote=footnote, validation=report, mode=mode, model=model, data_version=data_version, as_of_week=as_of_week,
    )


def text_only_answer(text: str) -> Answer:
    """Wrap a plain-text end_turn as a single unverified claim so something is always rendered."""
    return Answer(answer_markdown=text or "The agent returned no answer.",
                  claims=[{"id": "c1", "statement": (text or "no answer")[:200], "headline": True}],
                  caveats=["The agent did not submit a structured answer; nothing here is verified."])
