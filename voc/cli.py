"""Command-line entry point. Each stage registers its own sub-parser lazily so
lanes can be developed independently; a missing stage shows up as a stub."""
from __future__ import annotations

import argparse
import importlib
import sys

# (subcommand, module exposing add_parser(subparsers) and setting args.func)
STAGES = [
    ("ingest", "voc.ingest.cli"),
    ("extract", "voc.extract.cli"),
    ("theme", "voc.theme.cli"),
    ("trends", "voc.analytics.cli"),
    ("build-db", "voc.store.cli"),
    ("qa", "voc.qa"),
    ("tool", "voc.agent.tool_cli"),
    ("ask", "voc.agent.ask_cli"),
    ("record-answer", "voc.agent.record"),
    ("warm-answers", "voc.agent.warm"),
    ("serve", "voc.api.cli"),
    ("run-all", "voc.run_all"),
]


def _register_stub(subparsers, name: str, error: Exception) -> None:
    p = subparsers.add_parser(name, help=f"(unavailable: {error.__class__.__name__})")
    p.set_defaults(_stub_error=f"{error.__class__.__name__}: {error}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="voc", description="Voice of the Customer Insights PoC")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, module_path in STAGES:
        try:
            module = importlib.import_module(module_path)
            module.add_parser(sub)
        except Exception as exc:  # stage not implemented yet or import error
            _register_stub(sub, name, exc)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if getattr(args, "_stub_error", None):
        print(f"{args.command} is not available ({args._stub_error})", file=sys.stderr)
        return 2
    return int(args.func(args) or 0)
