"""Per-call extraction contract: strict API schema, pydantic model and lenient normaliser."""
from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, field_validator

from voc.taxonomy import loader as tx

SCHEMA_VERSION = "1"

# Bounds enforced after parsing (kept out of the API schema for portability).
MAX_REASONS, MAX_PRODUCTS, MAX_SERVICES, MAX_TOPICS, MAX_EVIDENCE, MAX_POSITIVE = 3, 3, 3, 5, 3, 3
QUOTE_MIN, QUOTE_MAX = 8, 300
LIMITS = {"specific_reason": 160, "issue_statement": 220, "driver": 200, "topic_label": 60,
          "summary": 200, "stated_reason": 160, "underlying_driver": 200, "what": 160}

SENTIMENTS = [-2, -1, 0, 1, 2]
SPEAKERS = tx.codes("speaker")
OUTCOMES = tx.codes("outcome")
RESOLUTIONS = tx.codes("resolution_status")
ASKS = tx.codes("customer_asks")
POSITIVE_CATEGORIES = tx.codes("positive_moment_categories")


class ContactReason(BaseModel):
    reason: str
    specific_reason: str
    is_primary: bool

    @field_validator("reason")
    @classmethod
    def _reason(cls, v: str) -> str:
        if v not in tx.codes("contact_reasons"):
            raise ValueError(f"unknown reason {v}")
        return v


class Evidence(BaseModel):
    quote: str
    speaker: str


class Topic(BaseModel):
    topic_label: str
    issue_statement: str
    product: str
    sentiment: int
    driver_category: str
    driver: str
    outcome: str
    evidence: list[Evidence]

    @field_validator("product")
    @classmethod
    def _product(cls, v: str) -> str:
        if v not in tx.codes("products"):
            raise ValueError(f"unknown product {v}")
        return v

    @field_validator("driver_category")
    @classmethod
    def _driver(cls, v: str) -> str:
        if v not in tx.codes("driver_categories"):
            raise ValueError(f"unknown driver_category {v}")
        return v


class PositiveMoment(BaseModel):
    what: str
    category: str
    quote: str
    speaker: str


class Extraction(BaseModel):
    contact_reasons: list[ContactReason]
    products: list[str]
    services: list[str]
    customer_ask: str
    stated_reason: str
    underlying_driver: str
    reason_differs: bool
    topics: list[Topic]
    overall_sentiment: int
    resolution_status: str
    positive_moments: list[PositiveMoment]
    redaction_heavy: bool
    summary: str

    @property
    def primary_reason(self) -> str:
        for r in self.contact_reasons:
            if r.is_primary:
                return r.reason
        return self.contact_reasons[0].reason


def _enum(values: list) -> dict:
    return {"type": "string", "enum": values}


def build_api_schema() -> dict:
    """Strict JSON schema for output_config.format (type/enum/required/additionalProperties/items only)."""
    evidence = {"type": "object", "additionalProperties": False, "required": ["quote", "speaker"],
                "properties": {"quote": {"type": "string"}, "speaker": _enum(SPEAKERS)}}
    topic = {"type": "object", "additionalProperties": False,
             "required": ["topic_label", "issue_statement", "product", "sentiment", "driver_category",
                          "driver", "outcome", "evidence"],
             "properties": {"topic_label": {"type": "string"}, "issue_statement": {"type": "string"},
                            "product": _enum(tx.codes("products")),
                            "sentiment": {"type": "integer", "enum": SENTIMENTS},
                            "driver_category": _enum(tx.codes("driver_categories")),
                            "driver": {"type": "string"}, "outcome": _enum(OUTCOMES),
                            "evidence": {"type": "array", "items": evidence}}}
    reason = {"type": "object", "additionalProperties": False,
              "required": ["reason", "specific_reason", "is_primary"],
              "properties": {"reason": _enum(tx.codes("contact_reasons")),
                             "specific_reason": {"type": "string"}, "is_primary": {"type": "boolean"}}}
    positive = {"type": "object", "additionalProperties": False,
                "required": ["what", "category", "quote", "speaker"],
                "properties": {"what": {"type": "string"}, "category": _enum(POSITIVE_CATEGORIES),
                               "quote": {"type": "string"}, "speaker": _enum(SPEAKERS)}}
    return {
        "type": "object", "additionalProperties": False,
        "required": ["contact_reasons", "products", "services", "customer_ask", "stated_reason",
                     "underlying_driver", "reason_differs", "topics", "overall_sentiment",
                     "resolution_status", "positive_moments", "redaction_heavy", "summary"],
        "properties": {
            "contact_reasons": {"type": "array", "items": reason},
            "products": {"type": "array", "items": _enum(tx.codes("products"))},
            "services": {"type": "array", "items": _enum(tx.codes("services"))},
            "customer_ask": _enum(ASKS),
            "stated_reason": {"type": "string"},
            "underlying_driver": {"type": "string"},
            "reason_differs": {"type": "boolean"},
            "topics": {"type": "array", "items": topic},
            "overall_sentiment": {"type": "integer", "enum": SENTIMENTS},
            "resolution_status": _enum(RESOLUTIONS),
            "positive_moments": {"type": "array", "items": positive},
            "redaction_heavy": {"type": "boolean"},
            "summary": {"type": "string"},
        },
    }


EXTRACTION_API_SCHEMA = build_api_schema()


class ExtractionError(ValueError):
    """Structural problem that cannot be repaired leniently."""


def _norm_key(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


def _clip(s: Any, limit: int, flags: list[str], field: str) -> str:
    s = "" if s is None else str(s).strip()
    if len(s) > limit:
        flags.append(f"clipped:{field}")
        s = s[:limit].rstrip()
    return s


# Near-miss values worth keeping rather than dropping to an abstention: a topic outcome has no
# "partially resolved", but the customer did say the problem is not fully fixed.
ENUM_ALIASES = {"partially_resolved": "unresolved", "partly_resolved": "unresolved",
                "not_resolved": "unresolved", "resolved_partially": "unresolved"}


def _coerce_enum(value: Any, allowed: list[str], fallback: str, flags: list[str], field: str) -> str:
    v = str(value or "").strip()
    if v in allowed:
        return v
    alias = ENUM_ALIASES.get(v)
    if alias in allowed:
        flags.append(f"aliased_enum:{field}={v[:40]}")
        return alias
    flags.append(f"invalid_enum:{field}={v[:40]}")
    return fallback


def _coerce_sentiment(value: Any, flags: list[str], field: str) -> int:
    try:
        v = int(round(float(value)))
    except (TypeError, ValueError):
        flags.append(f"invalid_sentiment:{field}")
        return -1
    if v < -2 or v > 2:
        flags.append(f"clamped_sentiment:{field}")
        v = max(-2, min(2, v))
    return v


def normalize_extraction(raw: dict) -> tuple[Extraction, list[str]]:
    """Repair bound and enum violations where a sensible repair exists; raise ExtractionError otherwise.
    Returns the validated Extraction and the list of repair flags."""
    flags: list[str] = []
    if not isinstance(raw, dict):
        raise ExtractionError("extraction is not an object")
    out: dict[str, Any] = {}

    # contact reasons: dedupe, cap, exactly one primary
    reasons, seen = [], set()
    for r in raw.get("contact_reasons") or []:
        if not isinstance(r, dict):
            continue
        code = _coerce_enum(r.get("reason"), tx.codes("contact_reasons"), "other_or_unclear", flags, "reason")
        if code in seen:
            flags.append("duplicate_reason")
            continue
        seen.add(code)
        reasons.append({"reason": code, "specific_reason": _clip(r.get("specific_reason"), LIMITS["specific_reason"], flags, "specific_reason"),
                        "is_primary": bool(r.get("is_primary"))})
    if not reasons:
        raise ExtractionError("no contact_reasons")
    if len(reasons) > MAX_REASONS:
        flags.append("too_many_reasons")
        reasons = reasons[:MAX_REASONS]
    primaries = [r for r in reasons if r["is_primary"]]
    if len(primaries) != 1:
        flags.append("no_primary" if not primaries else "multiple_primary")
        for i, r in enumerate(reasons):
            r["is_primary"] = (i == 0) if not primaries else (r is primaries[0])
    out["contact_reasons"] = reasons

    def _list_enum(field: str, kind: str, cap: int, fallback: str | None) -> list[str]:
        vals: list[str] = []
        for v in raw.get(field) or []:
            code = _coerce_enum(v, tx.codes(kind), fallback or "", flags, field)
            if code and code not in vals:
                vals.append(code)
        if len(vals) > cap:
            flags.append(f"too_many_{field}")
            vals = vals[:cap]
        return vals

    out["products"] = _list_enum("products", "products", MAX_PRODUCTS, "other_or_unspecified") or ["other_or_unspecified"]
    if out["products"] == ["other_or_unspecified"] and not raw.get("products"):
        flags.append("no_products")
    out["services"] = _list_enum("services", "services", MAX_SERVICES, None)
    out["customer_ask"] = _coerce_enum(raw.get("customer_ask"), ASKS, "other", flags, "customer_ask")
    out["stated_reason"] = _clip(raw.get("stated_reason"), LIMITS["stated_reason"], flags, "stated_reason")
    out["underlying_driver"] = _clip(raw.get("underlying_driver"), LIMITS["underlying_driver"], flags, "underlying_driver")
    out["reason_differs"] = bool(raw.get("reason_differs"))

    topics, seen_topics = [], set()
    for t in raw.get("topics") or []:
        if not isinstance(t, dict):
            continue
        issue = _clip(t.get("issue_statement"), LIMITS["issue_statement"], flags, "issue_statement")
        if not issue:
            flags.append("empty_issue_statement")
            continue
        key = _norm_key(issue)
        if key in seen_topics:
            flags.append("duplicate_topic")
            continue
        seen_topics.add(key)
        evidence = []
        for e in t.get("evidence") or []:
            if not isinstance(e, dict):
                continue
            q = str(e.get("quote") or "").strip()
            if len(q) < QUOTE_MIN:
                flags.append("short_quote_dropped")
                continue
            if len(q) > QUOTE_MAX:
                flags.append("quote_clipped")
                q = q[:QUOTE_MAX].rstrip()
            evidence.append({"quote": q, "speaker": _coerce_enum(e.get("speaker"), SPEAKERS, "narrative", flags, "speaker")})
        if len(evidence) > MAX_EVIDENCE:
            flags.append("too_many_evidence")
            evidence = evidence[:MAX_EVIDENCE]
        if not evidence:
            flags.append("topic_without_evidence")
        topics.append({
            "topic_label": _clip(t.get("topic_label"), LIMITS["topic_label"], flags, "topic_label") or issue[:LIMITS["topic_label"]],
            "issue_statement": issue,
            "product": _coerce_enum(t.get("product"), tx.codes("products"), "other_or_unspecified", flags, "topic.product"),
            "sentiment": _coerce_sentiment(t.get("sentiment"), flags, "topic.sentiment"),
            "driver_category": _coerce_enum(t.get("driver_category"), tx.codes("driver_categories"), "other_or_unclear", flags, "driver_category"),
            "driver": _clip(t.get("driver"), LIMITS["driver"], flags, "driver"),
            "outcome": _coerce_enum(t.get("outcome"), OUTCOMES, "unknown", flags, "outcome"),
            "evidence": evidence,
        })
    if not topics:
        raise ExtractionError("no topics")
    if len(topics) > MAX_TOPICS:
        flags.append("too_many_topics")
        topics = topics[:MAX_TOPICS]
    out["topics"] = topics

    out["overall_sentiment"] = _coerce_sentiment(raw.get("overall_sentiment"), flags, "overall_sentiment")
    out["resolution_status"] = _coerce_enum(raw.get("resolution_status"), RESOLUTIONS, "unknown", flags, "resolution_status")

    positives = []
    for p in raw.get("positive_moments") or []:
        if not isinstance(p, dict):
            continue
        q = str(p.get("quote") or "").strip()
        if len(q) < QUOTE_MIN:
            flags.append("short_positive_quote_dropped")
            continue
        positives.append({"what": _clip(p.get("what"), LIMITS["what"], flags, "what"),
                          "category": _coerce_enum(p.get("category"), POSITIVE_CATEGORIES, "other", flags, "positive.category"),
                          "quote": q[:QUOTE_MAX], "speaker": _coerce_enum(p.get("speaker"), SPEAKERS, "narrative", flags, "positive.speaker")})
    if len(positives) > MAX_POSITIVE:
        flags.append("too_many_positive_moments")
        positives = positives[:MAX_POSITIVE]
    out["positive_moments"] = positives
    out["redaction_heavy"] = bool(raw.get("redaction_heavy"))
    out["summary"] = _clip(raw.get("summary"), LIMITS["summary"], flags, "summary")

    return Extraction.model_validate(out), flags
