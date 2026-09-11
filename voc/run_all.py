"""`voc run-all`: the whole pipeline end to end. With VOC_LLM=fake this is the CI smoke test."""
from __future__ import annotations

import argparse
import sys
import time
from typing import Any

from voc.config import get_settings
from voc.paths import get_paths


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("run-all", help="ingest -> extract -> theme -> build-db -> qa in one command")
    p.add_argument("--limit", type=int, default=None, help="extract at most N calls")
    p.add_argument("--skip-ingest", action="store_true", help="use the existing data/calls.jsonl")
    p.add_argument("--target", type=int, default=None)
    p.add_argument("--start", default=None)
    p.add_argument("--end", default=None)
    p.set_defaults(func=run)


def _step(name: str, fn, *args, **kwargs) -> Any:
    print(f"\n=== {name} ===")
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    print(f"--- {name} done in {time.perf_counter() - t0:.1f}s")
    return out


def run(args: argparse.Namespace) -> int:
    from voc.extract import load as extract_load
    from voc.extract import runner as extract_runner
    from voc.llm.client import LLMCacheMiss, get_client
    from voc.store.build import build
    from voc.theme.registry import RunStats, ThemeOptions

    settings = get_settings()
    paths = get_paths().ensure()

    if not args.skip_ingest:
        if not paths.calls.exists():
            from voc.ingest import cfpb, sample
            start = args.start or "2024-07"
            end = args.end or "2026-06"
            _step("ingest pull", cfpb.pull, paths, settings.company, start, end)
            _step("ingest sample", sample.sample, paths, settings.company, start, end,
                  target=args.target or settings.target_calls, seed=settings.seed)
        else:
            print(f"using existing {paths.calls}")

    client = get_client()
    calls = extract_load.load_calls(paths.calls)

    def _extract() -> int:
        pending = extract_runner.select_pending(calls, paths=paths)
        if args.limit:
            pending = pending[: args.limit]
        return extract_runner.run_extract(pending, calls, force=False, args={"limit": args.limit})

    try:
        _step("extract", _extract)
    except LLMCacheMiss as exc:
        print(f"extraction needs model output: {exc}\n"
              f"Export work bundles with `voc extract --export data/work/extract_bundles`.", file=sys.stderr)
        return 3

    from voc.theme import consolidate as consolidate_mod
    from voc.theme import reassign as reassign_mod
    from voc.theme import seed as seed_mod
    from voc.theme import stability as stability_mod

    opts = ThemeOptions()
    for name, fn in (("theme seed", seed_mod.run_seed), ("theme consolidate", consolidate_mod.run_consolidate),
                     ("theme reassign", reassign_mod.run_reassign), ("theme stability", stability_mod.run_stability)):
        try:
            _step(name, fn, paths, client, RunStats(), opts)
        except LLMCacheMiss as exc:
            print(f"{name} needs model output: {exc}\n"
                  f"Export bundles with `voc theme export --dir data/work/theme_bundles`.", file=sys.stderr)
            return 3

    meta = _step("build-db", build, paths, True, False)
    from voc.qa import report as qa_report
    _step("qa", qa_report, argparse.Namespace(qa_cmd="report"))
    print(f"\nready: {meta.get('n_calls', '?')} calls, data_version {meta.get('data_version')}, "
          f"as_of {meta.get('as_of_week')}\nrun `python -m voc serve`")
    return 0
