"""`voc build-db`: rebuild the SQLite index from the files under data/."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from voc.paths import get_paths


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("build-db", help="Rebuild data/voc.sqlite from the files under data/")
    p.add_argument("--data-dir", default=None, help="override VOC_DATA_DIR")
    p.add_argument("--no-trends", action="store_true", help="skip the analytics materialisation")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from voc.store.build import BuildRefused, build

    paths = get_paths(Path(args.data_dir) if args.data_dir else None)
    if not paths.calls.exists():
        print(f"no calls file at {paths.calls}: run `voc ingest sample` first", file=sys.stderr)
        return 2
    try:
        meta = build(paths, run_trends=not args.no_trends, quiet=args.quiet)
    except BuildRefused as exc:
        print(f"build refused: {exc}", file=sys.stderr)
        return 2
    if not args.quiet:
        print(f"built {paths.sqlite} · data_version {meta.get('data_version')} · as_of {meta.get('as_of_week')}")
    return 0
