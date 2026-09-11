"""Step 0 of theming: deterministic bucketing (driver_category x polarity), ordering and batching."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from voc.paths import Paths
from voc.taxonomy import loader as tx

BATCH_SIZE = 100
MIN_NEUTRAL_ROWS = 30
ABSTENTION_CATEGORY = "other_or_unclear"
POLARITY_ORDER = {"negative": 0, "positive": 1, "neutral": 2}


def polarity_of(sentiment: int) -> str:
    if sentiment < 0:
        return "negative"
    return "positive" if sentiment > 0 else "neutral"


def bucket_of(driver_category: str, polarity: str) -> str:
    return f"{driver_category}|{polarity}"


def split_bucket(bucket: str) -> tuple[str, str]:
    driver_category, polarity = bucket.split("|", 1)
    return driver_category, polarity


def bucket_slug(bucket: str) -> str:
    """Filesystem-safe form used in cache names and bundle paths."""
    return bucket.replace("|", "__")


def batch_id(bucket: str, idx: int) -> str:
    return f"{bucket_slug(bucket)}/{idx:03d}"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_rows(paths: Paths) -> list[dict[str, Any]]:
    """One row per topic of every status=ok extraction, with product/date taken from the call."""
    calls = {c["call_id"]: c for c in _read_jsonl(paths.calls)}
    rows: list[dict[str, Any]] = []
    for ex in _read_jsonl(paths.extractions):
        if ex.get("status") != "ok" or not isinstance(ex.get("extraction"), dict):
            continue
        call = calls.get(ex["call_id"], {})
        for idx, t in enumerate(ex["extraction"].get("topics") or []):
            statement = str(t.get("issue_statement") or "").strip()
            if not statement:
                continue
            sentiment = int(t.get("sentiment", -1))
            dc = t.get("driver_category") or ABSTENTION_CATEGORY
            pol = polarity_of(sentiment)
            rows.append({
                "topic_id": f"{ex['call_id']}:{idx}", "call_id": ex["call_id"], "idx": idx,
                "product": t.get("product") or call.get("product") or "other_or_unspecified",
                "call_product": call.get("product") or "other_or_unspecified",
                "date": call.get("date") or "", "sentiment": sentiment, "issue_statement": statement,
                "driver": str(t.get("driver") or ""), "driver_category": dc,
                "topic_label": str(t.get("topic_label") or ""), "polarity": pol, "bucket": bucket_of(dc, pol),
            })
    return rows


def _row_sort_key(row: dict[str, Any]) -> tuple:
    return (row["product"], row["date"], row["call_id"], row["idx"])


def bucket_sort_key(bucket: str) -> tuple:
    dc, pol = split_bucket(bucket)
    cats = tx.codes("driver_categories")
    return (POLARITY_ORDER.get(pol, 9), cats.index(dc) if dc in cats else len(cats), dc)


def group_buckets(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Bucket -> rows ordered by product then date; buckets ordered negative, positive, neutral."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["bucket"], []).append(row)
    return {b: sorted(grouped[b], key=_row_sort_key) for b in sorted(grouped, key=bucket_sort_key)}


def is_llm_bucket(bucket: str, n_rows: int) -> bool:
    """Buckets the model sees; the rest go straight to their catch-all theme."""
    dc, pol = split_bucket(bucket)
    if dc == ABSTENTION_CATEGORY or n_rows == 0:
        return False
    return pol != "neutral" or n_rows >= MIN_NEUTRAL_ROWS


def llm_buckets(grouped: dict[str, list[dict[str, Any]]], limit: int | None = None) -> list[str]:
    selected = [b for b, rows in grouped.items() if is_llm_bucket(b, len(rows))]
    return selected[:limit] if limit else selected


def make_batches(rows: list[dict[str, Any]], size: int = BATCH_SIZE) -> list[list[dict[str, Any]]]:
    return [rows[i:i + size] for i in range(0, len(rows), size)]
