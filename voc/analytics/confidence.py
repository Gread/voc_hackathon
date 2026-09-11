"""Confidence tiers (DESIGN 9): computed by code from verified call ids, never emitted by the model."""
from __future__ import annotations

from typing import Iterable, Mapping

from voc.analytics.emerging import recent_weeks
from voc.schemas.answer import Confidence

THIN_EVIDENCE_CUT = 0.5
RECENT_SHARE_CUT = 0.6
EMERGING_STATUSES = ("emerging", "new")
TIER_LABELS = {"broad_pattern": "broad pattern", "moderate": "moderate", "emerging_signal": "emerging signal",
               "anecdotal": "anecdotal", "unverified": "unverified"}


def _plural(n: int, noun: str) -> str:
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def badge(tier_name: str, n: int, months: int, products: int, states: int, weeks: int | None = None,
          thin_evidence: bool = False) -> str:
    """Badge text, e.g. 'broad pattern . 312 calls . 11 months . 4 products . 27 states'."""
    if tier_name == "unverified":
        return "not supported by retrieved data"
    parts = [TIER_LABELS[tier_name], _plural(n, "call")]
    if tier_name == "broad_pattern":
        parts += [_plural(months, "month"), _plural(products, "product"), _plural(states, "state")]
    elif tier_name == "moderate":
        parts += [_plural(months, "month"), _plural(products, "product")]
    elif tier_name == "emerging_signal":
        parts.append(f"last {weeks} weeks" if weeks else "mostly in the last 4 weeks")
    text = " · ".join(parts)
    return f"{text} (thin evidence)" if thin_evidence else text


def tier(n: int, months: int, products: int, states: int, recent_share: float = 0.0,
         theme_status: str | None = None, evidence_share: float = 1.0, weeks: int | None = None) -> Confidence:
    """Tier rules in order: broad_pattern, moderate, emerging_signal, anecdotal, unverified."""
    concentrated = False
    if n <= 0:
        name = "unverified"
    elif n >= 50 and months >= 3 and (products >= 2 or states >= 5):
        name = "broad_pattern"
    elif n >= 15 and months >= 2:
        name = "moderate"
    elif n >= 15:
        name, concentrated = "moderate", True     # a spike, not a pattern
    elif n >= 5 and (theme_status in EMERGING_STATUSES or recent_share >= RECENT_SHARE_CUT):
        name = "emerging_signal"
    else:
        name = "anecdotal"
    thin = name != "unverified" and evidence_share < THIN_EVIDENCE_CUT
    return Confidence(tier=name, n=n, months=months, products=products, states=states, recent_share=recent_share,
                      thin_evidence=thin, concentrated=concentrated,
                      badge=badge(name, n, months, products, states, weeks, thin))


def confidence_from_calls(calls: Iterable[Mapping[str, object]], as_of_week: str | None = None,
                          theme_status: str | None = None, evidence_share: float = 1.0) -> Confidence:
    """Convenience: derive n, months, products, states and recent_share from call rows (month, product, region, week)."""
    rows = list(calls)
    ids = {str(r.get("call_id", i)) for i, r in enumerate(rows)}
    months = {r.get("month") for r in rows if r.get("month")}
    products = {r.get("product") for r in rows if r.get("product")}
    states = {r.get("region") for r in rows if r.get("region") and r.get("region") != "unknown"}
    recent_share = 0.0
    if as_of_week and rows:
        recent = set(recent_weeks(as_of_week))
        recent_share = sum(1 for r in rows if r.get("week") in recent) / len(rows)
    return tier(len(ids), len(months), len(products), len(states), recent_share, theme_status, evidence_share)


def weakest(confidences: Iterable[Confidence]) -> Confidence | None:
    """The weakest tier among several claims (answer-level badge)."""
    order = list(TIER_LABELS)
    items = list(confidences)
    return max(items, key=lambda c: order.index(c.tier)) if items else None
