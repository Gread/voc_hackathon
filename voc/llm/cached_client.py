"""Record/replay wrapper: data/cache/<stage>/<name>.json is the hand-off format for build-time agents."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voc.llm.client import LLMCacheMiss, LLMClient, LLMRequest, LLMResult, Usage
from voc.paths import get_paths


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def cache_path(stage: str, name: str) -> Path:
    return get_paths().cache / stage / f"{name}.json"


def read_cache(stage: str, name: str, key: str | None) -> LLMResult | None:
    """Return the cached result when the file exists and its key matches (or no key is required)."""
    p = cache_path(stage, name)
    if not p.exists():
        return None
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if key and payload.get("key") != key:
        return None
    if not isinstance(payload.get("response"), dict):
        return None
    usage = Usage(**{k: int(v or 0) for k, v in (payload.get("usage") or {}).items()
                     if k in Usage.__dataclass_fields__})
    return LLMResult(data=payload["response"], usage=usage, model=payload.get("model", "unknown"),
                     produced_by=payload.get("produced_by", "unknown"), cached=True)


def write_cache(stage: str, name: str, key: str | None, result: LLMResult, meta: dict[str, Any] | None = None) -> Path:
    payload: dict[str, Any] = dict(meta or {})
    payload.update({
        "key": key, "model": result.model, "produced_by": result.produced_by,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "usage": result.usage.to_dict(), "response": result.data,
    })
    p = cache_path(stage, name)
    atomic_write_json(p, payload)
    return p


class CachedClient:
    def __init__(self, inner: LLMClient | None, write_only: bool = False):
        self.inner = inner
        self.write_only = write_only

    def _lookup(self, req: LLMRequest) -> LLMResult | None:
        if self.write_only or not req.cache_name:
            return None
        return read_cache(req.stage, req.cache_name, req.cache_key)

    def _store(self, req: LLMRequest, result: LLMResult) -> None:
        if req.cache_name:
            write_cache(req.stage, req.cache_name, req.cache_key, result, req.meta)

    def _miss(self, req: LLMRequest) -> LLMCacheMiss:
        return LLMCacheMiss(f"no cached result for {req.stage}/{req.cache_name} and no API access")

    def complete_json(self, req: LLMRequest) -> LLMResult:
        hit = self._lookup(req)
        if hit is not None:
            return hit
        if self.inner is None:
            raise self._miss(req)
        result = self.inner.complete_json(req)
        self._store(req, result)
        return result

    async def acomplete_json(self, req: LLMRequest) -> LLMResult:
        hit = self._lookup(req)
        if hit is not None:
            return hit
        if self.inner is None:
            raise self._miss(req)
        result = await self.inner.acomplete_json(req)
        self._store(req, result)
        return result
