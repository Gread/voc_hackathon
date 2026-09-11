"""Turns a raw model response (API, agent or fake) into one validated extractions.jsonl row:
schema + bounds via normalize_extraction, verbatim quote verification, speaker relabelling and
consistency flags. Nothing here is fatal except a response that cannot be repaired."""
from __future__ import annotations

import re
from typing import Any

from pydantic import ValidationError

from voc.extract.prompt import PROMPT_VERSION
from voc.extract.verify_quotes import find_quote, speaker_for_span
from voc.schemas.call import CallRecord
from voc.schemas.extraction import SCHEMA_VERSION, ExtractionError, normalize_extraction

REDACTION_TOKEN = re.compile(r"X{2,}(?:/X{2,})*")
HEAVY_REDACTION_SHARE = 0.15


def redaction_share(text: str) -> float:
    """Share of whitespace-separated tokens that are CFPB redactions."""
    tokens = text.split()
    if not tokens:
        return 0.0
    return sum(1 for t in tokens if REDACTION_TOKEN.fullmatch(t.strip(".,;:!?()\"'"))) / len(tokens)


def _verify(item: dict[str, Any], call: CallRecord, relabel_flags: list[str]) -> None:
    """Add offsets and verification fields to an evidence or positive-moment dict in place."""
    m = find_quote(call.text, item["quote"])
    if m is None:
        item.update({"char_start": None, "char_end": None, "verified": 0, "match_kind": None})
    else:
        item.update({"char_start": m.char_start, "char_end": m.char_end, "verified": 1, "match_kind": m.match_kind})
    if call.shape != "transcript":
        item["speaker"] = "narrative"
    elif m is not None:
        actual = speaker_for_span(call, m.char_start, m.char_end)
        if item["speaker"] != actual:
            relabel_flags.append("speaker_relabelled")
            item["speaker"] = actual


def make_row(call: CallRecord, *, status: str, produced_by: str | None, model: str | None,
             extracted_at: str | None, error: str | None = None, flags: list[str] | None = None,
             quote_verify_rate: float | None = None, extraction: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"call_id": call.call_id, "status": status, "error": error, "produced_by": produced_by,
            "model": model, "prompt_version": PROMPT_VERSION, "schema_version": SCHEMA_VERSION,
            "extracted_at": extracted_at, "flags": sorted(set(flags or [])),
            "quote_verify_rate": quote_verify_rate, "extraction": extraction}


def validate_response(call: CallRecord, response: Any, *, produced_by: str | None, model: str | None,
                      extracted_at: str | None, extra_flags: list[str] | None = None) -> dict[str, Any]:
    """Validate one raw Extraction JSON for a call. Never raises."""
    try:
        ext, flags = normalize_extraction(response)
    except (ExtractionError, ValidationError, TypeError, AttributeError) as exc:
        msg = str(exc).splitlines()[0][:300]
        return make_row(call, status="error", produced_by=produced_by, model=model,
                        extracted_at=extracted_at, error=f"invalid extraction: {msg}", flags=extra_flags)
    flags = list(flags) + list(extra_flags or [])
    data = ext.model_dump()

    n_quotes = n_verified = 0
    for topic in data["topics"]:
        for ev in topic["evidence"]:
            _verify(ev, call, flags)
            n_quotes += 1
            n_verified += ev["verified"]
        topic["evidence_ok"] = int(any(ev["verified"] for ev in topic["evidence"]))
    for pm in data["positive_moments"]:
        _verify(pm, call, flags)
        n_quotes += 1
        n_verified += pm["verified"]
    rate = (n_verified / n_quotes) if n_quotes else 0.0

    primary_topic = data["topics"][0]
    if abs(data["overall_sentiment"] - primary_topic["sentiment"]) > 1:
        flags.append("sentiment_inconsistent")
    if call.product not in data["products"]:
        flags.append("product_mismatch")
    if n_verified == 0:
        flags.append("no_verified_quotes")
    if data["redaction_heavy"] or redaction_share(call.text) >= HEAVY_REDACTION_SHARE:
        flags.append("heavy_redaction")

    return make_row(call, status="ok", produced_by=produced_by, model=model, extracted_at=extracted_at,
                    flags=flags, quote_verify_rate=round(rate, 4), extraction=data)
