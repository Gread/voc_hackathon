"""One interface for every JSON-producing LLM call (extraction, theming); live, cached or fake."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from voc.config import get_settings


class LLMError(RuntimeError):
    pass


class LLMRefusal(LLMError):
    pass


class LLMCacheMiss(LLMError):
    pass


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0

    def add(self, other: "Usage") -> "Usage":
        return Usage(self.input_tokens + other.input_tokens, self.output_tokens + other.output_tokens,
                     self.cache_read_input_tokens + other.cache_read_input_tokens,
                     self.cache_creation_input_tokens + other.cache_creation_input_tokens)

    def to_dict(self) -> dict[str, int]:
        return {"input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "cache_read_input_tokens": self.cache_read_input_tokens,
                "cache_creation_input_tokens": self.cache_creation_input_tokens}


@dataclass
class LLMRequest:
    stage: str                       # extract | theme_seed | theme_consolidate | theme_reassign | theme_rename
    model: str
    system: str
    user: str
    schema: dict[str, Any]
    effort: str | None = "medium"
    max_tokens: int = 4096
    cache_name: str | None = None    # file stem under data/cache/<stage>/
    cache_key: str | None = None     # content key stored in the file; mismatch = stale
    meta: dict[str, Any] = field(default_factory=dict)   # extra fields for the cache file / fake client


@dataclass
class LLMResult:
    data: dict[str, Any]
    usage: Usage
    model: str
    produced_by: str                 # api | claude_agent | fake
    cached: bool = False


class LLMClient(Protocol):
    def complete_json(self, req: LLMRequest) -> LLMResult: ...
    async def acomplete_json(self, req: LLMRequest) -> LLMResult: ...


def get_client(mode: str | None = None, role: str = "build") -> LLMClient:
    """Factory honouring VOC_LLM: fake | live | cached (cache first, live on miss when a key exists).

    `role` picks which provider setting applies — "ask" for live answering, "build" for the
    extraction and theming stages, which are configured separately on purpose."""
    settings = get_settings()
    mode = mode or settings.llm_mode
    if mode == "fake":
        from voc.llm.fake_client import FakeClient
        return FakeClient()
    from voc.llm.cached_client import CachedClient
    inner = None
    asking = role == "ask"
    provider = settings.ask_provider if asking else settings.build_provider
    if settings.ask_key_present if asking else settings.build_key_present:
        if provider == "openrouter":
            from voc.llm.openrouter_client import OpenRouterClient
            inner = OpenRouterClient()
        else:
            from voc.llm.anthropic_client import AnthropicClient
            inner = AnthropicClient()
    if mode == "live":
        if inner is None:
            raise LLMError(f"VOC_LLM=live but the {role} role points at provider {provider!r} with no key. "
                           f"Set VOC_{role.upper()}_PROVIDER and its key, or run this stage with build-time agents.")
        return CachedClient(inner=inner, write_only=True)
    return CachedClient(inner=inner)
