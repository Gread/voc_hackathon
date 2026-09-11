"""Stability check: re-assign a random 10 % of rows in shuffled batches and measure agreement with pass 3."""
from __future__ import annotations

import random
from typing import Any

from voc.config import get_settings
from voc.llm.client import LLMCacheMiss, LLMClient
from voc.paths import Paths
from voc.theme.buckets import batch_id, group_buckets, llm_buckets, load_rows, make_batches
from voc.theme.reassign import assign_rows, build_reassign_request, parse_assignments
from voc.theme.registry import Registry, RunStats, ThemeOptions, gather_requests, prompt_view, read_members

SAMPLE_FRACTION = 0.1
MIN_SAMPLE = 5
WEAK_THRESHOLD = 0.6
MIN_THEME_SAMPLE = 3


def sample_rows(rows: list[dict[str, Any]], rng: random.Random, fraction: float = SAMPLE_FRACTION) -> list[dict[str, Any]]:
    k = min(len(rows), max(MIN_SAMPLE, round(len(rows) * fraction)))
    picked = rng.sample(rows, k)
    rng.shuffle(picked)
    return picked


def _resample_bucket(bucket: str, rows: list[dict[str, Any]], registry: Registry, client: LLMClient, stats: RunStats,
                     opts: ThemeOptions) -> list[dict[str, Any]]:
    offered = registry.offered(bucket)
    catch_all = registry.ensure_catch_all(bucket)
    view = prompt_view(offered)
    batches = make_batches(rows, opts.batch_size)
    reqs = [build_reassign_request(bucket, i, b, view, name_prefix="stability/") for i, b in enumerate(batches)]
    results = gather_requests(client, reqs, opts.concurrency)
    offered_ids = {t["theme_id"] for t in offered}
    out = []
    for i, (batch, res) in enumerate(zip(batches, results)):
        stats.record(res)
        out.extend(assign_rows(batch, parse_assignments(res.data), offered_ids, catch_all, batch_id(bucket, i), "stability"))
    return out


def agreement_report(registry: Registry, baseline: dict[str, str], resampled: list[dict[str, Any]]) -> dict[str, Any]:
    per_theme: dict[str, dict[str, Any]] = {}
    n_agree = 0
    for m in resampled:
        before = registry.effective(baseline.get(m["topic_id"], ""))
        after = registry.effective(m["theme_id"])
        agree = before == after
        n_agree += int(agree)
        slot = per_theme.setdefault(before, {"n": 0, "agree": 0})
        slot["n"] += 1
        slot["agree"] += int(agree)
    for slot in per_theme.values():
        slot["agreement"] = round(slot["agree"] / slot["n"], 3) if slot["n"] else None
    weak = sorted(tid for tid, s in per_theme.items() if s["n"] >= MIN_THEME_SAMPLE and s["agreement"] < WEAK_THRESHOLD
                  and tid in registry.themes and registry.get(tid)["status"] == "active")
    n = len(resampled)
    return {"n_sampled": n, "n_agree": n_agree, "agreement": round(n_agree / n, 3) if n else None,
            "per_theme": per_theme, "weak": weak}


def run_stability(paths: Paths, client: LLMClient, stats: RunStats, opts: ThemeOptions) -> list[str]:
    """Write the agreement number and grouping_quality into registry.json; returns pending buckets (skip mode)."""
    registry = Registry.load(paths.registry)
    baseline = {m["topic_id"]: m["theme_id"] for m in read_members(paths.members)}
    grouped = group_buckets(load_rows(paths))
    rng = random.Random(get_settings().seed)
    resampled: list[dict[str, Any]] = []
    pending: list[str] = []
    for bucket in llm_buckets(grouped, opts.limit_buckets):
        if not registry.offered(bucket):
            continue
        try:
            resampled.extend(_resample_bucket(bucket, sample_rows(grouped[bucket], rng), registry, client, stats, opts))
        except LLMCacheMiss as exc:
            if opts.on_miss != "skip":
                raise
            pending.append(bucket)
            print(f"stability {bucket}: pending ({exc})")
    if pending:
        return pending
    report = agreement_report(registry, baseline, resampled)
    for t in registry.themes.values():
        t["grouping_quality"] = "weak" if t["theme_id"] in report["weak"] else "ok"
    registry.stability = report
    if "stability" not in registry.passes_done:
        registry.passes_done.append("stability")
    registry.save(paths.registry)
    print(f"stability: agreement {report['agreement']} on {report['n_sampled']} rows; weak themes: {len(report['weak'])}; {stats.summary()}")
    return []
