"""Pass 1: seed the theme registry bucket by bucket (sequential head, concurrent tail, reconcile, cap)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from voc.llm.client import LLMCacheMiss, LLMClient, LLMRefusal, LLMRequest
from voc.paths import Paths
from voc.schemas.theme import SEED_API_SCHEMA, THEME_PROMPT_VERSION, SeedOutput
from voc.theme.buckets import batch_id, bucket_slug, group_buckets, llm_buckets, load_rows, make_batches
from voc.theme.consolidate import consolidate_scope
from voc.theme.reassign import assign_rows, fallback_rows
from voc.theme.registry import (Registry, RunStats, ThemeOptions, content_hash, gather_requests, make_request,
                                prompt_view, registry_hash, render_registry, render_rows, row_view, write_members,
                                write_merges)
from voc.theme.similarity import token_set_jaccard

STAGE = "theme_seed"
MAX_NEW_PER_BATCH = 5
RECONCILE_THRESHOLD = 0.6


@dataclass
class SeedState:
    registry: Registry
    rows_by_id: dict[str, dict[str, Any]]
    members: list[dict[str, Any]] = field(default_factory=list)
    merges: list[dict[str, Any]] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)


def build_seed_request(bucket: str, idx: int, batch: list[dict[str, Any]], view: list[dict[str, Any]]) -> LLMRequest:
    rows = [row_view(r) for r in batch]
    user = (f"Bucket: {bucket}\n\n## Registry ({len(view)} themes)\n{render_registry(view)}\n\n"
            f"## Statements ({len(rows)})\n{render_rows(batch)}\n\n"
            "Assign every statement; define new themes only when no cause fits (max 5).")
    key = content_hash(THEME_PROMPT_VERSION, rows, view)
    return make_request(STAGE, f"{bucket_slug(bucket)}/{idx:03d}_{registry_hash(view)}", key, "seed", user,
                        SEED_API_SCHEMA, {"bucket": bucket, "batch_idx": idx, "rows": rows, "registry": view})


def parse_seed(data: dict[str, Any]) -> SeedOutput:
    try:
        return SeedOutput.model_validate(data)
    except Exception as exc:  # noqa: BLE001 - a malformed batch assigns nothing
        print(f"  invalid seed output ignored: {str(exc)[:120]}")
        return SeedOutput(assignments=[], new_themes=[])


def accept_new_themes(bucket: str, output: SeedOutput, registry: Registry, cap: int,
                      accepted: list[tuple[str, str]] | None) -> dict[str, str]:
    """tmp_id -> theme_id for accepted proposals. With `accepted` (parallel phase), proposals whose name
    overlaps an earlier parallel proposal >= 0.6 map to that earlier theme; the cap drops the rest."""
    mapping: dict[str, str] = {}
    for nt in output.new_themes[:MAX_NEW_PER_BATCH]:
        if accepted is not None:
            twin = next((tid for name, tid in accepted if token_set_jaccard(name, nt.name) >= RECONCILE_THRESHOLD), None)
            if twin:
                mapping[nt.tmp_id] = twin
                continue
        if len(registry.active(bucket)) >= cap:
            continue
        theme = registry.add(bucket, nt.name, nt.problem_statement, nt.root_cause, created_pass="seed")
        mapping[nt.tmp_id] = theme["theme_id"]
        if accepted is not None:
            accepted.append((nt.name, theme["theme_id"]))
    return mapping


def apply_batch(bucket: str, batch: list[dict[str, Any]], output: SeedOutput, tmp_map: dict[str, str],
                offered_ids: set[str], state: SeedState, bid: str) -> None:
    parsed = {a.topic_id: (tmp_map.get(a.theme_id, a.theme_id), float(a.confidence)) for a in output.assignments}
    catch_all = state.registry.catch_all_id(bucket) or state.registry.ensure_catch_all(bucket)
    for m in assign_rows(batch, parsed, offered_ids | set(tmp_map.values()), catch_all, bid, "seed"):
        state.members.append(m)
        if m["pass"] == "seed":
            state.registry.add_example(m["theme_id"], state.rows_by_id[m["topic_id"]]["issue_statement"])


def _maybe_consolidate(bucket: str, state: SeedState, client: LLMClient, stats: RunStats, opts: ThemeOptions) -> None:
    if len(state.registry.active(bucket)) < opts.cap:
        return
    print(f"  {bucket}: cap {opts.cap} reached, consolidating mid-way")
    merges, log = consolidate_scope(state.registry, state.members, state.rows_by_id, client, stats, opts,
                                    bucket=bucket, pass_name="seed_consolidate")
    state.merges.extend(merges)
    state.decisions.extend(log)


def seed_bucket(bucket: str, rows: list[dict[str, Any]], state: SeedState, client: LLMClient, stats: RunStats,
                opts: ThemeOptions) -> None:
    registry = state.registry
    registry.ensure_catch_all(bucket)
    batches = make_batches(rows, opts.batch_size)
    for i, batch in enumerate(batches[:opts.sequential]):
        offered = registry.active(bucket)
        try:
            res = client.complete_json(build_seed_request(bucket, i, batch, prompt_view(offered)))
        except LLMRefusal as exc:
            # Some batches the provider simply will not answer, fraud narratives especially. Losing
            # 100 statements to the catch-all beats losing a run of 150 requests.
            state.members.extend(fallback_rows(batch, registry.ensure_catch_all(bucket), batch_id(bucket, i)))
            print(f"seed {bucket} batch {i}: refused, rows go to the catch-all ({exc})")
            continue
        stats.record(res)
        out = parse_seed(res.data)
        tmp_map = accept_new_themes(bucket, out, registry, opts.cap, None)
        apply_batch(bucket, batch, out, tmp_map, {t["theme_id"] for t in offered}, state, batch_id(bucket, i))
        _maybe_consolidate(bucket, state, client, stats, opts)
    rest = batches[opts.sequential:]
    if not rest:
        return
    offered = registry.active(bucket)              # frozen snapshot for the concurrent tail
    view = prompt_view(offered)
    reqs = [build_seed_request(bucket, opts.sequential + j, b, view) for j, b in enumerate(rest)]
    results = gather_requests(client, reqs, opts.concurrency, tolerate=LLMRefusal)
    accepted: list[tuple[str, str]] = []
    for j, (batch, res) in enumerate(zip(rest, results)):
        if isinstance(res, BaseException):
            state.members.extend(fallback_rows(batch, registry.ensure_catch_all(bucket),
                                               batch_id(bucket, opts.sequential + j)))
            print(f"seed {bucket} batch {opts.sequential + j}: refused, rows go to the catch-all")
            continue
        stats.record(res)
        out = parse_seed(res.data)
        tmp_map = accept_new_themes(bucket, out, registry, opts.cap, accepted)
        apply_batch(bucket, batch, out, tmp_map, {t["theme_id"] for t in offered}, state, batch_id(bucket, opts.sequential + j))
    _maybe_consolidate(bucket, state, client, stats, opts)


def run_seed(paths: Paths, client: LLMClient, stats: RunStats, opts: ThemeOptions) -> SeedState:
    """Build registry.json, members.jsonl (pass=seed) and merges.json from scratch; pending buckets (skip mode)
    leave the files untouched so a re-run replays the cache and continues."""
    rows = load_rows(paths)
    grouped = group_buckets(rows)
    state = SeedState(registry=Registry(), rows_by_id={r["topic_id"]: r for r in rows})
    selected = set(llm_buckets(grouped, opts.limit_buckets))
    print(f"seed: {len(rows)} topic rows in {len(grouped)} buckets ({len(selected)} sent to the model)")
    for bucket, brows in grouped.items():
        catch_all = state.registry.ensure_catch_all(bucket)
        if bucket not in selected:
            state.members.extend(fallback_rows(brows, catch_all, batch_id(bucket, 0)))
            continue
        try:
            seed_bucket(bucket, brows, state, client, stats, opts)
            print(f"seed {bucket}: {len(brows)} rows -> {len(state.registry.active(bucket))} themes")
        except LLMCacheMiss as exc:
            if opts.on_miss != "skip":
                raise
            state.pending.append(bucket)
            print(f"seed {bucket}: pending ({exc})")
    if state.pending:
        return state
    state.registry.produced_by = stats.produced_by_label()
    state.registry.passes_done = ["seed"]
    state.registry.save(paths.registry)
    write_members(paths.members, state.members)
    write_merges(paths.merges, state.merges, state.decisions)
    print(f"seed done: {len(state.registry.active())} active themes, {len(state.members)} members; {stats.summary()}")
    return state
