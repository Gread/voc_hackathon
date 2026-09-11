"""Builds the byte-stable extraction system prompt, the user turn and the cache key.
No CFPB product, issue or sub-issue ever enters a prompt (DESIGN decision 6)."""
from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

from voc.config import get_settings
from voc.llm.client import LLMRequest
from voc.schemas.call import CallRecord
from voc.schemas.extraction import EXTRACTION_API_SCHEMA, SCHEMA_VERSION
from voc.taxonomy import loader as tx

PROMPT_VERSION = "ext-1.0"
PROMPT_PATH = Path(__file__).with_name("prompt_system.md")
STAGE = "extract"
MAX_TOKENS = 4096

# placeholder -> taxonomy kind rendered through the shared loader
_SECTIONS = {
    "contact_reasons": "contact_reasons",
    "products": "products",
    "services": "services",
    "driver_categories": "driver_categories",
    "customer_asks": "customer_asks",
    "sentiment": "sentiment",
    "positive_moment_categories": "positive_moment_categories",
}


@lru_cache(maxsize=1)
def build_system_prompt() -> str:
    """Render prompt_system.md with the taxonomy sections. Pure function of the files: byte-stable."""
    text = PROMPT_PATH.read_text(encoding="utf-8")
    for placeholder, kind in _SECTIONS.items():
        text = text.replace("{{" + placeholder + "}}", tx.prompt_section(kind))
    text = (text.replace("{{prompt_version}}", PROMPT_VERSION)
                .replace("{{schema_version}}", SCHEMA_VERSION)
                .replace("{{taxonomy_version}}", tx.version()))
    if "{{" in text:
        raise RuntimeError("unrendered placeholder in prompt_system.md")
    return text


def build_user_message(call: CallRecord) -> str:
    """The record and nothing else."""
    return f'<record shape="{call.shape}">\n{call.text}\n</record>'


def cache_key(text_sha: str) -> str:
    raw = f"{PROMPT_VERSION}|{SCHEMA_VERSION}|{tx.version()}|{text_sha}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_request(call: CallRecord, model: str | None = None, effort: str | None = None) -> LLMRequest:
    settings = get_settings()
    return LLMRequest(
        stage=STAGE,
        model=model or settings.extract_model,
        system=build_system_prompt(),
        user=build_user_message(call),
        schema=EXTRACTION_API_SCHEMA,
        effort=effort or settings.extract_effort,
        max_tokens=MAX_TOKENS,
        cache_name=call.call_id,
        cache_key=cache_key(call.text_sha),
        meta={"call_id": call.call_id, "text_sha": call.text_sha, "prompt_version": PROMPT_VERSION,
              "schema_version": SCHEMA_VERSION, "taxonomy_version": tx.version(), "text": call.text},
    )


def estimate_tokens(text: str) -> int:
    """Offline estimate used when no key exists: 4 characters per token."""
    return max(1, len(text) // 4)
