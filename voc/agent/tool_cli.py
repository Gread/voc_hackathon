"""`voc tool <name> --args '<json>'`: the agent's tools from the shell, used when a build-time agent
records a demo answer without an API key."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from voc.agent.tools import DISPATCH, READ_TOOLS, TOOL_SPECS, ToolContext, run_tool
from voc.store.db import connect, db_exists, get_meta


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("tool", help="Run one analysis tool and print its result envelope")
    p.add_argument("name", help="tool name, or 'list'")
    p.add_argument("--args", default="{}", help="tool arguments as JSON")
    p.add_argument("--as-of", dest="as_of", default=None, help="ISO week, e.g. 2026-W26")
    p.add_argument("--session", default=None, help="append the call and its result to this JSONL session file")
    p.add_argument("--compact", action="store_true", help="print without indentation")
    p.set_defaults(func=run)


def _list_tools() -> int:
    for spec in TOOL_SPECS:
        print(f"{spec['name']:<20} {spec['description'].split('.')[0]}.")
        print(f"{'':<20} args: {', '.join(spec['input_schema']['properties'])}")
    return 0


def _session_qhash(session_path: Path | None) -> str:
    """Persist under the recording session's own qhash, which is what finalize verifies against.
    Result ids restart at r1 per session, so a shared qhash lets one recording overwrite another's."""
    if session_path is None:
        return "cli"
    meta = session_path.parent / (session_path.name.removesuffix(".tools.jsonl") + ".json")
    try:
        return json.loads(meta.read_text(encoding="utf-8"))["qhash"]
    except (OSError, ValueError, KeyError):
        return session_path.stem


def run(args: argparse.Namespace) -> int:
    if args.name in ("list", "--list"):
        return _list_tools()
    if args.name not in DISPATCH:
        print(f"unknown tool {args.name}; available: {', '.join(READ_TOOLS)}", file=sys.stderr)
        return 2
    if not db_exists():
        print("no index found: run `voc build-db` first", file=sys.stderr)
        return 2
    try:
        tool_args = json.loads(args.args or "{}")
    except json.JSONDecodeError as exc:
        print(f"--args is not valid JSON: {exc}", file=sys.stderr)
        return 2

    con = connect()
    session_path = Path(args.session) if args.session else None
    ctx = ToolContext(con=con, qhash=_session_qhash(session_path),
                      as_of_week=args.as_of or get_meta(con, "as_of_week"))
    if session_path and session_path.exists():
        ctx.counter = sum(1 for line in session_path.read_text(encoding="utf-8").splitlines() if line.strip())
    t0 = time.monotonic()
    try:
        envelope = run_tool(args.name, tool_args, con, ctx)
    except Exception as exc:
        print(f"{args.name} failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(envelope, ensure_ascii=False, indent=None if args.compact else 1, default=str))
    if session_path:
        session_path.parent.mkdir(parents=True, exist_ok=True)
        line = {"seq": ctx.counter, "t_ms": int((time.monotonic() - t0) * 1000) + ctx.counter * 1500,
                "tool": args.name, "args": tool_args, "result_id": envelope["result_id"], "result": envelope}
        with session_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")
    return 0
