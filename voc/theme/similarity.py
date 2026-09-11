"""Text similarity behind a small interface, so embeddings could replace token overlap later."""
from __future__ import annotations

import re
from typing import Protocol

_TOKEN = re.compile(r"[a-z0-9]+")
# Function words that carry no meaning for theme-name overlap.
STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has", "have", "in", "is", "it",
    "its", "of", "on", "or", "that", "the", "their", "them", "they", "this", "to", "was", "were", "with",
    "after", "when", "not", "no", "my", "i", "me", "our", "we", "you", "your", "customer", "customers",
})


def tokens(text: str) -> frozenset[str]:
    """Lower-cased alphanumeric tokens without stop words."""
    return frozenset(t for t in _TOKEN.findall((text or "").lower()) if t not in STOP_WORDS)


def token_set_jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


class Similarity(Protocol):
    def score(self, a: str, b: str) -> float: ...


class TokenSetJaccard:
    def score(self, a: str, b: str) -> float:
        return token_set_jaccard(a, b)


def default_similarity() -> Similarity:
    return TokenSetJaccard()
