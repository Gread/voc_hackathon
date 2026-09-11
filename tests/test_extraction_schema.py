"""Extraction contract as used by the extract lane: schema round-trip, prompt stability, validation rows."""
from __future__ import annotations

import json
import re

from voc.extract.prompt import PROMPT_VERSION, build_system_prompt, build_user_message, cache_key
from voc.extract.validate import redaction_share, validate_response
from voc.extract.verify_quotes import find_quote
from voc.schemas.call import CallRecord
from voc.schemas.extraction import EXTRACTION_API_SCHEMA, SCHEMA_VERSION, Extraction, normalize_extraction
from voc.taxonomy import loader as tx


def _examples() -> list[tuple[str, str, dict]]:
    prompt = build_system_prompt()
    records = re.findall(r'<record shape="(\w+)">\n(.*?)\n</record>', prompt, re.S)
    blocks = re.findall(r"```json\n(.*?)\n```", prompt, re.S)
    assert len(records) == 3 and len(blocks) == 3
    return [(shape, text, json.loads(block)) for (shape, text), block in zip(records, blocks)]


def test_api_schema_is_strict_and_lists_enums():
    props = EXTRACTION_API_SCHEMA["properties"]
    assert EXTRACTION_API_SCHEMA["additionalProperties"] is False
    assert set(EXTRACTION_API_SCHEMA["required"]) == set(props)
    assert props["contact_reasons"]["items"]["properties"]["reason"]["enum"] == tx.codes("contact_reasons")
    assert props["topics"]["items"]["properties"]["sentiment"]["enum"] == [-2, -1, 0, 1, 2]


def test_worked_examples_round_trip_and_quotes_verify():
    for shape, text, raw in _examples():
        ext, flags = normalize_extraction(raw)
        assert flags == [], (shape, flags)
        again = Extraction.model_validate(json.loads(ext.model_dump_json()))
        assert again == ext
        assert sum(r.is_primary for r in ext.contact_reasons) == 1
        for topic in ext.topics:
            for ev in topic.evidence:
                assert find_quote(text, ev.quote) is not None, ev.quote
                assert ev.speaker == ("narrative" if shape == "narrative" else "customer")
        for pm in ext.positive_moments:
            assert find_quote(text, pm.quote) is not None


def test_system_prompt_is_stable_long_and_label_free():
    a, b = build_system_prompt(), build_system_prompt()
    assert a == b and "{{" not in a
    assert len(a) // 4 > 2500, "system prompt must stay above ~2.5k tokens to be cacheable"
    for code in tx.codes("contact_reasons") + tx.codes("driver_categories"):
        assert f"`{code}`" in a
    assert PROMPT_VERSION == "ext-1.0"


def test_user_message_is_the_record_only():
    call = CallRecord.build(call_id="cfpb_1", date="2025-02-03", text="Fee charged twice.", product="credit_card",
                            product_raw="Credit card", issue_raw="Fees or interest", sub_issue_raw="Problem with fees")
    msg = build_user_message(call)
    assert msg == '<record shape="narrative">\nFee charged twice.\n</record>'
    for label in ("Credit card", "Fees or interest", "Problem with fees", "credit_card"):
        assert label not in msg


def test_cache_key_depends_on_versions_and_text():
    k = cache_key("abc")
    assert len(k) == 64 and k == cache_key("abc") and k != cache_key("abd")
    assert SCHEMA_VERSION in ("1",) and tx.version() == "1"


def test_validate_response_enriches_evidence_and_flags():
    shape, text, raw = _examples()[0]
    call = CallRecord.build(call_id="cfpb_1", date="2025-02-03", text=text, product="credit_card")
    raw = json.loads(json.dumps(raw))
    raw["topics"][0]["evidence"].append({"quote": "this sentence is not in the text at all", "speaker": "narrative"})
    raw["overall_sentiment"] = 2
    row = validate_response(call, raw, produced_by="claude_agent", model="claude-agent-build", extracted_at="2026-01-01T00:00:00+00:00")
    assert row["status"] == "ok" and row["produced_by"] == "claude_agent"
    assert row["prompt_version"] == PROMPT_VERSION and row["schema_version"] == SCHEMA_VERSION
    ev = row["extraction"]["topics"][0]["evidence"]
    assert ev[0]["verified"] == 1 and ev[0]["match_kind"] == "exact"
    assert text[ev[0]["char_start"]:ev[0]["char_end"]] == ev[0]["quote"]
    assert ev[-1]["verified"] == 0 and ev[-1]["char_start"] is None
    assert row["extraction"]["topics"][0]["evidence_ok"] == 1
    assert 0 < row["quote_verify_rate"] < 1
    assert "sentiment_inconsistent" in row["flags"] and "product_mismatch" in row["flags"]
    assert "no_verified_quotes" not in row["flags"]


def test_validate_response_error_row_on_broken_response():
    call = CallRecord.build(call_id="cfpb_1", date="2025-02-03", text="Some text here.", product="credit_card")
    row = validate_response(call, {"contact_reasons": []}, produced_by="api", model="m", extracted_at=None)
    assert row["status"] == "error" and "no contact_reasons" in row["error"] and row["extraction"] is None
    row = validate_response(call, "not an object", produced_by="api", model="m", extracted_at=None)
    assert row["status"] == "error"


def test_redaction_share():
    assert redaction_share("XXXX XXXX said XX/XX/XXXX.") == 0.75
    assert redaction_share("no redaction at all") == 0.0


def test_near_miss_enum_values_are_aliased_not_discarded():
    """A topic outcome has no "partially resolved", but the customer did say it is not fully fixed:
    keep the meaning rather than dropping to an abstention."""
    from voc.llm.fake_client import fake_extraction
    from voc.schemas.extraction import normalize_extraction

    raw = fake_extraction("Chase charged me a $34.00 overdraft fee and nobody called back.")
    raw["topics"][0]["outcome"] = "partially_resolved"
    ext, flags = normalize_extraction(raw)
    assert ext.topics[0].outcome == "unresolved"
    assert any(f.startswith("aliased_enum:outcome") for f in flags)

    raw["topics"][0]["outcome"] = "nonsense"
    ext, flags = normalize_extraction(raw)
    assert ext.topics[0].outcome == "unknown"
    assert any(f.startswith("invalid_enum:outcome") for f in flags)
