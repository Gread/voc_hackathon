"""Constant-fraction hash sampling of eligible CFPB narratives -> data/calls.jsonl."""
from __future__ import annotations

import hashlib
from collections import Counter
from typing import Any

from voc.ingest.cfpb import read_raw_window
from voc.ingest.normalize import (
    complaint_id_of, date_of, normalize_narrative, raw_to_call, read_json, word_count,
    write_json_atomic, write_jsonl_atomic,
)
from voc.paths import Paths
from voc.schemas.call import text_sha

DEFAULT_MIN_WORDS = 30


def keep_score(seed: int, complaint_id: int | str) -> float:
    """Uniform in [0, 1): the record is sampled iff keep_score < f."""
    digest = hashlib.sha256(f"{seed}:{complaint_id}".encode("utf-8")).hexdigest()
    return int(digest, 16) / 2**256


def _prepared(src: dict[str, Any]) -> dict[str, Any]:
    """Raw _source plus the normalised text and its sha, used for dedupe and word counts."""
    text = normalize_narrative(src.get("complaint_what_happened") or "")
    return {**src, "_text": text, "_sha": text_sha(text), "_date": date_of(src), "_cid": complaint_id_of(src)}


def eligible_rows(rows_by_month: dict[str, list[dict]], min_words: int = DEFAULT_MIN_WORDS) -> list[dict]:
    """Drop short narratives, dedupe by complaint_id and by identical text keeping the earliest; sorted by date, id."""
    prepared = [_prepared(src) for rows in rows_by_month.values() for src in rows]
    prepared = [p for p in prepared if word_count(p["_text"]) >= min_words]
    prepared.sort(key=lambda p: (p["_date"], str(p["_cid"]).zfill(12)))
    seen_sha: set[str] = set()
    seen_cid: set[str] = set()
    out: list[dict] = []
    for p in prepared:
        if p["_sha"] not in seen_sha and str(p["_cid"]) not in seen_cid:
            seen_sha.add(p["_sha"])
            seen_cid.add(str(p["_cid"]))
            out.append(p)
    return out


def implied_fraction(target: int, n_eligible: int) -> float:
    if n_eligible <= 0:
        return 0.0
    return min(1.0, target / n_eligible)


def select(rows: list[dict], fraction: float, seed: int) -> list[dict]:
    return [p for p in rows if keep_score(seed, p["_cid"]) < fraction]


def population_by_month(rows: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(p["_date"][:7] for p in rows).items()))


def sample(paths: Paths, company: str, start: str, end: str, *, target: int, seed: int,
           min_words: int = DEFAULT_MIN_WORDS) -> dict[str, Any]:
    """Write data/calls.jsonl for the window and the population counts into data/profile.json."""
    raw = read_raw_window(paths, company, start, end)
    if not raw:
        raise SystemExit(f"no raw months for {company!r} under {paths.raw_cfpb}; run `voc ingest pull` first")
    eligible = eligible_rows(raw, min_words)
    fraction = implied_fraction(target, len(eligible))
    chosen = select(eligible, fraction, seed)
    records = [raw_to_call(p, fraction, company) for p in chosen]
    records.sort(key=lambda r: (r.date, r.call_id))
    n = write_jsonl_atomic(paths.calls, (r.model_dump() for r in records))

    profile = read_json(paths.profile, default={}) or {}
    profile.update({
        "company": company,
        "window": {"start": start, "end": end},
        "seed": seed,
        "target": target,
        "min_words": min_words,
        "n_raw": sum(len(v) for v in raw.values()),
        "n_eligible": len(eligible),
        "n_sampled": n,
        "sampling_fraction": fraction,
        "population_by_month": population_by_month(eligible),
        "sampled_by_month": population_by_month(chosen),
    })
    write_json_atomic(paths.profile, profile)
    print(f"raw {profile['n_raw']}  eligible {len(eligible)}  f={fraction:.4f}  sampled {n} -> {paths.calls}")
    return profile
