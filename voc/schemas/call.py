"""Normalised call record (data/calls.jsonl) and helpers shared by ingest and store."""
from __future__ import annotations

import hashlib
import unicodedata
from datetime import date as _date
from typing import Any, Literal

from pydantic import BaseModel, Field


def normalize_text(text: str) -> str:
    """The exact text the extractor sees: NFC, LF line endings, stripped ends."""
    return unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n")).strip()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iso_week(day: str) -> str:
    y, w, _ = _date.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


class CallRecord(BaseModel):
    call_id: str
    source: str = "cfpb"
    shape: Literal["narrative", "transcript"] = "narrative"
    date: str
    week: str
    month: str
    text: str
    text_sha: str
    product: str
    product_raw: str | None = None
    sub_product_raw: str | None = None
    issue_raw: str | None = None
    sub_issue_raw: str | None = None
    region: str = "unknown"
    region_group: str = "other"
    channel: str = "other"
    segment: str = "none"
    company: str = "unknown"
    sampling_fraction: float = 1.0
    n_turns: int | None = None
    customer_char_ranges: list[list[int]] | None = None
    meta: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def build(cls, **kw) -> "CallRecord":
        """Fill derived fields (week, month, text_sha) from date and text."""
        kw["text"] = normalize_text(kw["text"])
        kw.setdefault("text_sha", text_sha(kw["text"]))
        kw.setdefault("week", iso_week(kw["date"]))
        kw.setdefault("month", kw["date"][:7])
        return cls(**kw)
