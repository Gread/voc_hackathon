"""The batch client's schema adaptation. Pure functions: no network, no key."""
from __future__ import annotations

import json

import pytest

from voc.llm.client import LLMError, LLMRefusal, LLMRequest
from voc.llm.openrouter_client import build_body, parse, relax_schema
from voc.schemas.extraction import EXTRACTION_API_SCHEMA


def _req(schema=None) -> LLMRequest:
    return LLMRequest(stage="extract", model="google/gemini-2.5-flash", system="s", user="u",
                      schema=schema or {"type": "object", "properties": {}}, cache_name="c1")


def test_an_integer_enum_is_moved_into_the_description():
    """Gemini's function format allows enum on strings only. An integer enum voids the whole schema
    on the way through and the model answers `{}` with no error, so it must not survive."""
    relaxed = relax_schema({"type": "object", "properties": {
        "sentiment": {"type": "integer", "enum": [-2, -1, 0, 1, 2]},
        "label": {"type": "string", "enum": ["a", "b"]}}})

    sentiment = relaxed["properties"]["sentiment"]
    assert "enum" not in sentiment, "an integer enum must not reach the provider"
    assert sentiment["type"] == "integer", "the type still has to say integer"
    assert "-2, -1, 0, 1, 2" in sentiment["description"], "the model still needs the allowed values"
    assert relaxed["properties"]["label"]["enum"] == ["a", "b"], "string enums are fine and must stay"


def test_the_real_extraction_schema_carries_no_numeric_enum_to_the_provider():
    body = build_body(_req(EXTRACTION_API_SCHEMA), "google/gemini-2.5-flash")
    schema = body["tools"][0]["function"]["parameters"]

    def numeric_enums(node, path=""):
        if isinstance(node, dict):
            if node.get("type") in ("integer", "number") and "enum" in node:
                yield path
            for k, v in node.items():
                yield from numeric_enums(v, f"{path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from numeric_enums(v, f"{path}[{i}]")

    assert not list(numeric_enums(schema))
    assert schema["properties"]["topics"], "relaxing must not drop the rest of the schema"


def test_the_tool_call_is_forced_so_the_model_cannot_answer_in_prose():
    body = build_body(_req(), "m")
    assert body["tool_choice"]["function"]["name"] == body["tools"][0]["function"]["name"]


def test_prose_instead_of_a_tool_call_is_a_refusal_not_a_silent_empty_result():
    payload = {"choices": [{"message": {"content": "I cannot help with that."}}]}
    with pytest.raises(LLMRefusal):
        parse(payload, _req(), "m")


def test_unparseable_arguments_raise_rather_than_yield_an_empty_extraction():
    payload = {"choices": [{"message": {"tool_calls": [{"function": {"arguments": "{not json"}}]}}]}
    with pytest.raises(LLMError):
        parse(payload, _req(), "m")


def test_usage_is_read_back_so_cost_reporting_is_not_zero():
    payload = {"choices": [{"message": {"tool_calls": [{"function": {"arguments": '{"a":1}'}}]}}],
               "usage": {"prompt_tokens": 120, "completion_tokens": 34,
                         "prompt_tokens_details": {"cached_tokens": 20}}}
    out = parse(payload, _req(), "m")
    assert out.data == {"a": 1}
    assert (out.usage.input_tokens, out.usage.output_tokens) == (120, 34)
    assert out.usage.cache_read_input_tokens == 20
    assert out.produced_by == "api"
