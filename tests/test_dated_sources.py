"""A source only belongs on a week axis if its calls actually spread over weeks.

The transcript corpus is stamped within a single month at source, so putting it on a timeline piled
two thirds of the corpus into the first five frames and left a flat line behind it - an artefact of
stapling two corpora together, not anything a customer did. The rule is measured, not named, so a
corpus added later classifies itself.
"""
from __future__ import annotations

import sqlite3

import pytest

from voc.store.db import connect, create_schema
from voc.store.queries import MIN_TIMELINE_WEEKS, dated_sources


@pytest.fixture
def con() -> sqlite3.Connection:
    c = connect(":memory:")
    create_schema(c)
    def add(call_id, source, week):
        c.execute("INSERT INTO calls(call_id, source, shape, date, week, month, text, text_sha, product, "
                  "region, region_group, channel, segment, company, sampling_fraction) "
                  "VALUES (?,?,'narrative','2026-01-05',?,'2026-01','t',?,'credit_card','TX','southwest',"
                  "'web','none','BANK',1.0)", (call_id, source, week, call_id))
    for i in range(MIN_TIMELINE_WEEKS + 4):           # spread wide enough to qualify
        add(f"spread{i}", "complaints", f"2026-W{i + 1:02d}")
    for i in range(400):                              # many calls, almost no weeks
        add(f"pile{i}", "transcripts", f"2023-W{35 + (i % 5)}")
    c.commit()
    return c


def test_a_source_crammed_into_a_few_weeks_is_not_dated(con):
    assert dated_sources(con) == ["complaints"], "volume must not buy a place on the time axis"


def test_the_rule_is_coverage_not_a_hard_coded_name(con):
    """A new corpus that spreads over time qualifies without anyone editing a list."""
    for i in range(MIN_TIMELINE_WEEKS + 2):
        con.execute("INSERT INTO calls(call_id, source, shape, date, week, month, text, text_sha, product, "
                    "region, region_group, channel, segment, company, sampling_fraction) "
                    "VALUES (?,'chat','narrative','2026-02-05',?,'2026-02','t',?,'credit_card','TX',"
                    "'southwest','web','none','BANK',1.0)", (f"chat{i}", f"2026-W{i + 1:02d}", f"chat{i}"))
    con.commit()

    assert sorted(dated_sources(con)) == ["chat", "complaints"]
