"""The OpenRouter adapter translates between the OpenAI wire format and the Anthropic-shaped blocks
the agent loop reads. These are pure functions: no network, no key."""
from __future__ import annotations

import json

from voc.agent.openrouter_turn import (TextBlock, ToolUseBlock, _stop_reason, to_openai_messages,
                                       to_openai_tools)


def test_tool_specs_become_openai_functions():
    specs = [{"name": "list_themes", "description": "Themes ranked by calls.",
              "input_schema": {"type": "object", "properties": {"limit": {"type": "integer"}},
                               "required": ["limit"], "additionalProperties": False}}]
    out = to_openai_tools(specs)
    assert out[0]["type"] == "function"
    assert out[0]["function"]["name"] == "list_themes"
    assert out[0]["function"]["parameters"] == specs[0]["input_schema"], "the schema must survive verbatim"


def test_a_tool_round_trip_keeps_the_ids_that_pair_calls_with_results():
    """A tool result must come back attached to the call it answers, or the model loses the thread."""
    messages = [
        {"role": "user", "content": "Which themes are biggest?"},
        {"role": "assistant", "content": [TextBlock(text="Let me look.").model_dump(),
                                          ToolUseBlock(id="call_7", name="list_themes",
                                                       input={"limit": 5}).model_dump()]},
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "call_7",
                                      "content": '{"rows": []}'}]},
    ]
    out = to_openai_messages(messages, system="You are an analyst.")

    assert out[0] == {"role": "system", "content": "You are an analyst."}
    assistant = next(m for m in out if m["role"] == "assistant")
    assert assistant["content"] == "Let me look."
    call = assistant["tool_calls"][0]
    assert call["id"] == "call_7" and call["function"]["name"] == "list_themes"
    assert json.loads(call["function"]["arguments"]) == {"limit": 5}

    tool_msg = next(m for m in out if m["role"] == "tool")
    assert tool_msg["tool_call_id"] == "call_7", "the result must name the call it answers"
    assert tool_msg["content"] == '{"rows": []}'


def test_a_mid_conversation_nudge_survives_translation():
    """The loop nudges the model toward submit_answer. Dropping that turn would strand the run."""
    out = to_openai_messages([{"role": "system", "content": "Call submit_answer now."}], system="base")
    assert [m["content"] for m in out if m["role"] == "system"] == ["base", "Call submit_answer now."]


def test_a_tool_result_turn_does_not_also_emit_an_empty_user_message():
    out = to_openai_messages([{"role": "user", "content": [{"type": "tool_result", "tool_use_id": "a",
                                                            "content": "{}"}]}], system="s")
    assert [m["role"] for m in out] == ["system", "tool"], "an empty user turn confuses some models"


def test_stop_reason_maps_to_what_the_loop_checks():
    assert _stop_reason("tool_calls", has_tools=True) == "tool_use"
    assert _stop_reason("stop", has_tools=False) == "end_turn"
    assert _stop_reason("content_filter", has_tools=False) == "refusal", "a refusal must end the run"
    # A model can emit tool calls while reporting length; the calls are what matter.
    assert _stop_reason("length", has_tools=True) == "tool_use"
