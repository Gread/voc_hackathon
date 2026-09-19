"""Answer contract of the Q&A agent (submit_answer input) and the server-verified answer."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

ASK_PROMPT_VERSION = "ask-1.0"
CONFIDENCE_TIERS = ["broad_pattern", "moderate", "emerging_signal", "anecdotal", "unverified"]


class KeyNumber(BaseModel):
    label: str
    value: float
    result_id: str


class Claim(BaseModel):
    id: str
    statement: str
    headline: bool = False
    result_ids: list[str] = Field(default_factory=list)
    call_ids: list[str] = Field(default_factory=list)
    n_calls: int = 0
    theme_ids: list[str] = Field(default_factory=list)
    key_numbers: list[KeyNumber] = Field(default_factory=list)


class Quote(BaseModel):
    evidence_id: str
    call_id: str
    quote: str
    why: str = ""


class Chart(BaseModel):
    kind: str            # trend | bars
    title: str
    result_id: str
    series_key: str = ""


class Answer(BaseModel):
    answer_markdown: str
    claims: list[Claim]
    quotes: list[Quote] = Field(default_factory=list)
    charts: list[Chart] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    followups: list[str] = Field(default_factory=list)


class Confidence(BaseModel):
    tier: str
    n: int = 0
    months: int = 0
    products: int = 0
    states: int = 0
    recent_share: float = 0.0
    thin_evidence: bool = False
    concentrated: bool = False
    badge: str = ""


class VerifiedClaim(Claim):
    verified_n: int = 0
    model_n: int = 0
    confidence: Confidence | None = None
    flags: list[str] = Field(default_factory=list)
    verified: bool = True
    corrections: list[dict[str, Any]] = Field(default_factory=list)


class VerifiedAnswer(BaseModel):
    answer_markdown: str
    claims: list[VerifiedClaim]
    quotes: list[Quote]
    charts: list[Chart]
    caveats: list[str]
    followups: list[str]
    confidence: Confidence
    coverage_line: str = ""
    footnote: str = ""
    validation: dict[str, Any] = Field(default_factory=dict)
    mode: str = "live"              # live | recorded | templated
    model: str = ""
    data_version: str = ""
    as_of_week: str = ""


def _obj(required: list[str], props: dict[str, Any]) -> dict:
    return {"type": "object", "additionalProperties": False, "required": required, "properties": props}


ANSWER_API_SCHEMA = _obj(
    ["answer_markdown", "claims", "quotes", "charts", "caveats", "followups"],
    {
        "answer_markdown": {"type": "string"},
        "claims": {"type": "array", "items": _obj(
            ["id", "statement", "headline", "result_ids", "call_ids", "n_calls", "theme_ids", "key_numbers"],
            {"id": {"type": "string"}, "statement": {"type": "string"}, "headline": {"type": "boolean"},
             "result_ids": {"type": "array", "items": {"type": "string"}},
             "call_ids": {"type": "array", "items": {"type": "string"},
                          "description": "Calls backing this claim. List them all when the claim is "
                                         "about just these calls; when it is about more than you can "
                                         "list, give a few as examples and put the real total in "
                                         "n_calls. The server recounts either way."},
             "n_calls": {"type": "integer",
                         "description": "How many calls the claim is really about, which may be far "
                                        "more than the ids listed in call_ids."},
             "theme_ids": {"type": "array", "items": {"type": "string"}},
             "key_numbers": {"type": "array", "items": _obj(["label", "value", "result_id"], {
                 "label": {"type": "string"}, "value": {"type": "number"}, "result_id": {"type": "string"}})}})},
        "quotes": {"type": "array", "items": _obj(["evidence_id", "call_id", "quote", "why"], {
            "evidence_id": {"type": "string"}, "call_id": {"type": "string"},
            "quote": {"type": "string"}, "why": {"type": "string"}})},
        "charts": {"type": "array", "items": _obj(["kind", "title", "result_id", "series_key"], {
            "kind": {"type": "string", "enum": ["trend", "bars"]}, "title": {"type": "string"},
            "result_id": {"type": "string"}, "series_key": {"type": "string"}})},
        "caveats": {"type": "array", "items": {"type": "string"}},
        "followups": {"type": "array", "items": {"type": "string"}},
    },
)

BOUNDS = {"claims": (1, 6), "result_ids": 4, "call_ids": 50, "key_numbers": 4, "theme_ids": 3,
          "quotes": 8, "charts": 2, "caveats": 4, "followups": 3}


def clip_answer(answer: Answer) -> Answer:
    """Enforce the list bounds leniently (truncate, never reject)."""
    a = answer.model_copy(deep=True)
    a.claims = a.claims[: BOUNDS["claims"][1]]
    for c in a.claims:
        c.result_ids = c.result_ids[: BOUNDS["result_ids"]]
        c.call_ids = c.call_ids[: BOUNDS["call_ids"]]
        c.key_numbers = c.key_numbers[: BOUNDS["key_numbers"]]
        c.theme_ids = c.theme_ids[: BOUNDS["theme_ids"]]
    a.quotes = a.quotes[: BOUNDS["quotes"]]
    a.charts = a.charts[: BOUNDS["charts"]]
    a.caveats = a.caveats[: BOUNDS["caveats"]]
    a.followups = a.followups[: BOUNDS["followups"]]
    return a
