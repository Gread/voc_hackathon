"""Transcript rendering, customer offsets and merge into calls.jsonl."""
from __future__ import annotations

from pathlib import Path

from voc.ingest.normalize import read_jsonl
from voc.ingest.transcripts import ingest_transcripts, merge_into_calls, render_transcript, transcript_to_call
from voc.paths import get_paths
from voc.schemas.call import CallRecord

FIXTURE = Path(__file__).parent / "fixtures" / "transcripts_sample.jsonl"


def test_render_transcript_offsets_point_at_customer_text():
    turns = [{"speaker": "agent", "text": "Hi"}, {"speaker": "customer", "text": "Fee\nagain"},
             {"speaker": "customer", "text": " thanks "}]
    text, n_turns, ranges = render_transcript(turns)
    assert text == "AGENT: Hi\nCUSTOMER: Fee again\nCUSTOMER: thanks"
    assert n_turns == 3
    assert [text[a:b] for a, b in ranges] == ["Fee again", "thanks"]


def test_transcript_to_call_contract():
    recs = list(read_jsonl(FIXTURE))
    call = transcript_to_call(recs[0], source="conv", company="EXAMPLE BANK, N.A.")
    assert call.call_id == "conv_t001" and call.shape == "transcript" and call.channel == "phone"
    assert call.n_turns == 4 and call.product == "credit_card" and call.product_raw == "Credit card"
    assert call.region == "WA" and call.region_group == "west" and call.segment == "servicemember"
    assert call.week == "2025-W10" and call.month == "2025-03" and call.sampling_fraction == 1.0
    lines = call.text.split("\n")
    assert lines[0].startswith("AGENT: ") and lines[1].startswith("CUSTOMER: ")
    assert [call.text[a:b] for a, b in call.customer_char_ranges] == [
        "I was charged a late fee of $39 even though my autopay is on. It has happened twice now.",
        "I just want the fee reversed and autopay fixed.",
    ]
    second = transcript_to_call(recs[1])
    assert second.call_id == "conv_t002"  # prefix not doubled
    assert second.product == "checking_or_savings" and second.region == "unknown" and second.company == "unknown"
    assert second.text.split("\n")[0] == "CUSTOMER: My debit card was declined at the grocery store and the app shows an error."


def test_ingest_merges_and_dedupes(data_dir: Path):
    paths = get_paths().ensure()
    existing = CallRecord.build(call_id="cfpb_1", date="2025-01-02", text="x" * 40, product="credit_card")
    merge_into_calls(paths, [existing])
    assert ingest_transcripts(paths, FIXTURE, source="conv") == 2
    rows = list(read_jsonl(paths.calls))
    assert [r["call_id"] for r in rows] == ["cfpb_1", "conv_t001", "conv_t002"]
    # re-ingesting (from a directory this time) replaces rather than duplicates
    corpus_dir = data_dir / "corpus"
    corpus_dir.mkdir()
    (corpus_dir / "part1.jsonl").write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    ingest_transcripts(paths, corpus_dir, source="conv")
    rows = list(read_jsonl(paths.calls))
    assert len(rows) == 3 and all(CallRecord(**r) for r in rows)
    assert rows[1]["customer_char_ranges"] and rows[1]["n_turns"] == 4
