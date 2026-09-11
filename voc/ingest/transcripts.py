"""Multi-turn transcripts -> CUSTOMER/AGENT text with customer_char_ranges, merged into calls.jsonl."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterator

from voc.ingest.normalize import normalize_narrative, read_jsonl, write_jsonl_atomic
from voc.paths import Paths
from voc.schemas.call import CallRecord
from voc.taxonomy.loader import codes, map_product, map_region_group, map_segment

SPEAKER_PREFIX = {"customer": "CUSTOMER: ", "agent": "AGENT: "}
_WS_RE = re.compile(r"\s+")


def _turn_text(text: str) -> str:
    """One turn per line: newlines inside a turn collapse to spaces."""
    return _WS_RE.sub(" ", normalize_narrative(text)).strip()


def render_transcript(turns: list[dict[str, Any]]) -> tuple[str, int, list[list[int]]]:
    """Returns (text, n_turns, customer_char_ranges); ranges exclude the speaker prefix."""
    lines: list[str] = []
    ranges: list[list[int]] = []
    offset = 0
    for turn in turns:
        speaker = str(turn.get("speaker", "")).lower()
        prefix = SPEAKER_PREFIX.get(speaker, "AGENT: ")
        body = _turn_text(str(turn.get("text", "")))
        start = offset + len(prefix)
        if speaker == "customer":
            ranges.append([start, start + len(body)])
        lines.append(prefix + body)
        offset += len(prefix) + len(body) + 1  # newline
    return "\n".join(lines), len(lines), ranges


def _product_code(value: str | None) -> str:
    if value in codes("products"):
        return value  # already a taxonomy code
    return map_product(value)


def transcript_to_call(rec: dict[str, Any], *, source: str = "conv", company: str = "unknown") -> CallRecord:
    text, n_turns, ranges = render_transcript(rec.get("turns") or [])
    rid = str(rec["id"])
    state = str(rec.get("state") or "").strip().upper()
    call = CallRecord.build(
        call_id=rid if rid.startswith(f"{source}_") else f"{source}_{rid}",
        source=source,
        shape="transcript",
        date=str(rec["date"])[:10],
        text=text,
        product=_product_code(rec.get("product")),
        product_raw=rec.get("product"),
        region=state or "unknown",
        region_group=map_region_group(state),
        channel="phone",
        segment=map_segment(rec.get("tags")),
        company=rec.get("company") or company,
        sampling_fraction=float(rec.get("sampling_fraction", 1.0)),
        n_turns=n_turns,
        customer_char_ranges=ranges,
        meta={k: v for k, v in rec.items() if k not in {"id", "date", "turns", "product", "state", "tags"}},
    )
    if call.text != text:  # offsets are computed on the final text; rendering keeps it normalised
        raise ValueError(f"transcript {rid}: rendered text changed under normalisation")
    return call


def iter_transcripts(path: Path) -> Iterator[dict[str, Any]]:
    files = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    for file in files:
        yield from read_jsonl(file)


def merge_into_calls(paths: Paths, records: list[CallRecord]) -> int:
    """Append/replace by call_id into data/calls.jsonl, kept sorted by date then call_id."""
    existing = {row["call_id"]: row for row in read_jsonl(paths.calls)}
    for rec in records:
        existing[rec.call_id] = rec.model_dump()
    rows = sorted(existing.values(), key=lambda r: (r["date"], r["call_id"]))
    return write_jsonl_atomic(paths.calls, rows)


def ingest_transcripts(paths: Paths, path: Path, *, source: str = "conv", company: str = "unknown") -> int:
    records = [transcript_to_call(rec, source=source, company=company) for rec in iter_transcripts(path)]
    total = merge_into_calls(paths, records)
    print(f"transcripts: {len(records)} records from {path} -> {paths.calls} ({total} calls total)")
    return len(records)
