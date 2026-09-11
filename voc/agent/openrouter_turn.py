"""OpenRouter turn for the Q&A agent, so the live Ask can run on Gemini (or anything OpenRouter serves).

The agent loop in runner.py is provider-agnostic: it calls `turn(messages, emit)` and reads Anthropic-shaped
content blocks back. This module speaks OpenRouter's OpenAI-compatible API and translates in both directions,
so the loop, the budgets, the tool execution and the server-side verifier are untouched.

Nothing here can affect whether an answer is correct. The server recounts every claim from call ids and
checks every quoted number against the tool result it cites, whichever model proposed them.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable

import httpx

from voc.agent.runner import AnswerDeltaTracker

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT_S = 180.0
# OpenRouter reports reasoning effort as a level, not a token budget.
EFFORT_LEVELS = {"low": "low", "medium": "medium", "high": "high", "max": "high"}


# --- Anthropic-shaped blocks the loop already understands -------------------------------------

@dataclass
class TextBlock:
    text: str
    type: str = "text"

    def model_dump(self, exclude_none: bool = False) -> dict[str, Any]:
        return {"type": "text", "text": self.text}


@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]
    type: str = "tool_use"

    def model_dump(self, exclude_none: bool = False) -> dict[str, Any]:
        return {"type": "tool_use", "id": self.id, "name": self.name, "input": self.input}


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0


@dataclass
class Response:
    content: list[Any] = field(default_factory=list)
    stop_reason: str = "end_turn"
    usage: Usage = field(default_factory=Usage)


# --- translation ------------------------------------------------------------------------------

def to_openai_tools(specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"type": "function", "function": {"name": s["name"], "description": s["description"],
                                              "parameters": s["input_schema"]}} for s in specs]


def _text_of(content: Any) -> str:
    """Flatten an Anthropic content value to plain text."""
    if isinstance(content, str):
        return content
    parts = [b.get("text", "") for b in content or [] if isinstance(b, dict) and b.get("type") == "text"]
    return "\n".join(p for p in parts if p)


def to_openai_messages(messages: list[dict[str, Any]], system: str) -> list[dict[str, Any]]:
    """Anthropic-shaped conversation -> OpenAI chat messages, splitting tool results into tool turns."""
    out: list[dict[str, Any]] = [{"role": "system", "content": system}]
    for msg in messages:
        role, content = msg.get("role"), msg.get("content")
        if role == "system":
            out.append({"role": "system", "content": _text_of(content)})
            continue
        if role == "assistant":
            blocks = content if isinstance(content, list) else []
            calls = [{"id": b["id"], "type": "function",
                      "function": {"name": b["name"], "arguments": json.dumps(b.get("input") or {},
                                                                              ensure_ascii=False)}}
                     for b in blocks if isinstance(b, dict) and b.get("type") == "tool_use"]
            entry: dict[str, Any] = {"role": "assistant", "content": _text_of(content) or None}
            if calls:
                entry["tool_calls"] = calls
            out.append(entry)
            continue
        # user turn: tool results become their own messages, anything else stays as text
        results = [b for b in (content if isinstance(content, list) else [])
                   if isinstance(b, dict) and b.get("type") == "tool_result"]
        for block in results:
            body = block.get("content")
            out.append({"role": "tool", "tool_call_id": block.get("tool_use_id"),
                        "content": body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)})
        text = _text_of(content)
        if text or not results:
            out.append({"role": "user", "content": text})
    return out


def _stop_reason(finish: str | None, has_tools: bool) -> str:
    if has_tools:
        return "tool_use"
    if finish in ("content_filter", "error"):
        return "refusal"
    return "end_turn"


# --- the turn ----------------------------------------------------------------------------------

class OpenRouterTurn:
    """One streamed request to an OpenRouter model, emitting the same events the Anthropic turn emits."""

    def __init__(self, model: str, effort: str, system: str, tool_specs: list[dict[str, Any]],
                 api_key: str | None = None, base_url: str = BASE_URL,
                 client: httpx.Client | None = None) -> None:
        self.model = model
        self.effort = effort
        self.system = system
        self.tools = to_openai_tools(tool_specs)
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.base_url = base_url
        self._client = client

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=TIMEOUT_S)
        return self._client

    def _body(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "model": self.model,
            "max_tokens": 16000,
            "stream": True,
            "messages": to_openai_messages(messages, self.system),
            "tools": self.tools,
            "tool_choice": "auto",
            "reasoning": {"enabled": True, "effort": EFFORT_LEVELS.get(self.effort, "medium")},
            "usage": {"include": True},
        }

    def __call__(self, messages: list[dict[str, Any]], emit: Callable[[str, dict[str, Any]], None]) -> Response:
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "X-Title": "Voice of the Customer Insights"}
        text_parts: list[str] = []
        calls: dict[int, dict[str, str]] = {}          # stream index -> {id, name, arguments}
        deltas: dict[int, AnswerDeltaTracker] = {}     # answer_markdown streamed out of submit_answer
        usage = Usage()
        finish: str | None = None
        thinking_announced = False

        with self.client.stream("POST", self.base_url, headers=headers, json=self._body(messages)) as response:
            if response.status_code != 200:
                response.read()
                raise RuntimeError(f"OpenRouter HTTP {response.status_code}: {response.text[:300]}")
            for line in response.iter_lines():
                if not line.startswith("data: "):
                    continue
                payload = line[6:].strip()
                if payload == "[DONE]":
                    break
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    continue                            # OpenRouter sends keep-alive comments
                if event.get("usage"):
                    u = event["usage"]
                    usage.input_tokens = int(u.get("prompt_tokens") or 0)
                    usage.output_tokens = int(u.get("completion_tokens") or 0)
                    cached = (u.get("prompt_tokens_details") or {}).get("cached_tokens")
                    usage.cache_read_input_tokens = int(cached or 0)
                choice = (event.get("choices") or [{}])[0]
                finish = choice.get("finish_reason") or finish
                delta = choice.get("delta") or {}
                if delta.get("reasoning") and not thinking_announced:
                    emit("status", {"text": "thinking"})
                    thinking_announced = True
                if delta.get("reasoning"):
                    emit("thinking", {"text": delta["reasoning"]})
                if delta.get("content"):
                    text_parts.append(delta["content"])
                for call in delta.get("tool_calls") or []:
                    idx = int(call.get("index") or 0)
                    slot = calls.setdefault(idx, {"id": "", "name": "", "arguments": ""})
                    if call.get("id"):
                        slot["id"] = call["id"]
                    fn = call.get("function") or {}
                    if fn.get("name"):
                        slot["name"] = fn["name"]
                    if fn.get("arguments"):
                        slot["arguments"] += fn["arguments"]
                        if slot["name"] == "submit_answer":
                            chunk = deltas.setdefault(idx, AnswerDeltaTracker()).feed(fn["arguments"])
                            if chunk:
                                emit("answer_delta", {"text": chunk})

        blocks: list[Any] = []
        text = "".join(text_parts).strip()
        if text:
            blocks.append(TextBlock(text=text))
        for idx in sorted(calls):
            slot = calls[idx]
            if not slot["name"]:
                continue
            try:
                args = json.loads(slot["arguments"] or "{}")
            except json.JSONDecodeError:
                args = {"__raw": slot["arguments"]}     # the loop reports this back as a tool error
            blocks.append(ToolUseBlock(id=slot["id"] or f"call_{idx}", name=slot["name"],
                                       input=args if isinstance(args, dict) else {"value": args}))
        has_tools = any(getattr(b, "type", "") == "tool_use" for b in blocks)
        return Response(content=blocks, stop_reason=_stop_reason(finish, has_tools), usage=usage)
