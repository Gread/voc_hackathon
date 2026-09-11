"""Ask service used by POST /api/ask and `voc ask`: live agent, recorded replay, or templated fallback,
all streamed as the same event vocabulary and all passed through the same verifier."""
from __future__ import annotations

import asyncio
import json
import sqlite3
from dataclasses import dataclass
from typing import Any, AsyncIterator, Callable

from voc.agent import cache as cache_mod
from voc.agent.answer import text_only_answer, verify_answer
from voc.agent.runner import AgentEvent, AgentRun, run_agent
from voc.config import get_settings
from voc.paths import get_paths
from voc.schemas.answer import ASK_PROMPT_VERSION, Answer, VerifiedAnswer
from voc.schemas.filters import Filters
from voc.store.db import get_meta

EVENT_NAMES = ("status", "thinking", "tool_call", "tool_result", "answer_delta", "answer", "error", "done")


def encode_event(name: str, payload: dict[str, Any]) -> bytes:
    try:
        from voc.api.sse import encode_event as _enc
        return _enc(name, payload)
    except ImportError:
        return f"event: {name}\ndata: {json.dumps(payload, ensure_ascii=False, default=str)}\n\n".encode("utf-8")


@dataclass
class AskContext:
    con: sqlite3.Connection
    data_version: str
    as_of_week: str
    caveats: str
    footnote: str
    llm_mode: str


def build_context(con: sqlite3.Connection, as_of: str | None = None) -> AskContext:
    data_version = get_meta(con, "data_version", "") or ""
    as_of_week = as_of or get_meta(con, "as_of_week", "") or ""
    return AskContext(con=con, data_version=data_version, as_of_week=as_of_week,
                      caveats=caveats_text(con), footnote=footnote_text(con), llm_mode=get_meta(con, "llm_mode", "") or "")


def _meta_json(con: sqlite3.Connection, key: str) -> Any:
    raw = get_meta(con, key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return raw


def caveats_text(con: sqlite3.Connection) -> str:
    """The data block of the system prompt, rendered once per server start (stable for caching)."""
    prof: dict[str, Any] = {}
    p = get_paths().profile
    if p.exists():
        try:
            prof = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            prof = {}
    n_calls = get_meta(con, "n_calls", "?")
    company = prof.get("company") or get_meta(con, "company", "one bank")
    window = prof.get("window") or {}
    start, end = window.get("start", "?"), window.get("end", "?")
    frac = prof.get("sampling_fraction")
    frac_txt = f"sampled at a constant {frac:.0%} of that bank's narrative complaints per month" if isinstance(frac, (int, float)) else "sampled at a constant fraction per month"
    lines = [
        f"- Source: real, public consumer complaint narratives (US CFPB Consumer Complaint Database) about {company}.",
        f"- Scope: {n_calls} contacts received between {start} and {end}, {frac_txt}; every record is a real complaint written by the customer.",
        "- Dates are the date the regulator received the complaint, which lags the underlying contact by days to weeks.",
        "- Redactions such as XXXX and XX/XX/XXXX are the regulator's; they prove the text is real and must be kept in quotes.",
        "- The corpus is complaints: satisfaction findings are positive moments inside complaints, not a measure of overall satisfaction.",
        "- Channel is single-valued (web) in this corpus; product, segment and region group are the meaningful breakdown dimensions.",
    ]
    return "\n".join(lines)


def _meta_float(con: sqlite3.Connection, key: str) -> float | None:
    """Meta values are JSON, so a missing metric reads back as the literal 'null'."""
    raw = get_meta(con, key)
    if raw in (None, "", "null", "None"):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def footnote_text(con: sqlite3.Connection) -> str:
    parts = []
    golden = _meta_float(con, "qa_golden_primary_accuracy")
    agreement = _meta_float(con, "qa_reason_agreement")
    quotes = _meta_float(con, "qa_quote_verify_rate")
    if golden is not None:
        parts.append(f"extraction spot-check: primary reason accuracy {golden:.2f}")
    if agreement is not None:
        parts.append(f"agreement with the customers' own complaint category {agreement:.2f}")
    if quotes is not None:
        parts.append(f"quotes verified {quotes:.1%}")
    return "; ".join(parts)


def scope_note(con: sqlite3.Connection, filters: Filters) -> tuple[str, int]:
    try:
        from voc.store.queries import filters_where
        where, params = filters_where(filters, "c")
        n = con.execute(f"SELECT COUNT(*) AS n FROM calls c WHERE {where}", params).fetchone()["n"]
    except Exception:
        n = con.execute("SELECT COUNT(*) AS n FROM calls").fetchone()["n"]
    return f"based on {n:,} calls in scope ({filters.describe()})", int(n)


def _to_dict(ev: AgentEvent) -> dict[str, Any]:
    return {"name": ev.name, "payload": ev.payload, "t_ms": ev.t_ms}


def _templated(question: str, filters: Filters, ctx: AskContext, run: AgentRun | None, reason: str) -> tuple[Answer, dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Offline analyst if available, else the minimal wrap of whatever the run produced."""
    results = dict(run.results) if run else {}
    events: list[dict[str, Any]] = []
    try:
        from voc.agent.offline_analyst import answer_offline
        answer, results, events = answer_offline(question, filters, ctx.con, as_of_week=ctx.as_of_week, results=results)
        answer.caveats = list(answer.caveats) + [f"Templated answer (no model): {reason}."]
        return answer, results, events
    except ImportError:
        pass
    text = run.final_text if run and run.final_text else f"No answer could be produced ({reason})."
    return text_only_answer(text), results, events


def _finish(question: str, filters: Filters, ctx: AskContext, answer: Answer, results: dict[str, dict[str, Any]],
            trace: list[dict[str, Any]], *, mode: str, model: str, effort: str, usage: dict[str, Any] | None,
            persist: bool) -> VerifiedAnswer:
    note, _ = scope_note(ctx.con, filters)
    verified = verify_answer(answer, results, ctx.con, as_of_week=ctx.as_of_week, data_version=ctx.data_version,
                             mode=mode, model=model, footnote=ctx.footnote, scope_note=note)
    if persist:
        stored = cache_mod.StoredAnswer(
            qhash=cache_mod.qhash(question, filters, ctx.as_of_week, ctx.data_version), question=question,
            filters=filters.canonical(), as_of_week=ctx.as_of_week, data_version=ctx.data_version,
            prompt_version=ASK_PROMPT_VERSION, mode=mode, model=model, effort=effort,
            answer=verified.model_dump(), trace=trace, validation=verified.validation, usage=usage or {})
        cache_mod.save_answer(ctx.con, stored)
    return verified


async def _replay(stored: cache_mod.StoredAnswer, note: str | None = None) -> AsyncIterator[bytes]:
    if note:
        yield encode_event("status", {"text": note})
    for delay_ms, name, payload in cache_mod.replay_schedule(stored.trace):
        if name in ("answer", "done", "error"):
            continue
        if delay_ms:
            await asyncio.sleep(delay_ms / 1000)
        yield encode_event(name, payload)
    answer = dict(stored.answer)
    answer["mode"] = "recorded" if stored.mode in ("live", "recorded") else stored.mode
    answer["recorded_question"] = stored.question
    answer["recorded_at"] = stored.created_at
    yield encode_event("answer", {"answer": answer})
    yield encode_event("done", {})


async def _live(question: str, filters: Filters, ctx: AskContext, qh: str, n_in_scope: int,
                turn: Callable[..., Any] | None = None, persist: bool = True) -> AsyncIterator[bytes]:
    settings = get_settings()
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[AgentEvent | None] = asyncio.Queue()

    def on_event(ev: AgentEvent) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, ev)

    def work() -> AgentRun:
        try:
            return run_agent(question, filters, ctx.con, as_of_week=ctx.as_of_week, data_version=ctx.data_version,
                             caveats=ctx.caveats, n_in_scope=n_in_scope, qhash=qh, on_event=on_event, turn=turn)
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    task = loop.run_in_executor(None, work)
    while True:
        ev = await queue.get()
        if ev is None:
            break
        if ev.name in ("answer", "done"):
            continue
        yield encode_event(ev.name, ev.payload)
    run = await task
    trace = [_to_dict(e) for e in run.events]
    if run.outcome == "submitted" and run.answer is not None:
        verified = _finish(question, filters, ctx, run.answer, run.results, trace, mode="live", model=run.model,
                           effort=run.effort, usage=run.usage, persist=persist)
        yield encode_event("answer", {"answer": verified.model_dump()})
    else:
        reason = {"text_only": "the agent answered in prose without submitting a structured answer",
                  "timeout": "the agent ran out of time", "refusal": "the model declined",
                  "error": run.error or "the agent failed"}.get(run.outcome, run.error or run.outcome)
        yield encode_event("status", {"text": f"falling back to a templated answer: {reason}"})
        answer, results, events = _templated(question, filters, ctx, run, reason)
        trace += events
        verified = _finish(question, filters, ctx, answer, results, trace, mode="templated", model="none",
                           effort="", usage=run.usage, persist=False)
        yield encode_event("answer", {"answer": verified.model_dump()})
    yield encode_event("done", {})


async def stream_answer(question: str, filters: Filters | dict[str, Any] | None, con: sqlite3.Connection,
                        *, as_of: str | None = None, fresh: bool = False,
                        turn: Callable[..., Any] | None = None, persist: bool = True) -> AsyncIterator[bytes]:
    """Event stream for one question: recorded replay, live agent, or templated fallback."""
    filters = Filters.from_any(filters)
    ctx = build_context(con, as_of)
    settings = get_settings()
    qh = cache_mod.qhash(question, filters, ctx.as_of_week, ctx.data_version)
    yield encode_event("status", {"text": "received", "qhash": qh, "as_of_week": ctx.as_of_week,
                                  "data_version": ctx.data_version})

    if not fresh:
        stored = cache_mod.find_exact(ctx.con, question, filters, ctx.as_of_week, ctx.data_version)
        if stored is not None:
            async for chunk in _replay(stored):
                yield chunk
            return

    can_live = settings.can_call_api and ctx.llm_mode != "fake" and turn is None
    if can_live or turn is not None:
        note, n_in_scope = scope_note(ctx.con, filters)
        async for chunk in _live(question, filters, ctx, qh, n_in_scope, turn=turn, persist=persist):
            yield chunk
        return

    near = cache_mod.find_near(question, filters, ctx.data_version)
    if near is not None:
        stored, score = near
        async for chunk in _replay(stored, note=f"matched to recorded question: {stored.question} (similarity {score:.2f})"):
            yield chunk
        return

    for s in cache_mod.load_files():
        if cache_mod.normalise_question(s.question) == cache_mod.normalise_question(question) and s.data_version != ctx.data_version:
            yield encode_event("status", {"text": "a recorded answer exists for an older data version; re-record it with voc warm-answers"})
            break

    yield encode_event("status", {"text": "no model available; producing a templated answer from the tools"})
    answer, results, events = _templated(question, filters, ctx, None, "no API key on this machine")
    for ev in events:                      # show the same trace a live run would show
        name = str(ev.get("name", "status"))
        if name not in ("answer", "done", "error"):
            yield encode_event(name, dict(ev.get("payload") or {}))
    verified = _finish(question, filters, ctx, answer, results, events, mode="templated", model="none", effort="",
                       usage=None, persist=False)
    yield encode_event("answer", {"answer": verified.model_dump()})
    yield encode_event("done", {})


async def collect(stream: AsyncIterator[bytes]) -> list[tuple[str, dict[str, Any]]]:
    """Decode an event stream into (name, payload) pairs (tests and the CLI)."""
    out: list[tuple[str, dict[str, Any]]] = []
    async for chunk in stream:
        text = chunk.decode("utf-8")
        name, data = "", "{}"
        for line in text.splitlines():
            if line.startswith("event: "):
                name = line[7:].strip()
            elif line.startswith("data: "):
                data = line[6:]
        out.append((name, json.loads(data) if data else {}))
    return out
