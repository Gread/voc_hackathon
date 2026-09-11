"""Text normalisation for CFPB narratives, raw -> CallRecord mapping and small file helpers."""
from __future__ import annotations

import ast
import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Iterator

from voc.schemas.call import CallRecord, normalize_text
from voc.taxonomy.loader import map_channel, map_product, map_region_group, map_segment

_AMOUNT_RE = re.compile(r"\{\$([^}]*)\}")
_BLANK_RUN_RE = re.compile(r"\n[ \t]*\n(?:[ \t]*\n)+")
_WORD_RE = re.compile(r"\S+")


def unwrap_amounts(text: str) -> str:
    """CFPB writes amounts as {$300.00}; the braces are markup, not customer words."""
    return _AMOUNT_RE.sub(r"$\1", text)


def collapse_blank_lines(text: str) -> str:
    """Runs of blank lines become a single blank line."""
    return _BLANK_RUN_RE.sub("\n\n", text)


def decode_bytes_repr(text: str) -> str:
    """A small share of narratives reach the API as a Python bytes repr (b'...' with literal escapes),
    sometimes truncated mid-string by the regulator's length cap. Recover the real text; leave anything
    that still does not parse exactly as it came."""
    stripped = text.strip()
    if not stripped.startswith(("b'", 'b"')):
        return text
    quote = stripped[1]
    closed = stripped.endswith(quote) and len(stripped) >= 3
    escaped = any(chr(92) + ch in stripped for ch in "ntrx")
    # A long narrative opening with a capital is a repr; "b'cause they never called back" is a customer's
    # contraction. When in doubt leave the text alone: their exact words matter more than a tidy prefix.
    looks_like_a_narrative = len(stripped) >= 200 and stripped[2:3].isupper()
    if not (closed or escaped or looks_like_a_narrative):
        return text
    candidates = [stripped] if closed else []
    # A truncated repr has no closing quote (and may end mid-escape); close it and retry.
    candidates.append(stripped.rstrip(chr(92)) + quote)
    for candidate in candidates:
        try:
            value = ast.literal_eval(candidate)
        except (ValueError, SyntaxError):
            continue
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        if isinstance(value, str):
            return value
    return text


def normalize_narrative(text: str) -> str:
    """Exactly what the extractor sees: NFC + LF (normalize_text), unwrapped amounts, no blank-line runs."""
    return normalize_text(collapse_blank_lines(unwrap_amounts(normalize_text(decode_bytes_repr(text)))))


def word_count(text: str) -> int:
    return len(_WORD_RE.findall(text))


def company_slug(company: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", company.lower()).strip("_")
    return slug or "unknown"


def month_range(start: str, end: str) -> list[str]:
    """Inclusive list of YYYY-MM months."""
    y, m = (int(x) for x in start.split("-"))
    ey, em = (int(x) for x in end.split("-"))
    out: list[str] = []
    while (y, m) <= (ey, em):
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def next_month(month: str) -> str:
    y, m = (int(x) for x in month.split("-"))
    return f"{y + 1:04d}-01" if m == 12 else f"{y:04d}-{m + 1:02d}"


def month_bounds(month: str) -> tuple[str, str]:
    """(first day of month, first day of next month) as ISO dates."""
    return f"{month}-01", f"{next_month(month)}-01"


def complaint_id_of(src: dict[str, Any]) -> int | str:
    cid = src.get("complaint_id")
    return int(cid) if str(cid).isdigit() else str(cid)


def zip3_of(zip_code: Any) -> str | None:
    z = str(zip_code or "")[:3]
    return z if z.isdigit() else None


def date_of(src: dict[str, Any]) -> str:
    day = str(src.get("date_received") or "")[:10]
    date.fromisoformat(day)  # fail loudly on malformed input
    return day


def raw_to_call(src: dict[str, Any], sampling_fraction: float, company: str | None = None) -> CallRecord:
    """Map one CFPB _source dict to the record contract (DESIGN §2.4)."""
    cid = complaint_id_of(src)
    state = (src.get("state") or "").strip().upper()
    return CallRecord.build(
        call_id=f"cfpb_{cid}",
        source="cfpb",
        shape="narrative",
        date=date_of(src),
        text=normalize_narrative(src.get("complaint_what_happened") or ""),
        product=map_product(src.get("product"), src.get("sub_product")),
        product_raw=src.get("product"),
        sub_product_raw=src.get("sub_product"),
        issue_raw=src.get("issue"),
        sub_issue_raw=src.get("sub_issue"),
        region=state or "unknown",
        region_group=map_region_group(state),
        channel=map_channel(src.get("submitted_via")),
        segment=map_segment(src.get("tags")),
        company=company or src.get("company") or "unknown",
        sampling_fraction=sampling_fraction,
        meta={
            "complaint_id": cid,
            "company_response": src.get("company_response"),
            "timely": src.get("timely"),
            "zip3": zip3_of(src.get("zip_code")),
            "date_sent_to_company": str(src.get("date_sent_to_company") or "")[:10] or None,
        },
    )


# --- file helpers (atomic writes under data/) ------------------------------------------

def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def write_json_atomic(path: Path, obj: Any) -> None:
    write_text_atomic(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def write_jsonl_atomic(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    write_text_atomic(path, "".join(line + "\n" for line in lines))
    return len(lines)


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    if not path.exists():
        return
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))
