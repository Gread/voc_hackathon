"""`voc ask "question"`: run the ask service from the shell and print the verified answer."""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

from voc.agent.service import collect, stream_answer
from voc.store.db import connect, db_exists


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("ask", help="Ask a plain-language question (live, recorded or templated)")
    p.add_argument("question")
    p.add_argument("--filters", default="{}", help="JSON filters, e.g. '{\"product\": [\"credit_card\"]}'")
    p.add_argument("--as-of", dest="as_of", default=None, help="ISO week, e.g. 2026-W26")
    p.add_argument("--fresh", action="store_true", help="ignore recorded answers")
    p.add_argument("--json", action="store_true", help="print the verified answer as JSON")
    p.add_argument("--quiet", action="store_true", help="hide the tool trace")
    p.set_defaults(func=run)


def print_answer(answer: dict[str, Any]) -> None:
    conf = answer.get("confidence") or {}
    print(f"\n[{answer.get('mode', '?')} · {answer.get('model', '')}] confidence: {conf.get('badge', conf.get('tier', ''))}\n")
    print(answer.get("answer_markdown", ""))
    for c in answer.get("claims", []):
        badge = (c.get("confidence") or {}).get("badge", "")
        mark = "" if c.get("verified", True) else "  [NOT SUPPORTED BY RETRIEVED DATA]"
        print(f"  [{c['id']}] {c['statement']}  -- {badge}{mark}")
        for corr in c.get("corrections", []):
            print(f"        correction: {corr}")
    for q in answer.get("quotes", []):
        print(f'  "{q["quote"]}"  ({q["call_id"]})')
    if answer.get("caveats"):
        print("  caveats: " + " | ".join(answer["caveats"]))
    if answer.get("coverage_line"):
        print("  " + answer["coverage_line"])
    if answer.get("footnote"):
        print("  " + answer["footnote"])


def run(args: argparse.Namespace) -> int:
    if not db_exists():
        print("no index found: run `voc build-db` first", file=sys.stderr)
        return 2
    con = connect()
    filters = json.loads(args.filters or "{}")
    events = asyncio.run(collect(stream_answer(args.question, filters, con, as_of=args.as_of, fresh=args.fresh)))
    answer: dict[str, Any] | None = None
    for name, payload in events:
        if name == "answer":
            answer = payload.get("answer")
        elif not args.quiet and name in ("status", "tool_call", "tool_result", "error"):
            if name == "tool_call":
                print(f"  -> {payload.get('name')}({json.dumps(payload.get('args', {}), ensure_ascii=False)[:120]})")
            elif name == "tool_result":
                print(f"     {payload.get('result_id', '')}: {payload.get('summary', '')[:160]}")
            else:
                print(f"  {name}: {payload.get('text') or payload.get('message', '')}")
    if answer is None:
        print("no answer produced", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(answer, ensure_ascii=False, indent=1))
    else:
        print_answer(answer)
    return 0
