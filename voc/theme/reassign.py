"""Pass 3: every topic row assigned again against the frozen registry of its bucket (no new themes)."""
from __future__ import annotations

from typing import Any

from voc.llm.client import LLMClient, LLMRequest
from voc.paths import Paths
from voc.schemas.theme import REASSIGN_API_SCHEMA, THEME_PROMPT_VERSION, ReassignOutput
from voc.theme.buckets import batch_id, group_buckets, llm_buckets, load_rows, make_batches
from voc.theme.registry import (MIN_CONFIDENCE, Registry, RunStats, ThemeOptions, content_hash, gather_requests,
                                make_request, member, prompt_view, registry_hash, render_registry, render_rows,
                                row_view, write_members)

STAGE = "theme_reassign"


def parse_assignments(data: dict[str, Any]) -> dict[str, tuple[str, float]]:
    """topic_id -> (theme_id, confidence); malformed output means every row is unassigned."""
    try:
        out = ReassignOutput.model_validate({"assignments": data.get("assignments", [])})
    except Exception as exc:  # noqa: BLE001 - lenient: a bad batch falls back to the catch-all
        print(f"  invalid assignments ignored: {str(exc)[:120]}")
        return {}
    return {a.topic_id: (a.theme_id, float(a.confidence)) for a in out.assignments}


def build_reassign_request(bucket: str, idx: int, batch: list[dict[str, Any]], view: list[dict[str, Any]],
                           name_prefix: str = "") -> LLMRequest:
    rows = [row_view(r) for r in batch]
    user = (f"Bucket: {bucket}\n\n## Registry (final)\n{render_registry(view)}\n\n"
            f"## Statements ({len(rows)})\n{render_rows(batch)}\n\nAssign every statement (theme_id or NONE).")
    from voc.theme.buckets import bucket_slug
    name = f"{name_prefix}{bucket_slug(bucket)}/{idx:03d}_{registry_hash(view)}"
    key = content_hash(THEME_PROMPT_VERSION, rows, view)
    return make_request(STAGE, name, key, "reassign", user, REASSIGN_API_SCHEMA,
                        {"bucket": bucket, "batch_idx": idx, "rows": rows, "registry": view})


def assign_rows(batch: list[dict[str, Any]], parsed: dict[str, tuple[str, float]], offered_ids: set[str],
                catch_all: str, bid: str, pass_name: str = "reassign") -> list[dict[str, Any]]:
    out = []
    for row in batch:
        theme_id, conf = parsed.get(row["topic_id"], ("NONE", 0.0))
        if theme_id in offered_ids and conf >= MIN_CONFIDENCE:
            out.append(member(row["topic_id"], theme_id, conf, pass_name, bid))
        else:
            out.append(member(row["topic_id"], catch_all, conf, "fallback", bid))
    return out


def fallback_rows(rows: list[dict[str, Any]], catch_all: str, bid: str) -> list[dict[str, Any]]:
    return [member(r["topic_id"], catch_all, 0.0, "fallback", bid) for r in rows]


def reassign_bucket(bucket: str, rows: list[dict[str, Any]], registry: Registry, client: LLMClient,
                    stats: RunStats, opts: ThemeOptions) -> list[dict[str, Any]]:
    catch_all = registry.ensure_catch_all(bucket)
    offered = registry.offered(bucket)
    view = prompt_view(offered)
    batches = make_batches(rows, opts.batch_size)
    if not offered:
        return [m for i, b in enumerate(batches) for m in fallback_rows(b, catch_all, batch_id(bucket, i))]
    reqs = [build_reassign_request(bucket, i, b, view) for i, b in enumerate(batches)]
    results = gather_requests(client, reqs, opts.concurrency)
    offered_ids = {t["theme_id"] for t in offered}
    members: list[dict[str, Any]] = []
    for i, (batch, res) in enumerate(zip(batches, results)):
        stats.record(res)
        members.extend(assign_rows(batch, parse_assignments(res.data), offered_ids, catch_all, batch_id(bucket, i)))
    return members


def run_reassign(paths: Paths, client: LLMClient, stats: RunStats, opts: ThemeOptions) -> list[str]:
    """Write members.jsonl for every topic; returns the buckets left pending by cache misses (skip mode)."""
    from voc.llm.client import LLMCacheMiss
    registry = Registry.load(paths.registry)
    grouped = group_buckets(load_rows(paths))
    selected = set(llm_buckets(grouped, opts.limit_buckets))
    members: list[dict[str, Any]] = []
    pending: list[str] = []
    for bucket, rows in grouped.items():
        if bucket not in selected:
            members.extend(fallback_rows(rows, registry.ensure_catch_all(bucket), batch_id(bucket, 0)))
            continue
        try:
            members.extend(reassign_bucket(bucket, rows, registry, client, stats, opts))
            print(f"reassign {bucket}: {len(rows)} rows, {len(registry.offered(bucket))} themes offered")
        except LLMCacheMiss as exc:
            if opts.on_miss != "skip":
                raise
            pending.append(bucket)
            print(f"reassign {bucket}: pending ({exc})")
    if pending:
        return pending
    write_members(paths.members, members)
    registry.produced_by = "fake" if "fake" in (registry.produced_by or "", stats.produced_by_label()) else (registry.produced_by or stats.produced_by_label())
    if "reassign" not in registry.passes_done:
        registry.passes_done.append("reassign")
    registry.save(paths.registry)
    n_fb = sum(1 for m in members if m["pass"] == "fallback")
    print(f"reassign done: {len(members)} members ({n_fb} fallback to catch-all); {stats.summary()}")
    return []
