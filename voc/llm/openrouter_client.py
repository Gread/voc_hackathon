"""OpenRouter client for the batch stages (extraction, theming), so they can run on any model.

Implements the same two-method LLMClient protocol the Anthropic client implements. Structured output
is a forced tool call carrying the stage's JSON schema, which is what OpenRouter normalises across
providers; a model that answers in prose instead is retried once, then reported as a refusal.
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import time
from typing import Any

import httpx

from voc.config import get_settings
from voc.llm.client import LLMError, LLMRefusal, LLMRequest, LLMResult, Usage

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT_S = 180.0
MAX_RETRIES = 5
EMPTY_RETRIES = 3   # an empty turn is usually transient, not a refusal
# When a model keeps returning nothing for a batch, try a stronger one rather than losing the
# batch: one flaky response used to abort a 200-request theming run.
FALLBACK_MODEL = {"google/gemini-2.5-flash": "google/gemini-3.1-pro-preview"}
RETRY_STATUSES = {408, 409, 429, 500, 502, 503, 504}
TOOL_NAME = "emit"
EFFORT_LEVELS = {"low": "low", "medium": "medium", "high": "high", "max": "high"}


def _model_for(req: LLMRequest) -> str:
    """The stage decides the model; VOC_OR_* settings name it for OpenRouter."""
    s = get_settings()
    if req.stage == "extract":
        return s.or_extract_model
    if req.stage.startswith("theme"):
        return s.or_theme_model
    return s.or_ask_model


def relax_schema(node: Any) -> Any:
    """Rewrite constructs that Gemini's function-declaration format cannot express.

    An `enum` on a non-string type voids the WHOLE schema on the way through, and the failure is
    silent: the model still calls the tool, with `{}` as its arguments. The allowed values move into
    the description so the model still knows them, and the value comes back correctly typed.
    """
    if isinstance(node, dict):
        out = {k: relax_schema(v) for k, v in node.items()}
        if out.get("type") in ("integer", "number") and isinstance(out.get("enum"), list):
            allowed = ", ".join(str(v) for v in out.pop("enum"))
            out["description"] = f"{out.get('description', '')} Must be one of: {allowed}.".strip()
        return out
    if isinstance(node, list):
        return [relax_schema(v) for v in node]
    return node


def build_body(req: LLMRequest, model: str) -> dict[str, Any]:
    return {
        "model": model,
        "max_tokens": req.max_tokens,
        "messages": [{"role": "system", "content": req.system},
                     {"role": "user", "content": req.user}],
        "tools": [{"type": "function", "function": {
            "name": TOOL_NAME,
            "description": "Return the result for this record, matching the schema exactly.",
            "parameters": relax_schema(req.schema)}}],
        "tool_choice": {"type": "function", "function": {"name": TOOL_NAME}},
        "reasoning": {"enabled": True, "effort": EFFORT_LEVELS.get(req.effort or "medium", "medium")},
        "usage": {"include": True},
    }


def parse(payload: dict[str, Any], req: LLMRequest, model: str) -> LLMResult:
    choice = (payload.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    calls = message.get("tool_calls") or []
    if not calls:
        text = (message.get("content") or "").strip()
        raise LLMRefusal(f"{model} returned no structured output for {req.cache_name}: {text[:200]}")
    raw = (calls[0].get("function") or {}).get("arguments") or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LLMError(f"{model} returned invalid JSON for {req.cache_name}: {exc}") from exc
    if not isinstance(data, dict):
        raise LLMError(f"{model} returned {type(data).__name__}, not an object, for {req.cache_name}")
    u = payload.get("usage") or {}
    cached = (u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
    usage = Usage(input_tokens=int(u.get("prompt_tokens") or 0),
                  output_tokens=int(u.get("completion_tokens") or 0),
                  cache_read_input_tokens=int(cached))
    return LLMResult(data=data, usage=usage, model=model, produced_by="api")


def _delay(attempt: int) -> float:
    return min(60.0, 2.0 ** attempt + random.random())


class OpenRouterClient:
    """Blocking and async JSON completion over OpenRouter's OpenAI-compatible endpoint."""

    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL,
                 client: httpx.Client | None = None, aclient: httpx.AsyncClient | None = None) -> None:
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.base_url = base_url
        self._client = client
        self._aclient = aclient
        self._aloop: Any = None

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}",
                "X-Title": "Voice of the Customer Insights"}

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=TIMEOUT_S)
        return self._client

    @property
    def aclient(self) -> httpx.AsyncClient:
        """One client per event loop.

        The theming passes call `asyncio.run` once per batch group, so each group gets a fresh loop
        and closes it afterwards. A client cached across that boundary is bound to a loop that no
        longer exists, and the next group dies with "Event loop is closed".
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if self._aclient is None or self._aloop is not loop:
            self._aclient = httpx.AsyncClient(timeout=TIMEOUT_S,
                                              limits=httpx.Limits(max_connections=32))
            self._aloop = loop
        return self._aclient

    def complete_json(self, req: LLMRequest) -> LLMResult:
        model = req.model if "/" in req.model else _model_for(req)
        body = build_body(req, model)
        last: LLMRefusal | None = None
        for attempt in range(MAX_RETRIES + 1):
            response = self.client.post(self.base_url, headers=self.headers, json=body)
            if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES:
                time.sleep(_delay(attempt))
                continue
            if response.status_code != 200:
                raise LLMError(f"OpenRouter HTTP {response.status_code}: {response.text[:300]}")
            try:
                return parse(response.json(), req, model)
            except LLMRefusal as exc:
                # An empty turn is usually transient rather than a real refusal; give it another go.
                last = exc
                if attempt >= EMPTY_RETRIES:
                    break
                time.sleep(_delay(attempt))
        stronger = FALLBACK_MODEL.get(model)
        if stronger:
            response = self.client.post(self.base_url, headers=self.headers,
                                        json=build_body(req, stronger))
            if response.status_code == 200:
                return parse(response.json(), req, stronger)
        raise last or LLMError("unreachable")

    async def acomplete_json(self, req: LLMRequest) -> LLMResult:
        model = req.model if "/" in req.model else _model_for(req)
        body = build_body(req, model)
        last: LLMRefusal | None = None
        for attempt in range(MAX_RETRIES + 1):
            response = await self.aclient.post(self.base_url, headers=self.headers, json=body)
            if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES:
                await asyncio.sleep(_delay(attempt))
                continue
            if response.status_code != 200:
                raise LLMError(f"OpenRouter HTTP {response.status_code}: {response.text[:300]}")
            try:
                return parse(response.json(), req, model)
            except LLMRefusal as exc:
                last = exc
                if attempt >= EMPTY_RETRIES:
                    break
                await asyncio.sleep(_delay(attempt))
        stronger = FALLBACK_MODEL.get(model)
        if stronger:
            response = await self.aclient.post(self.base_url, headers=self.headers,
                                               json=build_body(req, stronger))
            if response.status_code == 200:
                return parse(response.json(), req, stronger)
        raise last or LLMError("unreachable")
