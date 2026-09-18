"""`voc warm-answers`: record every demo question live (needs an API key) so the demo replays instantly."""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

from voc.agent.service import collect, stream_answer
from voc.config import get_settings
from voc.questions import load_questions
from voc.store.db import connect, db_exists


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("warm-answers", help="Re-record the demo questions live and cache them")
    p.add_argument("path", nargs="?", default=None, help="questions file (default questions/demo.yaml)")
    p.add_argument("--effort", default="high")
    p.add_argument("--include-aliases", action="store_true")
    p.add_argument("--include-followups", action="store_true")
    p.add_argument("--only", default=None, help="comma-separated question ids")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    settings = get_settings()
    if not settings.can_ask_live:
        print("warm-answers needs ANTHROPIC_API_KEY (and VOC_LLM != fake)", file=sys.stderr)
        return 2
    if not db_exists():
        print("no index found: run `voc build-db` first", file=sys.stderr)
        return 2
    import os
    os.environ["VOC_ASK_EFFORT"] = args.effort
    from voc.config import reset_settings_cache
    reset_settings_cache()

    questions = load_questions(Path(args.path) if args.path else None)
    only = set(args.only.split(",")) if args.only else None
    con = connect()
    todo: list[tuple[str, dict[str, Any]]] = []
    for q in questions:
        if only and q["id"] not in only:
            continue
        todo.append((q["question"], q.get("filters") or {}))
        if args.include_aliases:
            todo += [(a, q.get("filters") or {}) for a in q["aliases"]]
        if args.include_followups:
            todo += [(f, q.get("filters") or {}) for f in q["followups"]]
    ok = 0
    for question, filters in todo:
        print(f"\n=== {question}")
        events = asyncio.run(collect(stream_answer(question, filters, con, fresh=True)))
        answer = next((p.get("answer") for n, p in events if n == "answer"), None)
        if answer and answer.get("mode") == "live":
            ok += 1
            print(f"  recorded · {answer['confidence']['badge']} · {len(answer.get('claims', []))} claims · {len(answer.get('quotes', []))} quotes")
        else:
            print(f"  FAILED: mode={answer.get('mode') if answer else None}")
    print(f"\n{ok}/{len(todo)} answers recorded")
    return 0 if ok == len(todo) else 1
