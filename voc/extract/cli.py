"""`voc extract` sub-command."""
from __future__ import annotations

import argparse
from pathlib import Path

from voc.extract import bundles, load, runner
from voc.paths import get_paths


def add_parser(subparsers) -> None:
    p = subparsers.add_parser("extract", help="read every call into the extraction schema (step 1)")
    p.add_argument("--limit", type=int, default=None, help="process at most N pending records")
    p.add_argument("--ids", type=Path, default=None, help="file with one call_id per line")
    p.add_argument("--retry-errors", action="store_true", help="re-request records whose cache file fails validation")
    p.add_argument("--force", action="store_true", help="ignore existing cache files")
    p.add_argument("--force-api", action="store_true", help="re-extract agent/fake-produced records via the API")
    p.add_argument("--dry-run", action="store_true", help="count tokens on a sample and print the projected cost")
    p.add_argument("--batch", action="store_true", help="use the Message Batches API (opt-in, untested without a key)")
    p.add_argument("--export", type=Path, default=None, metavar="DIR", help="write bundles for build-time agents")
    p.add_argument("--bundle-size", type=int, default=20)
    p.add_argument("--load", action="store_true", help="only consolidate cache files into extractions.jsonl")
    p.add_argument("--report", action="store_true", help="print invariants over extractions.jsonl")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    paths = get_paths().ensure()
    calls = load.load_calls(paths.calls)
    if args.load:
        load.consolidate(calls, paths)
        return 0
    if args.report:
        runner.report(calls, paths)
        return 0
    ids = runner.read_ids(args.ids) if args.ids else None
    if args.export:
        pending = runner.select_pending(calls, ids=ids, force=args.force, paths=paths)
        bundles.export_bundles(pending[: args.limit] if args.limit else pending, args.export, args.bundle_size)
        return 0
    pending = runner.select_pending(calls, ids=ids, retry_errors=args.retry_errors, force=args.force,
                                    force_api=args.force_api, paths=paths)
    if args.limit:
        pending = pending[: args.limit]
    if args.dry_run:
        runner.dry_run(pending)
        return 0
    if args.batch:
        return runner.run_batch(pending, calls)
    cli_args = {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items() if k != "func"}
    return runner.run_extract(pending, calls, force=args.force, args=cli_args)
