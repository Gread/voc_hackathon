"""Pull a Hugging Face conversation corpus into the transcript shape the pipeline already reads.

The source is one row per utterance (conversation_id, speaker, date_time, text); this groups them
back into whole conversations and keeps the ones long enough to be worth reading.

The corpora differ in kind and the product says so: complaints are real, written, and span two
years; this one is synthetic, spoken-shaped, and covers a single month. `origin` on every record
carries that, and the interface labels it rather than blending the two silently.
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Any, Iterator

import httpx

from voc.paths import Paths

ROWS_URL = "https://datasets-server.huggingface.co/rows"
PAGE = 100                      # the datasets-server maximum
SPEAKER_MAP = {"client": "customer", "customer": "customer", "user": "customer"}
MIN_TURNS = 6                   # below this there is no contact to read
MIN_CUSTOMER_WORDS = 25         # the customer has to actually say something
MAX_RETRIES = 6
RETRY_STATUSES = {429, 500, 502, 503, 504}
PAUSE_S = 0.35                  # the public endpoint rate-limits a tight loop


def fetch_page(dataset: str, offset: int, *, config: str = "default", split: str = "train",
               client: httpx.Client | None = None, sleep: Any = time.sleep) -> list[dict[str, Any]]:
    """One page of utterances, retrying the rate limit the public endpoint applies."""
    owned = client is None
    client = client or httpx.Client(timeout=90.0)
    try:
        for attempt in range(MAX_RETRIES + 1):
            response = client.get(ROWS_URL, params={"dataset": dataset, "config": config, "split": split,
                                                    "offset": offset, "length": PAGE})
            if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES:
                wait = float(response.headers.get("Retry-After") or 0) or min(60.0, 3.0 * 2 ** attempt)
                sleep(wait + random.random())
                continue
            response.raise_for_status()
            return [row["row"] for row in response.json().get("rows", [])]
        raise RuntimeError("unreachable")
    finally:
        if owned:
            client.close()


def group_conversations(rows: Iterator[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    """Utterance rows arrive grouped by conversation; emit each conversation once it ends."""
    current: list[dict[str, Any]] = []
    cid: str | None = None
    for row in rows:
        rid = str(row.get("conversation_id") or "")
        if cid is not None and rid != cid:
            yield {"conversation_id": cid, "utterances": current}
            current = []
        cid = rid
        current.append(row)
    if cid is not None and current:
        yield {"conversation_id": cid, "utterances": current}


def to_transcript(conv: dict[str, Any], *, company: str, fraction: float) -> dict[str, Any] | None:
    """The record shape `voc ingest transcripts` reads, or None when there is nothing to read."""
    turns = []
    customer_words = 0
    for utterance in conv["utterances"]:
        speaker = SPEAKER_MAP.get(str(utterance.get("speaker", "")).lower(), "agent")
        text = str(utterance.get("text") or "").strip()
        if not text:
            continue
        if speaker == "customer":
            customer_words += len(text.split())
        turns.append({"speaker": speaker, "text": text})
    if len(turns) < MIN_TURNS or customer_words < MIN_CUSTOMER_WORDS:
        return None
    date = str(conv["utterances"][0].get("date_time") or "")[:10]
    if len(date) != 10:
        return None
    return {"id": conv["conversation_id"], "date": date, "turns": turns,
            "company": company, "sampling_fraction": fraction,
            "origin": "synthetic", "n_utterances": len(turns)}


def pull(paths: Paths, dataset: str, *, target: int, seed: int, company: str,
         skip: int = 0, append: bool = False,
         out: Path | None = None, client: httpx.Client | None = None) -> Path:
    """Read the leading conversations of the dataset and write transcript JSONL.

    This is a prefix, not a hash sample, and the reason is worth stating: the file is not ordered by
    date (every offset carries the same September 2023 spread), so the first N conversations are as
    representative in time as any other N, and reading them costs 1 request per 100 utterances
    instead of paging the whole 5.5M-row corpus to sample a fraction of it. Deterministic all the
    same: the same target gives the same conversations, and `skip` continues where a previous pull
    stopped so a corpus can be grown without re-reading what is already ingested.
    """
    out = out or paths.data_dir / "raw" / "hf" / f"{dataset.replace('/', '__')}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    owned = client is None
    client = client or httpx.Client(timeout=90.0)
    kept: list[dict[str, Any]] = []
    seen = offset = 0
    try:
        def rows() -> Iterator[dict[str, Any]]:
            nonlocal offset
            while True:
                page = fetch_page(dataset, offset, client=client)
                if not page:
                    return
                yield from page
                offset += len(page)
                time.sleep(PAUSE_S)

        for conv in group_conversations(rows()):
            seen += 1
            if seen <= skip:                      # already ingested by an earlier pull
                continue
            record = to_transcript(conv, company=company, fraction=1.0)
            if record is not None:
                kept.append(record)
                if len(kept) % 250 == 0:
                    print(f"  {len(kept)}/{target} conversations", flush=True)
            if len(kept) >= target:
                break
    finally:
        if owned:
            client.close()
    with out.open("a" if append else "w", encoding="utf-8") as handle:
        for record in kept:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"hf: {seen} conversations scanned ({skip} skipped), {len(kept)} kept -> {out}")
    return out
