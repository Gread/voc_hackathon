"""The extraction stage: select pending records, run them through the LLM client with a
concurrency cap and a budget guard, persist per-record cache files, consolidate, report."""
from __future__ import annotations

import asyncio
import json
import os
import time
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voc.config import Settings, get_settings
from voc.extract import load
from voc.extract.prompt import STAGE, build_request, build_system_prompt, cache_key, estimate_tokens
from voc.llm import cost
from voc.llm.cached_client import CachedClient, atomic_write_json, cache_path, read_cache
from voc.llm.client import LLMClient, LLMRequest, Usage, get_client
from voc.paths import Paths, get_paths
from voc.schemas.call import CallRecord
from voc.taxonomy import loader as tx

DRY_RUN_SAMPLE = 50
OUTPUT_TOKENS_PER_RECORD = 1000     # JSON ~700 + thinking ~300 (DESIGN 5.8)
PROGRESS_EVERY = 25


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- selection -----------------------------------------------------------------------------

def round_robin_by_month(records: list[CallRecord]) -> list[CallRecord]:
    """Interleave months so a partial run stays uniform over time."""
    by_month: dict[str, deque[CallRecord]] = defaultdict(deque)
    for r in sorted(records, key=lambda r: (r.date, r.call_id)):
        by_month[r.month].append(r)
    queues = [by_month[m] for m in sorted(by_month)]
    out: list[CallRecord] = []
    while queues:
        for q in list(queues):
            out.append(q.popleft())
            if not q:
                queues.remove(q)
    return out


def _has_valid_cache(call: CallRecord) -> bool:
    return read_cache(STAGE, call.call_id, cache_key(call.text_sha)) is not None


def _cached_produced_by(call: CallRecord, paths: Paths) -> str | None:
    payload = load.read_cache_file(load.cache_file(call.call_id, paths))
    return None if isinstance(payload, str) else payload.get("produced_by")


def select_pending(calls: list[CallRecord], *, ids: set[str] | None = None, retry_errors: bool = False,
                   force: bool = False, force_api: bool = False, paths: Paths | None = None) -> list[CallRecord]:
    """Records that need a request, in round-robin month order. Stale or error files are deleted first."""
    paths = paths or get_paths()
    pending: list[CallRecord] = []
    for call in calls:
        if ids is not None and call.call_id not in ids:
            continue
        p = load.cache_file(call.call_id, paths)
        redo = force or not _has_valid_cache(call)
        if not redo and force_api and _cached_produced_by(call, paths) != "api":
            redo = True
        if not redo and retry_errors:
            row = load.row_for_call(call, paths)
            redo = row is not None and row["status"] == "error"
        if redo:
            if p.exists():
                os.remove(p)
            pending.append(call)
    return round_robin_by_month(pending)


def read_ids(path: Path) -> set[str]:
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


# --- async run -----------------------------------------------------------------------------

class RunState:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.usage = Usage()
        self.n_ok = 0
        self.n_err = 0
        self.n_cached = 0
        self.budget_hit = False
        self.errors: dict[str, str] = {}
        self.done = 0

    @property
    def est_usd(self) -> float:
        return cost.estimate_usd(self.settings.extract_model, self.usage)


def make_client(settings: Settings, force: bool = False) -> LLMClient:
    """The configured client, always behind the cache layer so fake runs persist files too."""
    client = get_client()
    if isinstance(client, CachedClient):
        return CachedClient(inner=client.inner, write_only=True) if force else client
    return CachedClient(inner=client, write_only=force)


def write_error_marker(req: LLMRequest, error: str, model: str, produced_by: str) -> None:
    """A cache file with response=null: loads as status=error and counts as pending on the next run."""
    payload = {k: v for k, v in req.meta.items() if k != "text"}
    payload.update({"key": req.cache_key, "model": model, "produced_by": produced_by, "created_at": _now(),
                    "usage": None, "response": None, "error": error[:500]})
    atomic_write_json(cache_path(req.stage, req.cache_name or "unknown"), payload)


async def _one(call: CallRecord, client: LLMClient, state: RunState, sem: asyncio.Semaphore, total: int) -> None:
    req = build_request(call)
    async with sem:
        if state.est_usd > state.settings.max_usd:
            state.budget_hit = True
            return
        try:
            result = await client.acomplete_json(req)
            state.usage = state.usage.add(result.usage)
            state.n_ok += 1
            state.n_cached += int(result.cached)
        except Exception as exc:  # per-record failures never abort the run
            state.n_err += 1
            state.errors[call.call_id] = f"{exc.__class__.__name__}: {exc}"
            produced_by = "fake" if state.settings.llm_mode == "fake" else "api"
            write_error_marker(req, state.errors[call.call_id], state.settings.extract_model, produced_by)
        state.done += 1
        if state.done % PROGRESS_EVERY == 0 or state.done == total:
            print(f"  {state.done}/{total} done (ok {state.n_ok}, err {state.n_err}, ~${state.est_usd:.2f})")


async def run_async(records: list[CallRecord], client: LLMClient, settings: Settings) -> RunState:
    state = RunState(settings)
    sem = asyncio.Semaphore(max(1, settings.concurrency))
    await asyncio.gather(*(_one(c, client, state, sem, len(records)) for c in records))
    if state.budget_hit:
        print(f"budget guard: VOC_MAX_USD={settings.max_usd} reached at ~${state.est_usd:.2f}; remaining records skipped")
    return state


def append_run_log(paths: Paths, state: RunState, started_at: str, n_requested: int, args: dict[str, Any]) -> None:
    entry = {"run_id": started_at, "stage": STAGE, "started_at": started_at, "ended_at": _now(),
             "n_requested": n_requested, "n_ok": state.n_ok, "n_err": state.n_err, "n_cached": state.n_cached,
             **state.usage.to_dict(), "est_usd": round(state.est_usd, 4), "budget_hit": state.budget_hit,
             "model": state.settings.extract_model, "llm_mode": state.settings.llm_mode, "args": args}
    paths.work.mkdir(parents=True, exist_ok=True)
    with (paths.work / "extract_runs.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run_extract(records: list[CallRecord], calls: list[CallRecord], *, force: bool, args: dict[str, Any]) -> int:
    """Request every pending record, then consolidate everything into extractions.jsonl."""
    settings, paths = get_settings(), get_paths().ensure()
    started = _now()
    print(f"extract: {len(records)} pending of {len(calls)} calls; mode={settings.llm_mode} "
          f"model={settings.extract_model} concurrency={settings.concurrency}")
    if records and settings.llm_mode != "fake" and not settings.build_key_present:
        print("no ANTHROPIC_API_KEY: records without a cache file will be reported as errors "
              "(use --export for build-time agents or VOC_LLM=fake for a smoke run)")
    state = asyncio.run(run_async(records, make_client(settings, force), settings))
    append_run_log(paths, state, started, len(records), args)
    stats = load.consolidate(calls, paths)
    print(f"run: ok {state.n_ok} (cached {state.n_cached}), errors {state.n_err}, "
          f"tokens in/out {state.usage.input_tokens}/{state.usage.output_tokens}, est ${state.est_usd:.2f}")
    return 0 if stats["n_ok"] or not records else 1


# --- dry run -------------------------------------------------------------------------------

def dry_run(records: list[CallRecord]) -> dict[str, Any]:
    settings = get_settings()
    sample = records[:DRY_RUN_SAMPLE]
    counter = _token_counter(settings)
    system_tokens = counter(build_request(sample[0]).system, ".") if sample else estimate_tokens(build_system_prompt())
    per_record = [max(1, counter(build_request(c).system, build_request(c).user) - system_tokens) for c in sample]
    mean_user = (sum(per_record) / len(per_record)) if per_record else 0.0
    n = len(records)
    usage = Usage(input_tokens=int(mean_user * n), output_tokens=OUTPUT_TOKENS_PER_RECORD * n,
                  cache_read_input_tokens=system_tokens * max(0, n - 1),
                  cache_creation_input_tokens=system_tokens if n else 0)
    est = cost.estimate_usd(settings.extract_model, usage)
    out = {"pending": n, "sampled": len(sample), "system_tokens": system_tokens,
           "mean_record_tokens": round(mean_user, 1), "counted_via": counter.__name__,
           "projected_usage": usage.to_dict(), "model": settings.extract_model,
           "projected_usd": round(est, 2), "budget_usd": settings.max_usd}
    print(json.dumps(out, indent=1))
    if est > settings.max_usd:
        print(f"WARNING: projected ${est:.2f} exceeds VOC_MAX_USD={settings.max_usd}")
    return out


def _token_counter(settings: Settings):
    """messages.count_tokens when Anthropic can be asked, else the 4-chars-per-token estimate.

    OpenRouter exposes no token-counting endpoint, so that provider falls back to the estimate
    rather than reaching for a client it has no key for.
    """
    if settings.can_call_api and settings.build_provider != "openrouter":
        from voc.llm.anthropic_client import AnthropicClient
        api = AnthropicClient()

        def api_count(system: str, user: str) -> int:
            req = build_request(CallRecord.build(call_id="dry", date="2026-01-01", text=user, product="other_or_unspecified"))
            req.system, req.user = system, user
            return api.count_tokens(req)
        return api_count

    def estimate(system: str, user: str) -> int:
        return estimate_tokens(system) + estimate_tokens(user)
    return estimate


# --- Message Batches API (opt-in; implemented but UNTESTED until a key exists) --------------

def run_batch(records: list[CallRecord], calls: list[CallRecord], poll_seconds: int = 30) -> int:
    settings, paths = get_settings(), get_paths().ensure()
    if not settings.can_call_api:
        print("--batch needs ANTHROPIC_API_KEY and VOC_LLM != fake")
        return 2
    import anthropic
    from voc.llm.anthropic_client import _parse, build_kwargs
    from voc.llm.cached_client import write_cache
    print("NOTE: batch mode is implemented but untested (no key on the build machine)")
    by_id = {c.call_id: c for c in records}
    client = anthropic.Anthropic()
    batch = client.messages.batches.create(
        requests=[{"custom_id": c.call_id, "params": build_kwargs(build_request(c))} for c in records])
    print(f"batch {batch.id} submitted with {len(records)} requests")
    while batch.processing_status != "ended":
        time.sleep(poll_seconds)
        batch = client.messages.batches.retrieve(batch.id)
        print(f"  {batch.processing_status}: {batch.request_counts}")
    n_ok = 0
    for item in client.messages.batches.results(batch.id):
        req = build_request(by_id[item.custom_id])
        if item.result.type == "succeeded":
            try:
                write_cache(req.stage, req.cache_name, req.cache_key, _parse(item.result.message, req), req.meta)
                n_ok += 1
                continue
            except Exception as exc:
                write_error_marker(req, f"{exc.__class__.__name__}: {exc}", settings.extract_model, "api")
        else:
            write_error_marker(req, f"batch {item.result.type}: {getattr(item.result, 'error', '')}",
                               settings.extract_model, "api")
    print(f"batch: {n_ok} ok of {len(records)}")
    load.consolidate(calls, paths)
    return 0


# --- report --------------------------------------------------------------------------------

def _share(n: int, d: int) -> float:
    return round(n / d, 4) if d else 0.0


def report(calls: list[CallRecord], paths: Paths | None = None) -> dict[str, Any]:
    """Invariants over extractions.jsonl (DESIGN 5.7 free metrics)."""
    paths = paths or get_paths()
    rows = load.read_jsonl(paths.extractions)
    by_id = {c.call_id: c for c in calls}
    ok = [r for r in rows if r["status"] == "ok" and r["call_id"] in by_id]
    n_topics = sum(len(r["extraction"]["topics"]) for r in ok)
    quotes = [q for r in ok for t in r["extraction"]["topics"] for q in t["evidence"]]
    quotes += [q for r in ok for q in r["extraction"]["positive_moments"]]
    primaries = [next(x["reason"] for x in r["extraction"]["contact_reasons"] if x["is_primary"]) for r in ok]
    agree_n = agree_d = 0
    for r, primary in zip(ok, primaries):
        call = by_id[r["call_id"]]
        mapped = tx.map_issue_to_reasons(call.issue_raw, call.sub_issue_raw)
        if mapped:
            agree_d += 1
            agree_n += int(primary in mapped)
    prod_hits = sum(1 for r in ok if by_id[r["call_id"]].product in r["extraction"]["products"])
    hist = Counter(r["extraction"]["overall_sentiment"] for r in ok)
    flags = Counter(f for r in rows for f in r.get("flags", []))
    out = {
        "n_calls": len(calls), "n_ok": len(ok),
        "n_error": sum(1 for r in rows if r["status"] not in ("ok", "stale")),
        "n_stale": sum(1 for r in rows if r["status"] == "stale"),
        "n_missing": len(calls) - len(rows),
        "share_other_or_unclear": _share(sum(1 for p in primaries if p == "other_or_unclear"), len(ok)),
        "quote_verify_rate": _share(sum(q["verified"] for q in quotes), len(quotes)),
        "topics_per_call": round(n_topics / len(ok), 2) if ok else 0.0,
        "sentiment_histogram": {str(k): hist[k] for k in sorted(hist)},
        "primary_reason_agreement": _share(agree_n, agree_d), "primary_reason_agreement_n": agree_d,
        "product_agreement": _share(prod_hits, len(ok)),
        "redaction_heavy_share": _share(sum(1 for r in ok if r["extraction"]["redaction_heavy"]), len(ok)),
        "produced_by": dict(Counter(r.get("produced_by") for r in rows)),
        "flags": dict(sorted(flags.items())),
        "errors": [{"call_id": r["call_id"], "error": r["error"]}
                   for r in rows if r["status"] not in ("ok", "stale")][:20],
        "stale": [r["call_id"] for r in rows if r["status"] == "stale"][:20],
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    paths.work.mkdir(parents=True, exist_ok=True)
    atomic_write_json(paths.work / "extract_report.json", out)
    return out
