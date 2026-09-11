"""Cache files (data/cache/extract/<call_id>.json, whoever wrote them) -> data/extractions.jsonl."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from voc.extract.prompt import cache_key
from voc.extract.validate import make_row, validate_response
from voc.paths import Paths, get_paths
from voc.schemas.call import CallRecord


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl_atomic(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def load_calls(path: Path | None = None) -> list[CallRecord]:
    p = path or get_paths().calls
    if not p.exists():
        raise FileNotFoundError(f"{p} not found: run `voc ingest sample` first")
    return [CallRecord.model_validate(row) for row in read_jsonl(p)]


def cache_file(call_id: str, paths: Paths | None = None) -> Path:
    return (paths or get_paths()).cache_extract / f"{call_id}.json"


def read_cache_file(path: Path) -> dict[str, Any] | str:
    """The payload, or an error message when the file is unreadable."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"unreadable cache file: {exc}"
    if not isinstance(payload, dict):
        return "cache file is not a JSON object"
    return payload


def validate_cache_payload(call: CallRecord, payload: dict[str, Any]) -> dict[str, Any]:
    """Validate one cache payload for its call through the same path as live responses."""
    produced_by = payload.get("produced_by")
    model = payload.get("model")
    created_at = payload.get("created_at")
    expected = cache_key(call.text_sha)
    if payload.get("key") != expected:
        return make_row(call, status="error", produced_by=produced_by, model=model, extracted_at=created_at,
                        error=f"stale cache key: expected {expected[:12]}..., file has "
                              f"{str(payload.get('key'))[:12]}... (prompt, schema, taxonomy or text changed)")
    if payload.get("response") is None:
        return make_row(call, status="error", produced_by=produced_by, model=model, extracted_at=created_at,
                        error=str(payload.get("error") or "cache file has no response"))
    extra: list[str] = []
    if payload.get("text_sha") not in (None, call.text_sha):
        extra.append("cache_text_sha_mismatch")
    return validate_response(call, payload["response"], produced_by=produced_by, model=model,
                             extracted_at=created_at, extra_flags=extra)


def row_for_call(call: CallRecord, paths: Paths | None = None) -> dict[str, Any] | None:
    """The extractions row for a call from its cache file, or None when no file exists."""
    p = cache_file(call.call_id, paths)
    if not p.exists():
        return None
    payload = read_cache_file(p)
    if isinstance(payload, str):
        return make_row(call, status="error", produced_by=None, model=None, extracted_at=None, error=payload)
    return validate_cache_payload(call, payload)


def consolidate(calls: list[CallRecord], paths: Paths | None = None,
                extra_rows: dict[str, dict[str, Any]] | None = None) -> dict[str, int]:
    """Validate every cache file and write data/extractions.jsonl sorted by call_id.
    extra_rows supplies rows (e.g. run errors) for calls that have no cache file."""
    paths = paths or get_paths()
    rows: list[dict[str, Any]] = []
    for call in calls:
        row = row_for_call(call, paths)
        if row is None and extra_rows:
            row = extra_rows.get(call.call_id)
        if row is not None:
            rows.append(row)
    rows.sort(key=lambda r: r["call_id"])
    write_jsonl_atomic(paths.extractions, rows)
    n_ok = sum(1 for r in rows if r["status"] == "ok")
    stats = {"n_calls": len(calls), "n_rows": len(rows), "n_ok": n_ok, "n_error": len(rows) - n_ok,
             "n_missing": len(calls) - len(rows)}
    print(f"loaded {stats['n_rows']} rows -> {paths.extractions} "
          f"(ok {stats['n_ok']}, error {stats['n_error']}, missing {stats['n_missing']})")
    return stats
