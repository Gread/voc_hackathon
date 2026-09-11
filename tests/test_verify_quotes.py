"""Quote verification: exact, normalised (curly quotes, whitespace), transcript speakers, unverifiable."""
from __future__ import annotations

from voc.extract.verify_quotes import find_quote, normalize, speaker_for_span
from voc.schemas.call import CallRecord

TEXT = "I was told the fee would be waived.\nInstead I was charged  $95.00 — twice.\nThe agent said “that's policy” and hung up."


def test_exact_match_has_offsets():
    m = find_quote(TEXT, "the fee would be waived")
    assert m is not None and m.match_kind == "exact"
    assert TEXT[m.char_start:m.char_end] == "the fee would be waived"


def test_curly_quotes_and_dash_normalise_to_ascii():
    m = find_quote(TEXT, 'The agent said "that\'s policy" and hung up.')
    assert m is not None and m.match_kind == "normalized"
    assert TEXT[m.char_start:m.char_end] == "The agent said “that's policy” and hung up."
    m2 = find_quote(TEXT, "charged $95.00 - twice")
    assert m2 is not None and TEXT[m2.char_start:m2.char_end] == "charged  $95.00 — twice"


def test_whitespace_runs_and_newlines_collapse():
    m = find_quote(TEXT, "waived. Instead I was charged $95.00")
    assert m is not None and m.match_kind == "normalized"
    assert TEXT[m.char_start:m.char_end] == "waived.\nInstead I was charged  $95.00"


def test_case_sensitive_and_no_fuzzy():
    assert find_quote(TEXT, "the Fee would be waived") is None
    assert find_quote(TEXT, "the fee will be waived") is None
    assert find_quote(TEXT, "") is None
    assert find_quote(TEXT, "   ") is None


def test_normalize_is_idempotent():
    assert normalize(normalize(TEXT)) == normalize(TEXT)


def _transcript() -> CallRecord:
    lines = ["CUSTOMER: My card was declined at the store.", "AGENT: I can see a fraud hold on the card.",
             "CUSTOMER: Nobody told me anything, this is ridiculous."]
    text = "\n".join(lines)
    starts = [0, len(lines[0]) + 1, len(lines[0]) + len(lines[1]) + 2]
    ranges = [[starts[0], starts[0] + len(lines[0])], [starts[2], starts[2] + len(lines[2])]]
    return CallRecord.build(call_id="conv_1", shape="transcript", date="2025-01-01", text=text,
                            product="checking_or_savings", n_turns=3, customer_char_ranges=ranges)


def test_speaker_for_span_transcript():
    call = _transcript()
    m = find_quote(call.text, "this is ridiculous")
    assert speaker_for_span(call, m.char_start, m.char_end) == "customer"
    m = find_quote(call.text, "fraud hold on the card")
    assert speaker_for_span(call, m.char_start, m.char_end) == "agent"
    # a span crossing turns is not a customer quote
    m = find_quote(call.text, "the store.\nAGENT: I can see")
    assert speaker_for_span(call, m.char_start, m.char_end) == "agent"


def test_speaker_for_span_narrative():
    call = CallRecord.build(call_id="cfpb_1", date="2025-01-01", text="A plain complaint.", product="credit_card")
    assert speaker_for_span(call, 0, 5) == "narrative"
