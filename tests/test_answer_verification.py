"""The server must recount every claim, drop unverifiable quotes and flag invented numbers."""
from __future__ import annotations

import json
import sqlite3

import pytest

from voc.agent.answer import compute_confidence, verify_answer
from voc.schemas.answer import Answer
from voc.store.db import connect, create_schema, set_meta


@pytest.fixture
def con() -> sqlite3.Connection:
    c = connect(":memory:")
    create_schema(c)
    set_meta(c, "data_version", "v1")
    set_meta(c, "as_of_week", "2026-W26")
    for i in range(1, 61):
        month = f"2026-{(i % 6) + 1:02d}"
        c.execute("INSERT INTO calls(call_id, source, shape, date, week, month, text, text_sha, product, region, "
                  "region_group, channel, segment, company, sampling_fraction) "
                  "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (f"c{i}", "test", "narrative", f"{month}-05", "2026-W20", month, f"text {i}", f"sha{i}",
                   "credit_card" if i % 2 else "checking_or_savings", "TX" if i % 3 else "CA",
                   "southwest", "web", "none", "BANK", 0.25))
    c.execute("INSERT INTO topics(topic_id, call_id, idx, topic_label, issue_statement, product, sentiment, "
              "driver_category, driver, outcome, evidence_ok) VALUES ('c1:0','c1',0,'fee','a fee appeared',"
              "'credit_card',-2,'unexpected_charge','a fee','unresolved',1)")
    c.execute("INSERT INTO evidence(evidence_id, topic_id, call_id, quote, char_start, char_end, speaker, "
              "verified, match_kind) VALUES ('c1:0:0','c1:0','c1','a fee appeared on my statement',0,29,"
              "'narrative',1,'exact')")
    c.execute("INSERT INTO tool_results(result_id, qhash, tool, args, sql, call_ids, created_at) "
              "VALUES ('r1','q','list_themes','{}','[]',?, '2026-09-11')",
              (json.dumps([f"c{i}" for i in range(1, 61)]),))
    c.commit()
    return c


def _answer(**kw) -> Answer:
    base = {"answer_markdown": "Fees are the top driver [c1].",
            "claims": [{"id": "c1", "statement": "Fees lead", "headline": True, "result_ids": ["r1"],
                        "call_ids": [], "n_calls": 60, "theme_ids": [], "key_numbers": []}],
            "quotes": [], "charts": [], "caveats": [], "followups": []}
    base.update(kw)
    return Answer.model_validate(base)


def verify(con, answer, qhash="q"):
    return verify_answer(answer, {"r1": {"result_id": "r1", "rows": [{"n_calls": 60, "share": 0.5}], "data": {},
                                         "scope": {"n_calls_in_scope": 60}}},
                         con, as_of_week="2026-W26", data_version="v1", mode="live", model="test", qhash=qhash)


def test_claim_is_recounted_from_call_ids(con):
    out = verify(con, _answer())
    assert out.claims[0].verified is True
    assert out.claims[0].verified_n == 60
    assert out.claims[0].confidence.tier == "broad_pattern"


def test_unknown_result_id_makes_the_claim_unverified(con):
    answer = _answer(claims=[{"id": "c1", "statement": "invented", "headline": True, "result_ids": ["r99"],
                              "call_ids": [], "n_calls": 900, "theme_ids": [], "key_numbers": []}])
    out = verify(con, answer)
    assert out.claims[0].verified is False
    assert out.claims[0].confidence.tier == "unverified"
    assert "c1" in out.validation["unverified_claims"]


def test_model_count_is_corrected_not_trusted(con):
    answer = _answer(claims=[{"id": "c1", "statement": "Fees lead", "headline": True, "result_ids": ["r1"],
                              "call_ids": [], "n_calls": 500, "theme_ids": [], "key_numbers": []}])
    out = verify(con, answer)
    assert out.claims[0].verified_n == 60
    assert out.claims[0].model_n == 500
    assert any(c["field"] == "n_calls" for c in out.claims[0].corrections)


def test_number_not_in_the_tool_result_is_flagged(con):
    answer = _answer(claims=[{"id": "c1", "statement": "Fees lead", "headline": True, "result_ids": ["r1"],
                              "call_ids": [], "n_calls": 60, "theme_ids": [],
                              "key_numbers": [{"label": "share", "value": 93.0, "result_id": "r1"}]}])
    out = verify(con, answer)
    assert any(f.startswith("number_not_from_tools") for f in out.claims[0].flags)
    assert out.validation["number_mismatches"]


def test_unverifiable_quote_is_dropped(con):
    answer = _answer(quotes=[{"evidence_id": "x", "call_id": "c1", "quote": "words nobody ever wrote", "why": ""}])
    out = verify(con, answer)
    assert out.quotes == []
    assert out.validation["dropped_quotes"]


def test_real_quote_is_kept_and_reanchored(con):
    answer = _answer(quotes=[{"evidence_id": "wrong", "call_id": "c1",
                              "quote": "a  fee appeared on my statement", "why": ""}])
    out = verify(con, answer)
    assert len(out.quotes) == 1
    assert out.quotes[0].evidence_id == "c1:0:0"


def test_chart_referencing_an_unknown_result_is_dropped(con):
    answer = _answer(charts=[{"kind": "bars", "title": "t", "result_id": "r99", "series_key": ""}])
    out = verify(con, answer)
    assert out.charts == []


def test_confidence_tiers():
    broad = compute_confidence({"n": 312, "months": 11, "products": 4, "states": 27,
                                "recent_share": 0.2, "evidence_share": 0.9})
    assert broad.tier == "broad_pattern" and "312" in broad.badge
    emerging = compute_confidence({"n": 7, "months": 1, "products": 1, "states": 2,
                                   "recent_share": 0.9, "evidence_share": 1.0}, "new")
    assert emerging.tier == "emerging_signal"
    anecdote = compute_confidence({"n": 3, "months": 1, "products": 1, "states": 1,
                                   "recent_share": 0.1, "evidence_share": 1.0})
    assert anecdote.tier == "anecdotal"
    none = compute_confidence({"n": 0, "months": 0, "products": 0, "states": 0,
                               "recent_share": 0.0, "evidence_share": 0.0})
    assert none.tier == "unverified"
    thin = compute_confidence({"n": 60, "months": 4, "products": 3, "states": 9,
                               "recent_share": 0.1, "evidence_share": 0.2})
    assert thin.thin_evidence and "thin evidence" in thin.badge


def test_another_questions_result_ids_never_count_toward_this_claim(con):
    """Result ids restart at r1 for every question. Before this was scoped, a second recording
    overwrote the first's row and claims were recounted against a stranger's calls."""
    con.execute("INSERT INTO tool_results(result_id, qhash, tool, args, sql, call_ids, created_at) "
                "VALUES ('r1','other_question','list_themes','{}','[]',?, '2026-09-11')",
                (json.dumps(["c1", "c2", "c3"]),))
    con.commit()

    assert verify(con, _answer()).claims[0].verified_n == 60, "its own question's 60 calls, not the other's 3"

    # A claim citing a result this question never ran is unsupported, not counted from someone else's row.
    orphan = verify(con, _answer(), qhash="a_question_that_ran_nothing").claims[0]
    assert orphan.verified is False
    assert "not_supported_by_retrieved_data" in orphan.flags
