"""`voc ingest pull|profile|sample|transcripts` sub-commands."""
from __future__ import annotations

import argparse
from pathlib import Path

from voc.config import get_settings
from voc.paths import get_paths

# Window decided for the demo corpus (24 full months).
DEFAULT_START = "2024-07"
DEFAULT_END = "2026-06"


def _window_args(p: argparse.ArgumentParser) -> None:
    s = get_settings()
    p.add_argument("--company", default=s.company, help="exact CFPB company name")
    p.add_argument("--start", default=DEFAULT_START, help="first month YYYY-MM")
    p.add_argument("--end", default=DEFAULT_END, help="last month YYYY-MM (inclusive)")


def cmd_pull(args: argparse.Namespace) -> int:
    from voc.ingest.cfpb import pull
    pull(get_paths().ensure(), args.company, args.start, args.end, force=args.force)
    return 0


def cmd_profile(args: argparse.Namespace) -> int:
    from voc.ingest.profile import build_profile, format_table
    profile = build_profile(get_paths().ensure(), args.company, args.start, args.end,
                            target=args.target, min_words=args.min_words)
    print(format_table(profile))
    print(f"-> {get_paths().profile}")
    return 0 if profile["gate"]["pass"] else 1


def cmd_sample(args: argparse.Namespace) -> int:
    from voc.ingest.sample import sample
    sample(get_paths().ensure(), args.company, args.start, args.end,
           target=args.target, seed=args.seed, min_words=args.min_words)
    return 0


def cmd_transcripts(args: argparse.Namespace) -> int:
    from voc.ingest.transcripts import ingest_transcripts
    ingest_transcripts(get_paths().ensure(), Path(args.path), source=args.source, company=args.company)
    return 0


def add_parser(subparsers) -> None:
    s = get_settings()
    parser = subparsers.add_parser("ingest", help="pull CFPB narratives, profile, sample, add transcripts")
    sub = parser.add_subparsers(dest="ingest_command", required=True)

    p = sub.add_parser("pull", help="pull raw narratives month by month into data/raw/cfpb/")
    _window_args(p)
    p.add_argument("--force", action="store_true", help="re-fetch months already cached")
    p.set_defaults(func=cmd_pull)

    p = sub.add_parser("profile", help="counts per month/week/product/segment + sampling gate")
    _window_args(p)
    p.add_argument("--target", type=int, default=s.target_calls)
    p.add_argument("--min-words", type=int, default=30)
    p.set_defaults(func=cmd_profile)

    p = sub.add_parser("sample", help="constant-fraction sampling -> data/calls.jsonl")
    _window_args(p)
    p.add_argument("--target", type=int, default=s.target_calls)
    p.add_argument("--seed", type=int, default=s.seed)
    p.add_argument("--min-words", type=int, default=30)
    p.set_defaults(func=cmd_sample)

    p = sub.add_parser("transcripts", help="merge a multi-turn transcript corpus into data/calls.jsonl")
    p.add_argument("--path", required=True, help="a .jsonl file or a directory of .jsonl files")
    p.add_argument("--source", default="conv", help="source name and call_id prefix")
    p.add_argument("--company", default="unknown")
    p.set_defaults(func=cmd_transcripts)
