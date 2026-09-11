"""Live Claude client for JSON-producing calls: structured outputs, cached system prompt, retries."""
from __future__ import annotations

import asyncio
import json
import random
import time
from typing import Any

import anthropic

from voc.llm.client import LLMError, LLMRefusal, LLMRequest, LLMResult, Usage

MAX_ATTEMPTS = 5
BACKOFF_CAP_S = 60.0


def _supports_thinking(model: str) -> bool:
    return not model.startswith("claude-haiku")


def build_kwargs(req: LLMRequest) -> dict[str, Any]:
    """Request body shared by sync/async paths; byte-stable system prompt carries the cache breakpoint."""
    output_config: dict[str, Any] = {"format": {"type": "json_schema", "schema": req.schema}}
    kwargs: dict[str, Any] = {
        "model": req.model,
        "max_tokens": req.max_tokens,
        "system": [{"type": "text", "text": req.system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": req.user}],
        "output_config": output_config,
    }
    if _supports_thinking(req.model):
        kwargs["thinking"] = {"type": "adaptive"}
        if req.effort:
            output_config["effort"] = req.effort
    return kwargs


def _usage(resp: Any) -> Usage:
    u = getattr(resp, "usage", None)
    return Usage(
        input_tokens=getattr(u, "input_tokens", 0) or 0,
        output_tokens=getattr(u, "output_tokens", 0) or 0,
        cache_read_input_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
        cache_creation_input_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
    )


def _parse(resp: Any, req: LLMRequest) -> LLMResult:
    if resp.stop_reason == "refusal":
        details = getattr(resp, "stop_details", None)
        raise LLMRefusal(f"refused ({getattr(details, 'category', None)}): {getattr(details, 'explanation', '')}")
    if resp.stop_reason == "max_tokens":
        raise LLMError("response truncated at max_tokens; raise max_tokens or shorten the input")
    text = next((b.text for b in resp.content if b.type == "text"), None)
    if text is None:
        raise LLMError("no text block in response")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError(f"response is not valid JSON: {exc}") from exc
    return LLMResult(data=data, usage=_usage(resp), model=resp.model, produced_by="api")


def _retryable(exc: Exception) -> bool:
    if isinstance(exc, anthropic.RateLimitError | anthropic.APIConnectionError):
        return True
    return isinstance(exc, anthropic.APIStatusError) and exc.status_code >= 500


def _delay(attempt: int) -> float:
    return min(BACKOFF_CAP_S, (2 ** attempt) + random.uniform(0, 1))


class AnthropicClient:
    def __init__(self, client: anthropic.Anthropic | None = None, aclient: anthropic.AsyncAnthropic | None = None):
        self._client = client
        self._aclient = aclient

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            self._client = anthropic.Anthropic(max_retries=4)
        return self._client

    @property
    def aclient(self) -> anthropic.AsyncAnthropic:
        if self._aclient is None:
            self._aclient = anthropic.AsyncAnthropic(max_retries=4)
        return self._aclient

    def complete_json(self, req: LLMRequest) -> LLMResult:
        kwargs = build_kwargs(req)
        for attempt in range(MAX_ATTEMPTS):
            try:
                return _parse(self.client.messages.create(**kwargs), req)
            except Exception as exc:
                if not _retryable(exc) or attempt == MAX_ATTEMPTS - 1:
                    raise
                time.sleep(_delay(attempt))
        raise LLMError("unreachable")

    async def acomplete_json(self, req: LLMRequest) -> LLMResult:
        kwargs = build_kwargs(req)
        for attempt in range(MAX_ATTEMPTS):
            try:
                return _parse(await self.aclient.messages.create(**kwargs), req)
            except Exception as exc:
                if not _retryable(exc) or attempt == MAX_ATTEMPTS - 1:
                    raise
                await asyncio.sleep(_delay(attempt))
        raise LLMError("unreachable")

    def count_tokens(self, req: LLMRequest) -> int:
        kwargs = build_kwargs(req)
        resp = self.client.messages.count_tokens(model=kwargs["model"], system=kwargs["system"],
                                                 messages=kwargs["messages"])
        return int(resp.input_tokens)
