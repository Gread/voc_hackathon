"""Token usage to USD, using list prices per million tokens (input, output)."""
from __future__ import annotations

from voc.llm.client import Usage

PRICES_PER_M = {
    "claude-opus-5": (5.0, 25.0),
    "claude-sonnet-5": (2.0, 10.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-fable-5-1": (10.0, 50.0),
}
CACHE_READ_MULT = 0.1
CACHE_WRITE_MULT = 1.25


def prices(model: str) -> tuple[float, float]:
    for key, value in PRICES_PER_M.items():
        if model.startswith(key):
            return value
    return (0.0, 0.0)


def estimate_usd(model: str, usage: Usage) -> float:
    inp, out = prices(model)
    return (usage.input_tokens * inp
            + usage.cache_read_input_tokens * inp * CACHE_READ_MULT
            + usage.cache_creation_input_tokens * inp * CACHE_WRITE_MULT
            + usage.output_tokens * out) / 1_000_000
