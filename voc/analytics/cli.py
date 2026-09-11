"""`voc trends`: materialise entity_period, entity_dim and emerging_scores from the index."""
from __future__ import annotations

import argparse
import sys
from typing import Any

from voc.paths import get_paths
from voc.store.db import connect


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("trends", help="Materialise trend, segment and emerging-issue tables")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from voc.analytics.materialize import materialize

    paths = get_paths()
    if not paths.sqlite.exists():
        print("no index found: run `voc build-db` first", file=sys.stderr)
        return 2
    con = connect(paths.sqlite)
    counts = materialize(con, quiet=args.quiet)
    con.commit()
    if not args.quiet:
        print("materialised: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return 0
