"""Verbatim quote verification: exact substring first, then a whitespace/punctuation-normalised
match mapped back to original offsets. No fuzzy matching anywhere (DESIGN decision 9)."""
from __future__ import annotations

from dataclasses import dataclass

from voc.schemas.call import CallRecord

# Unicode punctuation unified to ASCII before matching (case stays significant).
_CHAR_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "―": "-", "−": "-",
    "…": "...",
}


@dataclass(frozen=True)
class Match:
    char_start: int
    char_end: int        # exclusive
    match_kind: str      # exact | normalized


def normalize_with_map(text: str) -> tuple[str, list[int]]:
    """Normalised text plus, for every normalised character, the index of the original character."""
    out: list[str] = []
    index: list[int] = []
    in_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not in_space:
                out.append(" ")
                index.append(i)
                in_space = True
            continue
        in_space = False
        for rep in _CHAR_MAP.get(ch, ch):
            out.append(rep)
            index.append(i)
    return "".join(out), index


def normalize(text: str) -> str:
    return normalize_with_map(text)[0]


def find_quote(text: str, quote: str) -> Match | None:
    """Locate a quote inside text; exact first, normalised second, None otherwise."""
    q = quote.strip()
    if not q:
        return None
    idx = text.find(q)
    if idx >= 0:
        return Match(idx, idx + len(q), "exact")
    norm_text, index = normalize_with_map(text)
    norm_q = normalize(q).strip()
    if not norm_q:
        return None
    idx = norm_text.find(norm_q)
    if idx < 0:
        return None
    start = index[idx]
    end = index[idx + len(norm_q) - 1] + 1
    return Match(start, end, "normalized")


def speaker_for_span(call: CallRecord, start: int, end: int) -> str:
    """Who said the span: 'narrative' for complaints, 'customer' when the span lies inside a customer
    turn of a transcript, 'agent' otherwise."""
    if call.shape != "transcript" or not call.customer_char_ranges:
        return "narrative"
    for r_start, r_end in call.customer_char_ranges:
        if r_start <= start and end <= r_end:
            return "customer"
    return "agent"
