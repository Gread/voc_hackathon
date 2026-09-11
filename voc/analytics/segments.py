"""Segment and period comparisons (DESIGN 7.5): share, lift, Wilson interval, minimum-support suppression."""
from __future__ import annotations

from typing import Iterable, Mapping, Set

from voc.analytics.stats import log_rate_ratio, wilson_interval

MIN_SLICE = 50
MIN_N = 5


def is_suppressed(n_calls: int, n_slice: int, min_slice: int = MIN_SLICE, min_n: int = MIN_N) -> bool:
    return n_slice < min_slice or n_calls < min_n


def segment_row(value: str, n_calls: int, n_slice: int, overall_share: float,
                min_slice: int = MIN_SLICE, min_n: int = MIN_N) -> dict:
    """One breakdown row; suppressed rows keep n/N only so the UI can blank the cell."""
    share = n_calls / n_slice if n_slice else 0.0
    suppressed = is_suppressed(n_calls, n_slice, min_slice, min_n)
    lo, hi = wilson_interval(n_calls, n_slice)
    return {
        "value": value, "n_calls": n_calls, "n_slice": n_slice,
        "share": None if suppressed else share,
        "ci_lo": None if suppressed else lo, "ci_hi": None if suppressed else hi,
        "lift": None if suppressed or overall_share <= 0 else share / overall_share,
        "suppressed": suppressed,
    }


def breakdown(entity_call_ids: Set[str], call_values: Mapping[str, str],
              min_slice: int = MIN_SLICE, min_n: int = MIN_N) -> tuple[float, list[dict]]:
    """Rows per dimension value. call_values maps every call in scope to its value for the dimension."""
    n_all = len(call_values)
    n_entity = sum(1 for c in entity_call_ids if c in call_values)
    overall_share = n_entity / n_all if n_all else 0.0
    slices: dict[str, int] = {}
    hits: dict[str, int] = {}
    for call_id, value in call_values.items():
        slices[value] = slices.get(value, 0) + 1
        if call_id in entity_call_ids:
            hits[value] = hits.get(value, 0) + 1
    rows = [segment_row(v, hits.get(v, 0), n, overall_share, min_slice, min_n) for v, n in slices.items()]
    rows.sort(key=lambda r: (-r["n_calls"], r["value"]))
    return overall_share, rows


def rate_ratio_vs_complement(n_v: int, n_slice: int, n_entity: int, n_all: int) -> tuple[float, float, float]:
    """Rate ratio of the slice against everything outside it (tool output / dev mode only)."""
    return log_rate_ratio(n_v, n_slice, n_entity - n_v, n_all - n_slice)


def compare_shares(n_a: int, N_a: int, n_b: int, N_b: int, min_slice: int = MIN_SLICE) -> dict:
    """Share difference between two slices with both intervals; supported only when both N >= min_slice."""
    share_a = n_a / N_a if N_a else 0.0
    share_b = n_b / N_b if N_b else 0.0
    rr, rr_lo, rr_hi = log_rate_ratio(n_a, N_a, n_b, N_b)
    return {
        "n_a": n_a, "n_b": n_b, "share_a": share_a, "share_b": share_b,
        "diff_pts": (share_a - share_b) * 100.0,
        "ci_a": wilson_interval(n_a, N_a), "ci_b": wilson_interval(n_b, N_b),
        "rate_ratio": rr, "rate_ratio_lo": rr_lo, "rate_ratio_hi": rr_hi,
        "supported": N_a >= min_slice and N_b >= min_slice,
    }


def call_values_from_rows(rows: Iterable[Mapping[str, object]], dim: str, call_key: str = "call_id") -> dict[str, str]:
    """Helper for callers holding call dicts: {call_id: str(row[dim])}."""
    return {str(r[call_key]): str(r[dim]) for r in rows}
