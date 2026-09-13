"""Pass 2: candidate pairs, model judgements, union-find merges (merges.json) and the rename pass."""
from __future__ import annotations

from typing import Any

from voc.llm.client import LLMClient, LLMRequest, LLMResult
from voc.llm.client import LLMRefusal
from voc.paths import Paths
from voc.schemas.theme import (CONSOLIDATE_API_SCHEMA, RENAME_API_SCHEMA, THEME_PROMPT_VERSION, ConsolidateOutput,
                               RenameOutput)
from voc.theme.buckets import bucket_slug, load_rows
from voc.theme.registry import (Registry, RunStats, ThemeOptions, content_hash, gather_requests, make_request,
                                merge_record, prompt_view, read_members, read_merges, registry_hash, write_merges)
from voc.theme.similarity import Similarity, default_similarity

STAGE = "theme_consolidate"
PAIR_BATCH = 40
SAMPLES_PER_THEME = 3
RENAME_BATCH = 40
NAME_JACCARD = 0.5
MAX_PAIRS_PER_THEME = 10   # keeps the pair list linear in the number of themes


def theme_products(members: list[dict[str, Any]], rows_by_id: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for m in members:
        row = rows_by_id.get(m["topic_id"])
        if row:
            out.setdefault(m["theme_id"], set()).add(row["product"])
    return out


def theme_samples(members: list[dict[str, Any]], rows_by_id: dict[str, dict[str, Any]], registry: Registry,
                  k: int = SAMPLES_PER_THEME) -> dict[str, list[str]]:
    """Up to k distinct member statements per theme, in membership order; registry examples as a fallback."""
    out: dict[str, list[str]] = {}
    for m in members:
        row = rows_by_id.get(m["topic_id"])
        lst = out.setdefault(m["theme_id"], [])
        if row and len(lst) < k and row["issue_statement"] not in lst:
            lst.append(row["issue_statement"])
    for t in registry.themes.values():
        lst = out.setdefault(t["theme_id"], [])
        for ex in t.get("examples", []):
            if len(lst) < k and ex not in lst:
                lst.append(ex)
    return out


def _judged_by(result: LLMResult) -> str:
    return result.model if result.produced_by == "api" else result.produced_by


def candidate_pairs(registry: Registry, products: dict[str, set[str]], bucket: str | None = None,
                    sim: Similarity | None = None) -> list[tuple[str, str]]:
    """Same polarity and (same driver_category with a shared product, or name+problem Jaccard >= 0.5)."""
    sim = sim or default_similarity()
    themes = sorted(registry.active(bucket), key=lambda t: t["theme_id"])
    scored: list[tuple[float, str, str]] = []
    for i, a in enumerate(themes):
        for b in themes[i + 1:]:
            if a["polarity"] != b["polarity"]:
                continue
            score = sim.score(f"{a['name']} {a['problem_statement']}", f"{b['name']} {b['problem_statement']}")
            same_family = (a["driver_category"] == b["driver_category"]
                           and bool(products.get(a["theme_id"], set()) & products.get(b["theme_id"], set())))
            if same_family or score >= NAME_JACCARD:
                scored.append((score, a["theme_id"], b["theme_id"]))
    scored.sort(key=lambda s: (-s[0], s[1], s[2]))
    counts: dict[str, int] = {}
    pairs: list[tuple[str, str]] = []
    for _, a, b in scored:
        if counts.get(a, 0) >= MAX_PAIRS_PER_THEME or counts.get(b, 0) >= MAX_PAIRS_PER_THEME:
            continue
        counts[a], counts[b] = counts.get(a, 0) + 1, counts.get(b, 0) + 1
        pairs.append((a, b))
    return sorted(pairs)


def _pair_view(a: str, b: str, registry: Registry, samples: dict[str, list[str]]) -> dict[str, Any]:
    def side(tid: str) -> dict[str, Any]:
        t = registry.get(tid)
        return {"theme_id": tid, "name": t["name"], "problem_statement": t["problem_statement"],
                "root_cause": t["root_cause"], "bucket": t["bucket"], "samples": samples.get(tid, [])[:SAMPLES_PER_THEME]}
    return {"a": a, "b": b, "theme_a": side(a), "theme_b": side(b)}


def _render_pairs(pairs: list[dict[str, Any]]) -> str:
    lines = []
    for i, p in enumerate(pairs):
        lines.append(f"### Pair {i + 1}: {p['a']} vs {p['b']}")
        for side in ("theme_a", "theme_b"):
            t = p[side]
            samples = "\n".join(f'    - "{s}"' for s in t["samples"]) or "    - (no samples)"
            lines.append(f"- {t['theme_id']} [{t['bucket']}] {t['name']}\n  problem: {t['problem_statement']}\n"
                         f"  cause: {t['root_cause']}\n  samples:\n{samples}")
    return "\n".join(lines)


def build_consolidate_request(pairs: list[dict[str, Any]], idx: int, scope: str, view_hash: str) -> LLMRequest:
    user = (f"Scope: {scope}\n\n## Candidate pairs ({len(pairs)})\n{_render_pairs(pairs)}\n\n"
            "Decide for every pair: merge or keep separate.")
    key = content_hash(THEME_PROMPT_VERSION, pairs)
    return make_request(STAGE, f"{scope}/{idx:03d}_{view_hash}", key, "consolidate", user, CONSOLIDATE_API_SCHEMA,
                        {"scope": scope, "batch_idx": idx, "pairs": pairs}, effort="high")


def apply_decisions(registry: Registry, decisions: list[dict[str, Any]], valid_pairs: set[tuple[str, str]],
                    pass_name: str, judged_by: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Union-find over merged_into: the loser root points at the winner root; returns (merges, decision log)."""
    merges, log = [], []
    for d in decisions:
        a, b = d.get("a"), d.get("b")
        if (a, b) not in valid_pairs and (b, a) not in valid_pairs:
            continue
        log.append({"a": a, "b": b, "merge": bool(d.get("merge")), "into": d.get("into"), "reason": str(d.get("reason", ""))[:120],
                    "pass": pass_name, "judged_by": judged_by})
        if not d.get("merge"):
            continue
        ra, rb = registry.effective(a), registry.effective(b)
        if ra == rb or registry.get(ra)["status"] != "active" or registry.get(rb)["status"] != "active":
            continue
        winner = ra if d.get("into") == a else rb if d.get("into") == b else min(ra, rb)
        loser = rb if winner == ra else ra
        registry.mark_merged(loser, winner)
        merges.append(merge_record(loser, winner, pass_name, str(d.get("reason", "")), judged_by))
    return merges, log


def consolidate_scope(registry: Registry, members: list[dict[str, Any]], rows_by_id: dict[str, dict[str, Any]],
                      client: LLMClient, stats: RunStats, opts: ThemeOptions, bucket: str | None = None,
                      pass_name: str = "consolidate") -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Judge every candidate pair in the scope (one bucket or all) and apply the merges."""
    products = theme_products(members, rows_by_id)
    samples = theme_samples(members, rows_by_id, registry)
    pairs = candidate_pairs(registry, products, bucket)
    scope = bucket_slug(bucket) if bucket else "all"
    if not pairs:
        return [], []
    view_hash = registry_hash(prompt_view(sorted(registry.active(bucket), key=lambda t: t["theme_id"])))
    batches = [pairs[i:i + PAIR_BATCH] for i in range(0, len(pairs), PAIR_BATCH)]
    reqs = [build_consolidate_request([_pair_view(a, b, registry, samples) for a, b in batch], i, scope, view_hash)
            for i, batch in enumerate(batches)]
    results = gather_requests(client, reqs, opts.concurrency, tolerate=LLMRefusal)
    merges, log = [], []
    for batch, res in zip(batches, results):
        if isinstance(res, BaseException):
            print(f"  consolidate batch refused, its {len(batch)} pair(s) stay separate")
            continue
        stats.record(res)
        try:
            decisions = ConsolidateOutput.model_validate(res.data).model_dump()["decisions"]
        except Exception as exc:  # noqa: BLE001 - a malformed batch merges nothing
            print(f"  invalid consolidate output ignored: {str(exc)[:120]}")
            continue
        m, lg = apply_decisions(registry, decisions, set(batch), pass_name, _judged_by(res))
        merges.extend(m)
        log.extend(lg)
    print(f"consolidate [{scope}]: {len(pairs)} pairs judged, {len(merges)} merges")
    return merges, log


def rename_pass(registry: Registry, members: list[dict[str, Any]], rows_by_id: dict[str, dict[str, Any]],
                client: LLMClient, stats: RunStats, opts: ThemeOptions) -> None:
    """Names and definitions only; bumps codebook_version. Membership is untouched."""
    samples = theme_samples(members, rows_by_id, registry)
    themes = sorted(registry.active(), key=lambda t: t["theme_id"])
    if not themes:
        return
    batches = [themes[i:i + RENAME_BATCH] for i in range(0, len(themes), RENAME_BATCH)]
    reqs = []
    for i, batch in enumerate(batches):
        view = [dict(v, samples=samples.get(v["theme_id"], [])) for v in prompt_view(batch)]
        user = "## Themes\n" + "\n".join(
            f"- {v['theme_id']} | {v['name']} | problem: {v['problem_statement']} | cause: {v['root_cause']} | samples: "
            + "; ".join(f'"{s}"' for s in v["samples"]) for v in view) + "\n\nReturn every theme with its final name and definitions."
        reqs.append(make_request("theme_rename", f"rename/{i:03d}_{registry_hash(view)}", content_hash(THEME_PROMPT_VERSION, view),
                                 "rename", user, RENAME_API_SCHEMA, {"batch_idx": i, "registry": view}))
    results = gather_requests(client, reqs, opts.concurrency, tolerate=LLMRefusal)
    registry.codebook_version += 1
    for batch, res in zip(batches, results):
        if isinstance(res, BaseException):
            print(f"  rename batch refused, {len(batch)} theme(s) keep their current names")
            continue
        stats.record(res)
        allowed = {t["theme_id"] for t in batch}
        try:
            renamed = RenameOutput.model_validate(res.data).themes
        except Exception as exc:  # noqa: BLE001
            print(f"  invalid rename output ignored: {str(exc)[:120]}")
            renamed = []
        for r in renamed:
            if r.theme_id in allowed:
                registry.rename(r.theme_id, r.name, r.problem_statement, r.root_cause)
    print(f"rename: {len(themes)} themes, codebook_version -> {registry.codebook_version}")


def run_consolidate(paths: Paths, client: LLMClient, stats: RunStats, opts: ThemeOptions) -> list[str]:
    """Consolidate the seeded registry across all buckets; returns ["consolidate"] when pending (skip mode)."""
    from voc.llm.client import LLMCacheMiss
    registry = Registry.load(paths.registry)
    if "consolidate" in registry.passes_done:
        print("consolidate: already done for this registry (re-run `voc theme seed` to rebuild)")
        return []
    members = read_members(paths.members)
    rows_by_id = {r["topic_id"]: r for r in load_rows(paths)}
    existing = read_merges(paths.merges)
    try:
        merges, log = consolidate_scope(registry, members, rows_by_id, client, stats, opts)
        rename_pass(registry, members, rows_by_id, client, stats, opts)
    except LLMCacheMiss as exc:
        if opts.on_miss != "skip":
            raise
        print(f"consolidate: pending ({exc})")
        return ["consolidate"]
    known = {m["from_theme"] for m in existing["merges"]}
    all_merges = existing["merges"] + [m for m in merges if m["from_theme"] not in known]
    write_merges(paths.merges, all_merges, existing["decisions"] + log)
    registry.passes_done.append("consolidate")
    registry.produced_by = "fake" if "fake" in (registry.produced_by or "", stats.produced_by_label()) else (registry.produced_by or stats.produced_by_label())
    registry.save(paths.registry)
    print(f"consolidate done: {len(registry.active())} active themes; {stats.summary()}")
    return []
