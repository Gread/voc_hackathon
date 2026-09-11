"""`voc theme seed|consolidate|reassign|stability|run|export|import`."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from voc.llm.client import LLMCacheMiss, get_client
from voc.paths import get_paths
from voc.theme.registry import RunStats, ThemeOptions

PASSES = ("seed", "consolidate", "reassign", "stability")


def _options(args: argparse.Namespace) -> ThemeOptions:
    return ThemeOptions(
        batch_size=getattr(args, "batch_size", 100),
        concurrency=getattr(args, "concurrency", 4),
        limit_buckets=getattr(args, "limit_buckets", None),
        on_miss=("skip" if getattr(args, "skip_missing", False) else "raise"),
    )


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("theme", help="Group topics into themes (seed, consolidate, reassign, stability)")
    sub = p.add_subparsers(dest="theme_cmd", required=True)
    for name in PASSES:
        s = sub.add_parser(name, help=f"theming pass: {name}")
        _common(s)
        s.set_defaults(func=run_pass, pass_name=name)
    r = sub.add_parser("run", help="seed -> consolidate -> reassign -> stability")
    _common(r)
    r.set_defaults(func=run_all_passes)
    e = sub.add_parser("export", help="write work bundles for build-time agents")
    _common(e)
    e.add_argument("--dir", required=True)
    e.add_argument("--pass", dest="pass_name", default="seed", choices=PASSES)
    e.set_defaults(func=run_export)
    # export is iterative: one wave per call, because a batch identity depends on earlier batches
    i = sub.add_parser("import", help="load agent-written cache files and continue the pass")
    _common(i)
    i.add_argument("--dir", required=True)
    i.add_argument("--pass", dest="pass_name", default="seed", choices=PASSES)
    i.set_defaults(func=run_import)


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--batch-size", type=int, default=100)
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--limit-buckets", type=int, default=None)
    p.add_argument("--skip-missing", action="store_true", help="leave buckets pending instead of failing on a cache miss")


def _run_one(pass_name: str, args: argparse.Namespace) -> int:
    from voc.theme import consolidate as consolidate_mod
    from voc.theme import reassign as reassign_mod
    from voc.theme import seed as seed_mod
    from voc.theme import stability as stability_mod

    paths = get_paths().ensure()
    if not paths.extractions.exists():
        print(f"no extractions at {paths.extractions}: run `voc extract` first", file=sys.stderr)
        return 2
    client = get_client()
    stats = RunStats()
    opts = _options(args)
    runner = {"seed": seed_mod.run_seed, "consolidate": consolidate_mod.run_consolidate,
              "reassign": reassign_mod.run_reassign, "stability": stability_mod.run_stability}[pass_name]
    try:
        runner(paths, client, stats, opts)
    except LLMCacheMiss as exc:
        print(f"cache miss: {exc}\nExport bundles with `voc theme export --dir <dir> --pass {pass_name}` "
              f"or set ANTHROPIC_API_KEY.", file=sys.stderr)
        return 3
    print(f"{pass_name}: {stats.summary()}")
    return 0


def run_pass(args: argparse.Namespace) -> int:
    return _run_one(args.pass_name, args)


def run_all_passes(args: argparse.Namespace) -> int:
    for name in PASSES:
        code = _run_one(name, args)
        if code:
            return code
    return 0


def run_export(args: argparse.Namespace) -> int:
    from voc.theme.bundles import export_bundles

    n = export_bundles(Path(args.dir), args.pass_name, _options(args))
    print(f"wrote {n} bundle(s) to {args.dir}")
    return 0


def run_import(args: argparse.Namespace) -> int:
    """Agent-written cache files are replayed by the cached client, so import = re-run the pass."""
    from voc.theme.bundles import verify_bundle_cache

    missing = verify_bundle_cache(Path(args.dir))
    if missing:
        print(f"{len(missing)} cache file(s) still missing, first: {missing[0]}", file=sys.stderr)
        return 3
    return _run_one(args.pass_name, args)
