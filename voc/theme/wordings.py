"""Wordings (DESIGN 6.6): distinct member issue statements ordered greedily for maximal diversity.

Each next wording maximises the minimum token-set Jaccard distance to the ones already chosen; ties prefer a
different product, then a different month. The same selection backs theme_wordings, theme_detail.wordings and
get_quotes(diverse=true). Jaccard is implemented here so the module has no dependency on the theming lane.
"""
from __future__ import annotations

import re
from typing import Iterable, Mapping

MAX_WORDINGS = 12
_WORD = re.compile(r"[a-z0-9]+")


def normalize_statement(text: str) -> str:
    """Lowercase alphanumeric words joined by single spaces; the dedup key."""
    return " ".join(_WORD.findall(text.lower()))


def token_set(text: str) -> frozenset[str]:
    return frozenset(_WORD.findall(text.lower()))


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def jaccard_distance(a: frozenset[str], b: frozenset[str]) -> float:
    return 1.0 - jaccard(a, b)


def _sort_key(row: Mapping[str, object]) -> tuple:
    return (str(row.get("date") or ""), str(row.get("topic_id") or ""))


def distinct_wordings(candidates: Iterable[Mapping[str, object]]) -> list[dict]:
    """Deduplicate by normalised issue_statement, keeping the earliest (date, topic_id) occurrence."""
    seen: set[str] = set()
    out: list[dict] = []
    for row in sorted(candidates, key=_sort_key):
        key = normalize_statement(str(row.get("issue_statement") or ""))
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(dict(row))
    return out


def select_wordings(candidates: Iterable[Mapping[str, object]], max_n: int = MAX_WORDINGS) -> list[dict]:
    """Greedy maximal-diversity ordering of distinct wordings.

    Candidate rows carry issue_statement, topic_id, call_id, product and date (YYYY-MM-DD); the first pick is
    the earliest statement, so the exhibit starts where the problem was first voiced.
    """
    rows = distinct_wordings(candidates)
    if not rows:
        return []
    tokens = [token_set(str(r["issue_statement"])) for r in rows]
    chosen_idx = [0]
    chosen_products = {rows[0].get("product")}
    chosen_months = {str(rows[0].get("date") or "")[:7]}
    min_dist = [jaccard_distance(tokens[0], t) for t in tokens]
    remaining = set(range(1, len(rows)))
    while remaining and len(chosen_idx) < max_n:
        best = min(remaining, key=lambda i: (
            -round(min_dist[i], 6),
            0 if rows[i].get("product") not in chosen_products else 1,
            0 if str(rows[i].get("date") or "")[:7] not in chosen_months else 1,
            _sort_key(rows[i]),
        ))
        remaining.discard(best)
        chosen_idx.append(best)
        chosen_products.add(rows[best].get("product"))
        chosen_months.add(str(rows[best].get("date") or "")[:7])
        for i in remaining:
            d = jaccard_distance(tokens[best], tokens[i])
            if d < min_dist[i]:
                min_dist[i] = d
    return [rows[i] for i in chosen_idx]
