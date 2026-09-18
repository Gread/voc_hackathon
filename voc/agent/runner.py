"""Manual tool loop for the Q&A agent: streaming, event trace, round/time budgets, terminal submit_answer."""
from __future__ import annotations

import json
import re
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from voc.config import get_settings
from voc.schemas.answer import ASK_PROMPT_VERSION, Answer, clip_answer
from voc.schemas.filters import Filters

MAX_ROUNDS = 8
NUDGE_ROUND = 6
SOFT_BUDGET_S = 60.0
HARD_BUDGET_S = 90.0
MAX_PARALLEL_TOOLS = 4
FALLBACK_BETA = "server-side-fallback-2026-07-01"
SYSTEM_PATH = Path(__file__).with_name("system.md")
MODELS_WITH_SYSTEM_TURNS = ("claude-opus-5", "claude-fable", "claude-mythos", "claude-opus-4-8")


@dataclass
class AgentEvent:
    name: str
    payload: dict[str, Any]
    t_ms: int


@dataclass
class AgentRun:
    question: str
    filters: Filters
    as_of_week: str
    data_version: str
    model: str
    effort: str
    events: list[AgentEvent] = field(default_factory=list)
    results: dict[str, dict[str, Any]] = field(default_factory=dict)   # result_id -> envelope
    answer: Answer | None = None
    final_text: str = ""
    outcome: str = "pending"        # submitted | text_only | timeout | refusal | error
    error: str = ""
    rounds: int = 0
    elapsed_s: float = 0.0
    usage: dict[str, int] = field(default_factory=lambda: {"input_tokens": 0, "output_tokens": 0,
                                                            "cache_read_input_tokens": 0,
                                                            "cache_creation_input_tokens": 0})


def render_system_prompt(caveats: str) -> str:
    return SYSTEM_PATH.read_text(encoding="utf-8").replace("{{DATA_CAVEATS}}", caveats.strip())


def first_user_message(question: str, filters: Filters, as_of_week: str, data_version: str, n_in_scope: int | None) -> str:
    scope = filters.describe()
    lines = [
        f"Question: {question}",
        f"Scope filters: {scope}" + (f" ({n_in_scope} calls in scope)" if n_in_scope is not None else ""),
        f"As-of week: {as_of_week}. Data version: {data_version}. Prompt version: {ASK_PROMPT_VERSION}.",
        "Use the tools, then call submit_answer alone in its own turn.",
    ]
    return "\n".join(lines)


class AnswerDeltaTracker:
    """Extracts the growing answer_markdown string from partial submit_answer JSON."""

    _key = re.compile(r'"answer_markdown"\s*:\s*"')
    _escapes = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "/": "/", "\\": "\\", '"': '"'}

    def __init__(self) -> None:
        self.buf = ""
        self.emitted = 0

    def feed(self, partial: str) -> str | None:
        self.buf += partial
        m = self._key.search(self.buf)
        if not m:
            return None
        s = self.buf[m.end():]
        out: list[str] = []
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == "\\":
                if i + 1 >= len(s):
                    break
                nxt = s[i + 1]
                if nxt == "u":
                    if i + 6 > len(s):
                        break
                    try:
                        out.append(chr(int(s[i + 2:i + 6], 16)))
                    except ValueError:
                        out.append("?")
                    i += 6
                    continue
                out.append(self._escapes.get(nxt, nxt))
                i += 2
                continue
            if ch == '"':
                break
            out.append(ch)
            i += 1
        text = "".join(out)
        new = text[self.emitted:]
        self.emitted = len(text)
        return new or None


def _supports_system_turns(model: str) -> bool:
    return model.startswith(MODELS_WITH_SYSTEM_TURNS)


def _nudge(messages: list[dict[str, Any]], model: str, text: str) -> None:
    """Mid-conversation operator instruction; keeps the cached prefix intact on supporting models."""
    if _supports_system_turns(model):
        messages.append({"role": "system", "content": text})
    else:
        last = messages[-1]
        if last["role"] == "user" and isinstance(last["content"], list):
            last["content"].append({"type": "text", "text": f"<system-reminder>{text}</system-reminder>"})
        else:
            messages.append({"role": "user", "content": f"<system-reminder>{text}</system-reminder>"})


def _block_dict(block: Any) -> dict[str, Any]:
    """Serialise a response content block for the next request."""
    if hasattr(block, "model_dump"):
        return block.model_dump(exclude_none=True)
    return dict(block)


class LiveTurn:
    """One streamed request to Claude; emits status/thinking/answer_delta events while streaming."""

    def __init__(self, client: Any, model: str, effort: str, system: str, tools: list[dict[str, Any]],
                 enable_fallbacks: bool):
        self.client = client
        self.model = model
        self.effort = effort
        self.system = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        self.tools = tools
        self.enable_fallbacks = enable_fallbacks

    def _kwargs(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        kw: dict[str, Any] = {
            "model": self.model, "max_tokens": 16000, "system": self.system, "messages": messages,
            "tools": self.tools, "thinking": {"type": "adaptive", "display": "summarized"},
            "output_config": {"effort": self.effort},
        }
        return kw

    def __call__(self, messages: list[dict[str, Any]], emit: Callable[[str, dict[str, Any]], None]) -> Any:
        import anthropic

        kw = self._kwargs(messages)
        use_beta = self.enable_fallbacks and self.model.startswith(("claude-opus-5", "claude-fable"))
        try:
            if use_beta:
                cm = self.client.beta.messages.stream(**kw, betas=[FALLBACK_BETA], fallbacks="default")
            else:
                cm = self.client.messages.stream(**kw)
            return self._consume(cm, emit)
        except (anthropic.BadRequestError, TypeError) as exc:
            if not use_beta:
                raise
            emit("status", {"text": f"fallbacks unavailable ({exc.__class__.__name__}); retrying without"})
            return self._consume(self.client.messages.stream(**kw), emit)

    @staticmethod
    def _consume(cm: Any, emit: Callable[[str, dict[str, Any]], None]) -> Any:
        tracker: AnswerDeltaTracker | None = None
        with cm as stream:
            for event in stream:
                et = event.type
                if et == "content_block_start":
                    block = event.content_block
                    if block.type == "tool_use":
                        tracker = AnswerDeltaTracker() if block.name == "submit_answer" else None
                        emit("status", {"text": f"calling {block.name}"})
                    elif block.type == "thinking":
                        emit("status", {"text": "thinking"})
                elif et == "content_block_delta":
                    d = event.delta
                    if d.type == "thinking_delta" and d.thinking:
                        emit("thinking", {"text": d.thinking})
                    elif d.type == "text_delta" and d.text:
                        emit("status", {"text": d.text})
                    elif d.type == "input_json_delta" and tracker is not None:
                        new = tracker.feed(d.partial_json)
                        if new:
                            emit("answer_delta", {"text": new})
                elif et == "content_block_stop":
                    tracker = None
            return stream.get_final_message()


def run_agent(
    question: str,
    filters: Filters,
    con: sqlite3.Connection,
    *,
    as_of_week: str,
    data_version: str,
    caveats: str,
    n_in_scope: int | None = None,
    qhash: str = "",
    turn: Callable[[list[dict[str, Any]], Callable[[str, dict[str, Any]], None]], Any] | None = None,
    on_event: Callable[[AgentEvent], None] | None = None,
    model: str | None = None,
    effort: str | None = None,
    client: Any | None = None,
) -> AgentRun:
    """Drive the tool loop until submit_answer, a text-only turn, a refusal or the hard time budget."""
    from voc.agent import tools as tools_mod

    settings = get_settings()
    model = model or settings.live_ask_model
    effort = effort or settings.ask_effort
    run = AgentRun(question=question, filters=filters, as_of_week=as_of_week, data_version=data_version,
                   model=model, effort=effort)
    t0 = time.monotonic()

    def emit(name: str, payload: dict[str, Any]) -> None:
        ev = AgentEvent(name, payload, int((time.monotonic() - t0) * 1000))
        run.events.append(ev)
        if on_event:
            on_event(ev)

    if turn is None:
        system = render_system_prompt(caveats)
        if settings.ask_provider == "openrouter":
            from voc.agent.openrouter_turn import OpenRouterTurn
            turn = OpenRouterTurn(model, effort, system, tools_mod.TOOL_SPECS)
        else:
            import anthropic

            client = client or anthropic.Anthropic(max_retries=2)
            turn = LiveTurn(client, model, effort, system, tools_mod.TOOL_SPECS, settings.enable_fallbacks)

    ctx = tools_mod.ToolContext(con=con, qhash=qhash, as_of_week=as_of_week)
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": first_user_message(question, filters, as_of_week, data_version, n_in_scope)}
    ]
    emit("status", {"text": "reading the question"})
    asked_to_submit = False

    try:
        for round_no in range(1, MAX_ROUNDS + 1):
            run.rounds = round_no
            final = turn(messages, emit)
            _accumulate_usage(run, final)
            content = list(final.content)
            messages.append({"role": "assistant", "content": [_block_dict(b) for b in content]})
            stop = getattr(final, "stop_reason", None)
            if stop == "refusal":
                run.outcome = "refusal"
                run.error = "the model declined to answer this question"
                emit("error", {"message": run.error})
                break
            tool_uses = [b for b in content if getattr(b, "type", None) == "tool_use"]
            texts = [b.text for b in content if getattr(b, "type", None) == "text"]
            if not tool_uses:
                run.final_text = "\n".join(texts).strip()
                # Answering in prose is the common near-miss: the work is done, the wrapper is missing.
                # Ask once for the structured call before falling back to a templated answer.
                if not asked_to_submit and round_no < MAX_ROUNDS:
                    asked_to_submit = True
                    _nudge(messages, model, "Do not answer in prose. Call the submit_answer tool now, alone in "
                                            "this turn, with the findings you already have.")
                    emit("status", {"text": "answer came back as prose; asking for the structured call"})
                    continue
                run.outcome = "text_only"
                break
            submits = [b for b in tool_uses if b.name == "submit_answer"]
            if submits and len(tool_uses) == 1:
                try:
                    run.answer = clip_answer(Answer.model_validate(submits[0].input))
                    run.outcome = "submitted"
                except Exception as exc:  # schema violation: ask once more
                    messages.append({"role": "user", "content": [{
                        "type": "tool_result", "tool_use_id": submits[0].id, "is_error": True,
                        "content": f"submit_answer rejected: {exc}. Call submit_answer again with a valid answer."}]})
                    emit("status", {"text": "answer rejected by validator; retrying"})
                    continue
                emit("status", {"text": "answer submitted"})
                break

            results_blocks = _run_tools(tool_uses, ctx, con, run, emit, tools_mod)
            messages.append({"role": "user", "content": results_blocks})

            elapsed = time.monotonic() - t0
            if elapsed > HARD_BUDGET_S:
                run.outcome = "timeout"
                run.error = f"stopped after {elapsed:.0f}s without an answer"
                emit("error", {"message": run.error})
                break
            if elapsed > SOFT_BUDGET_S or round_no >= NUDGE_ROUND:
                _nudge(messages, model, "Budget nearly spent: call submit_answer now with what you have.")
                emit("status", {"text": "budget nearly spent; asking for the answer"})
        else:
            run.outcome = "timeout"
            run.error = f"no answer after {MAX_ROUNDS} rounds"
            emit("error", {"message": run.error})
    except Exception as exc:  # any API/tool failure ends the run; the service decides the fallback
        run.outcome = "error"
        run.error = f"{exc.__class__.__name__}: {exc}"
        emit("error", {"message": run.error})

    run.elapsed_s = time.monotonic() - t0
    return run


def _accumulate_usage(run: AgentRun, final: Any) -> None:
    u = getattr(final, "usage", None)
    if u is None:
        return
    for key in run.usage:
        run.usage[key] += int(getattr(u, key, 0) or 0)


def _run_tools(tool_uses: list[Any], ctx: Any, con: sqlite3.Connection, run: AgentRun,
               emit: Callable[[str, dict[str, Any]], None], tools_mod: Any) -> list[dict[str, Any]]:
    """Execute up to MAX_PARALLEL_TOOLS calls concurrently; return all tool_result blocks in order."""

    def one(block: Any) -> dict[str, Any]:
        args = block.input if isinstance(block.input, dict) else json.loads(block.input or "{}")
        if block.name == "submit_answer":
            return {"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": "submit_answer must be the only tool call in its turn; call it alone after you have the data."}
        emit("tool_call", {"id": block.id, "name": block.name, "args": args})
        try:
            env = tools_mod.run_tool(block.name, args, con, ctx)
        except Exception as exc:
            emit("tool_result", {"id": block.id, "name": block.name, "error": str(exc)})
            return {"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": f"{block.name} failed: {exc}"}
        run.results[env["result_id"]] = env
        rows = env.get("rows") if isinstance(env.get("rows"), list) else None
        emit("tool_result", {"id": block.id, "result_id": env["result_id"], "name": block.name,
                             "summary": env.get("summary", ""), "n_rows": len(rows) if rows is not None else None,
                             "sql": env.get("sql", [])})
        return {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(env, ensure_ascii=False, default=str)}

    # SQLite connections are used from worker threads; check_same_thread is off in voc.store.db.connect
    with ThreadPoolExecutor(max_workers=min(MAX_PARALLEL_TOOLS, len(tool_uses))) as pool:
        return list(pool.map(one, tool_uses))
