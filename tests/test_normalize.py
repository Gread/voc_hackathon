"""Text normalisation and raw -> CallRecord mapping."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from voc.ingest.normalize import (
    collapse_blank_lines, company_slug, month_bounds, month_range, normalize_narrative,
    raw_to_call, unwrap_amounts, word_count,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def page() -> dict:
    return json.loads((FIXTURES / "cfpb_page_sample.json").read_text(encoding="utf-8"))


def test_unwrap_amounts_keeps_redactions():
    assert unwrap_amounts("fee of {$300.00} and {$1,200.00} on XX/XX/XXXX") == "fee of $300.00 and $1,200.00 on XX/XX/XXXX"
    assert unwrap_amounts("XXXX {not an amount}") == "XXXX {not an amount}"


def test_collapse_blank_lines_and_crlf():
    text = "a\r\n\r\n\r\n\r\nb\r\n\r\nc"
    assert normalize_narrative(text) == "a\n\nb\n\nc"
    assert collapse_blank_lines("a\n \n\t\n\nb") == "a\n\nb"


def test_normalize_is_idempotent_and_nfc():
    raw = "café {$5.00}\r\n"
    once = normalize_narrative(raw)
    assert once == "café $5.00"
    assert normalize_narrative(once) == once


def test_word_count_and_slug():
    assert word_count("one  two\nthree") == 3
    assert company_slug("JPMORGAN CHASE & CO.") == "jpmorgan_chase_co"


def test_month_helpers():
    assert month_range("2024-11", "2025-02") == ["2024-11", "2024-12", "2025-01", "2025-02"]
    assert month_bounds("2024-12") == ("2024-12-01", "2025-01-01")


def test_raw_to_call_maps_dimensions(page):
    src = page["hits"]["hits"][0]["_source"]
    rec = raw_to_call(src, 0.11, "EXAMPLE BANK, N.A.")
    assert rec.call_id == "cfpb_9000001"
    assert rec.date == "2024-07-15" and rec.month == "2024-07" and rec.week == "2024-W29"
    assert rec.product == "credit_card" and rec.product_raw == "Credit card"
    assert rec.region == "TX" and rec.region_group == "southwest"
    assert rec.channel == "web" and rec.segment == "servicemember"
    assert rec.sampling_fraction == 0.11 and rec.shape == "narrative"
    assert rec.text.startswith("I was charged an annual fee of $95.00 on XX/XX/XXXX")
    assert "\n\n\n" not in rec.text and "\r" not in rec.text
    assert rec.meta == {"complaint_id": 9000001, "company_response": "Closed with explanation",
                        "timely": "Yes", "zip3": "750", "date_sent_to_company": "2024-07-16"}


def test_raw_to_call_handles_missing_metadata(page):
    by_id = {h["_source"]["complaint_id"]: h["_source"] for h in page["hits"]["hits"]}
    lower_state = raw_to_call(by_id["9000002"], 0.5)
    assert lower_state.region == "NY" and lower_state.region_group == "northeast"
    assert lower_state.company == "EXAMPLE BANK, N.A."
    no_state = raw_to_call(by_id["9000006"], 0.5)
    assert no_state.region == "unknown" and no_state.region_group == "other"
    assert no_state.segment == "none"
    store_card = raw_to_call(by_id["9000004"], 0.5)
    assert store_card.product == "credit_card" and store_card.segment == "older_american"
    both = raw_to_call(by_id["9000005"], 0.5)
    assert both.segment == "older_american_servicemember" and both.meta["zip3"] is None
    assert both.product == "money_transfer_or_p2p"
