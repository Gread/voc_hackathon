"""Novel-vocabulary flag (DESIGN 7.3): a token first-seen index over issue statements. Deliberately simple."""
from __future__ import annotations

import re
from typing import Iterable, Mapping

from voc.analytics.emerging import week_add

MIN_COUNT = 5
LOOKBACK_WEEKS = 8
STOP_WORDS = frozenset("""
a an and are as at be been but by can did do for from had has have he her his i if in into is it its me my no
not of on or our she so that the their them then there they this to was we were what when where which who will
with would you your about after again all also am any because before being both could does doing down during each
few further get got he'd here how just more most off once only other out over own same should some such than
too under until up very via while why xxxx bank customer
""".split())
_TOKEN = re.compile(r"[a-z][a-z'-]{2,}")


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in STOP_WORDS]


def build_token_index(statements: Iterable[tuple[str, str]], min_count: int = MIN_COUNT) -> dict[str, str]:
    """(week, text) pairs -> {token: first week seen} for tokens with >= min_count occurrences overall."""
    first: dict[str, str] = {}
    counts: dict[str, int] = {}
    for week, text in statements:
        for tok in tokenize(text):
            counts[tok] = counts.get(tok, 0) + 1
            if tok not in first or week < first[tok]:
                first[tok] = week
    return {tok: wk for tok, wk in first.items() if counts[tok] >= min_count}


def novel_tokens(index: Mapping[str, str], as_of_week: str, lookback: int = LOOKBACK_WEEKS) -> set[str]:
    """Tokens whose first occurrence falls within the last `lookback` weeks before as_of_week (inclusive)."""
    start = week_add(as_of_week, -(lookback - 1))
    return {tok for tok, wk in index.items() if start <= wk <= as_of_week}


def has_novel_vocabulary(texts: Iterable[str], novel: set[str]) -> bool:
    if not novel:
        return False
    return any(tok in novel for text in texts for tok in tokenize(text))
