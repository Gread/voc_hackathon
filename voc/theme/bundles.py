"""Work bundles for build-time Claude agents.

A theming batch's cache name embeds the registry as it stood when the batch ran, so batches cannot all
be exported up front: the pass is replayed with a recording client that collects every request whose
cache file is missing. Fill those files, export again, repeat until `export` reports nothing pending.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from voc.llm.cached_client import cache_path, read_cache
from voc.llm.client import LLMCacheMiss, LLMClient, LLMRequest, LLMResult
from voc.paths import get_paths
from voc.theme.registry import RunStats, ThemeOptions

README = """# Theme work bundles ({pass_name} pass, wave of {n} batch(es))

Each `bundle_*.json` is one batch the pass is waiting for.

For every bundle:
1. Read `system_prompt` (the rules) and `user` (the registry and the numbered statements).
2. Produce JSON that validates against `schema`.
3. Write it to `cache_file` (path relative to the repo root), exactly this envelope:

```json
{{
  "key": "<the bundle's cache_key, copied verbatim>",
  "model": "claude-agent-build",
  "produced_by": "claude_agent",
  "created_at": "<UTC ISO timestamp>",
  "usage": null,
  "response": {{ "...your JSON..." }}
}}
```

Then run `python -m voc theme import --dir <this dir> --pass {pass_name}`.

Because a batch's identity depends on the registry built by earlier batches, one export is one wave:
after importing, run `python -m voc theme export --dir <dir> --pass {pass_name}` again. When it reports
0 bundles the pass is complete.

Validator rules: every `topic_id` of the batch appears exactly once in `assignments`; `theme_id` is an id
from the registry shown in `user`, `NEW-k` (seed pass only), or `NONE`; at most 5 new themes per batch.
"""


class RecordingClient:
    """Replays cache files; records (and re-raises) every miss so the caller can export it."""

    def __init__(self, inner: LLMClient | None = None) -> None:
        self.inner = inner
        self.missing: list[LLMRequest] = []
        self._seen: set[str] = set()

    def _hit(self, req: LLMRequest) -> LLMResult:
        if req.cache_name:
            hit = read_cache(req.stage, req.cache_name, req.cache_key)
            if hit is not None:
                return hit
        key = f"{req.stage}/{req.cache_name}"
        if key not in self._seen:
            self._seen.add(key)
            self.missing.append(req)
        raise LLMCacheMiss(f"no cached result for {key}")

    def complete_json(self, req: LLMRequest) -> LLMResult:
        return self._hit(req)

    async def acomplete_json(self, req: LLMRequest) -> LLMResult:
        return self._hit(req)


def _runner(pass_name: str):
    from voc.theme import consolidate as consolidate_mod
    from voc.theme import reassign as reassign_mod
    from voc.theme import seed as seed_mod
    from voc.theme import stability as stability_mod

    return {"seed": seed_mod.run_seed, "consolidate": consolidate_mod.run_consolidate,
            "reassign": reassign_mod.run_reassign, "stability": stability_mod.run_stability}[pass_name]


def pending_requests(pass_name: str, opts: ThemeOptions | None = None) -> list[LLMRequest]:
    """Replay the pass against the cache and return the requests it still needs."""
    opts = opts or ThemeOptions()
    opts = ThemeOptions(batch_size=opts.batch_size, sequential=opts.sequential, concurrency=1,
                        cap=opts.cap, limit_buckets=opts.limit_buckets, on_miss="skip")
    client = RecordingClient()
    try:
        _runner(pass_name)(get_paths(), client, RunStats(), opts)
    except LLMCacheMiss:
        pass
    return client.missing


def _bundle_dict(req: LLMRequest, idx: int) -> dict[str, Any]:
    repo_root = get_paths().data_dir.parent
    target = cache_path(req.stage, req.cache_name or f"batch_{idx}")
    try:
        rel = str(target.relative_to(repo_root))
    except ValueError:
        rel = str(target)
    return {"bundle_id": f"{req.stage}:{req.cache_name}", "index": idx, "stage": req.stage,
            "cache_name": req.cache_name, "cache_key": req.cache_key, "cache_file": rel.replace("\\", "/"),
            "model_hint": req.model, "system_prompt": req.system, "user": req.user, "schema": req.schema,
            "rows": req.meta.get("rows", []), "registry": req.meta.get("registry", []),
            "pairs": req.meta.get("pairs", [])}


def export_bundles(directory: Path, pass_name: str = "seed", opts: ThemeOptions | None = None) -> int:
    """Write one JSON file per pending batch of the next wave, plus a README with the contract."""
    directory.mkdir(parents=True, exist_ok=True)
    for stale in directory.glob("bundle_*.json"):
        stale.unlink()
    reqs = pending_requests(pass_name, opts)
    for idx, req in enumerate(reqs):
        path = directory / f"bundle_{idx:03d}.json"
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(_bundle_dict(req, idx), ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, path)
    (directory / "README.md").write_text(README.format(pass_name=pass_name, n=len(reqs)), encoding="utf-8")
    return len(reqs)


def verify_bundle_cache(directory: Path) -> list[str]:
    """Bundle ids whose cache file is missing or carries a stale key."""
    missing: list[str] = []
    for path in sorted(directory.glob("bundle_*.json")):
        bundle = json.loads(path.read_text(encoding="utf-8"))
        target = cache_path(bundle["stage"], bundle["cache_name"])
        try:
            if json.loads(target.read_text(encoding="utf-8")).get("key") != bundle["cache_key"]:
                missing.append(bundle["bundle_id"])
        except (OSError, json.JSONDecodeError):
            missing.append(bundle["bundle_id"])
    return missing
