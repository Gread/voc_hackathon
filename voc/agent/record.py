"""`voc record-answer`: record a demo answer without an API key. A build-time Claude agent works the
question through `voc tool ... --session <file>` and writes an Answer JSON; finalize runs the same
verifier as live answers and stores the result with mode="recorded"."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voc.agent import cache as cache_mod
from voc.agent.answer import verify_answer
from voc.agent.service import build_context, scope_note
from voc.paths import get_paths
from voc.schemas.answer import ASK_PROMPT_VERSION, Answer, clip_answer
from voc.schemas.filters import Filters
from voc.store.db import connect, db_exists

RECORD_MODEL = "claude-agent-build"


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("record-answer", help="Record demo answers without an API key")
    sub = p.add_subparsers(dest="record_cmd", required=True)
    s = sub.add_parser("start", help="open a recording session and print the agent instructions")
    s.add_argument("--question", required=True)
    s.add_argument("--filters", default="{}")
    s.add_argument("--as-of", dest="as_of", default=None)
    s.add_argument("--session-id", default=None)
    s.set_defaults(func=start)
    f = sub.add_parser("finalize", help="verify the recorded session and store the answer")
    f.add_argument("session_id")
    f.add_argument("--model", default=RECORD_MODEL)
    f.add_argument("--allow-unverified-headline", action="store_true")
    f.set_defaults(func=finalize)
    ls = sub.add_parser("list", help="list recording sessions")
    ls.set_defaults(func=list_sessions)


def recording_dir() -> Path:
    d = get_paths().work / "recording"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def start(args: argparse.Namespace) -> int:
    if not db_exists():
        print("no index found: run `voc build-db` first", file=sys.stderr)
        return 2
    con = connect()
    filters = Filters.from_any(json.loads(args.filters or "{}"))
    ctx = build_context(con, args.as_of)
    qh = cache_mod.qhash(args.question, filters, ctx.as_of_week, ctx.data_version)
    session_id = args.session_id or f"{_slug(args.question)}-{qh[:6]}"
    d = recording_dir()
    meta = {"session_id": session_id, "question": args.question, "filters": filters.canonical(),
            "as_of_week": ctx.as_of_week, "data_version": ctx.data_version, "qhash": qh,
            "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    (d / f"{session_id}.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    tools_file = d / f"{session_id}.tools.jsonl"
    answer_file = d / f"{session_id}.answer.json"
    tools_file.touch()
    print(json.dumps({
        "session_id": session_id, "qhash": qh, "as_of_week": ctx.as_of_week, "data_version": ctx.data_version,
        "tools_file": str(tools_file), "answer_file": str(answer_file),
        "instructions": [
            f"Call the analysis tools with: python -m voc tool <name> --args '<json>' --session \"{tools_file}\" (add --as-of {ctx.as_of_week} where relevant).",
            "Use at most 8 tool calls; every number in the answer must come from a tool result and cite its result_id.",
            f"When done, write the Answer JSON (schema: voc.schemas.answer.ANSWER_API_SCHEMA) to {answer_file}.",
            f"Then run: python -m voc record-answer finalize {session_id}",
        ],
    }, indent=1))
    return 0


def _load_session(session_id: str) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    d = recording_dir()
    meta = json.loads((d / f"{session_id}.json").read_text(encoding="utf-8"))
    calls: list[dict[str, Any]] = []
    tools_file = d / f"{session_id}.tools.jsonl"
    if tools_file.exists():
        for line in tools_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                calls.append(json.loads(line))
    answer_file = d / f"{session_id}.answer.json"
    if not answer_file.exists():
        raise FileNotFoundError(f"missing {answer_file}")
    answer = json.loads(answer_file.read_text(encoding="utf-8"))
    return meta, calls, answer


def trace_from_calls(calls: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Rebuild the event trace and the result map from the tool session lines."""
    events: list[dict[str, Any]] = [{"name": "status", "payload": {"text": "reading the question"}, "t_ms": 0}]
    results: dict[str, dict[str, Any]] = {}
    for i, c in enumerate(calls):
        t = int(c.get("t_ms") or (i + 1) * 1500)
        env = c.get("result") or {}
        rid = env.get("result_id") or c.get("result_id") or f"r{i + 1}"
        env["result_id"] = rid
        results[rid] = env
        events.append({"name": "tool_call", "payload": {"id": f"toolu_{i + 1}", "name": c.get("tool"), "args": c.get("args", {})}, "t_ms": t})
        rows = env.get("rows") if isinstance(env.get("rows"), list) else None
        events.append({"name": "tool_result", "payload": {"id": f"toolu_{i + 1}", "result_id": rid, "name": c.get("tool"),
                                                          "summary": env.get("summary", ""), "n_rows": len(rows) if rows is not None else None,
                                                          "sql": env.get("sql", [])}, "t_ms": t + 400})
    events.append({"name": "status", "payload": {"text": "answer submitted"}, "t_ms": (events[-1]["t_ms"] + 800) if events else 0})
    return events, results


def finalize(args: argparse.Namespace) -> int:
    meta, calls, raw_answer = _load_session(args.session_id)
    con = connect()
    ctx = build_context(con, meta.get("as_of_week"))
    if ctx.data_version != meta.get("data_version"):
        print(f"data_version changed since the session started ({meta.get('data_version')} -> {ctx.data_version}); "
              f"re-run the tools before finalizing", file=sys.stderr)
        return 2
    filters = Filters.from_any(meta.get("filters") or {})
    try:
        answer = clip_answer(Answer.model_validate(raw_answer))
    except Exception as exc:
        print(f"answer JSON invalid: {exc}", file=sys.stderr)
        return 2
    events, results = trace_from_calls(calls)
    # the tool CLI already persisted tool_results rows; results here are the envelopes for verification
    note, _ = scope_note(con, filters)
    verified = verify_answer(answer, results, con, as_of_week=ctx.as_of_week, data_version=ctx.data_version,
                             mode="recorded", model=args.model, qhash=meta["qhash"],
                             footnote=ctx.footnote, scope_note=note)
    report = verified.validation
    headline_unverified = any((not c.verified) and c.headline for c in verified.claims)
    print(json.dumps({"claims": [{"id": c.id, "verified": c.verified, "n": c.verified_n, "badge": c.confidence.badge if c.confidence else "",
                                  "flags": c.flags} for c in verified.claims],
                      "quotes_kept": len(verified.quotes), "quotes_dropped": len(report.get("dropped_quotes", [])),
                      "number_mismatches": report.get("number_mismatches", []),
                      "unlinked_numbers": report.get("unlinked_numbers", []),
                      "confidence": verified.confidence.badge}, indent=1, ensure_ascii=False))
    if headline_unverified and not args.allow_unverified_headline:
        print("headline claim is not supported by the recorded tool results; fix the answer JSON "
              "(cite the right result_ids / call_ids) and finalize again", file=sys.stderr)
        return 1
    stored = cache_mod.StoredAnswer(
        qhash=meta["qhash"], question=meta["question"], filters=filters.canonical(), as_of_week=ctx.as_of_week,
        data_version=ctx.data_version, prompt_version=ASK_PROMPT_VERSION, mode="recorded", model=args.model,
        effort="high", answer=verified.model_dump(), trace=events, validation=report)
    path = cache_mod.save_answer(con, stored)
    print(f"stored {path}")
    return 0


def list_sessions(args: argparse.Namespace) -> int:
    d = recording_dir()
    for p in sorted(d.glob("*.json")):
        if p.name.endswith(".answer.json"):
            continue
        meta = json.loads(p.read_text(encoding="utf-8"))
        has_answer = (d / f"{meta['session_id']}.answer.json").exists()
        stored = cache_mod.answer_path(meta["qhash"]).exists()
        print(f"{meta['session_id']:<50} answer={'yes' if has_answer else 'no ':<3} stored={'yes' if stored else 'no'}  {meta['question'][:60]}")
    return 0
