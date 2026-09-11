"""Golden-number tests for the emerging score, against the planted fixture patterns."""
from __future__ import annotations

import sqlite3

import pytest

from tests.fixtures.make_fixture import build_fixture
from voc.store.build import build
from voc.store.db import connect, get_meta
from voc.paths import get_paths


@pytest.fixture(scope="module")
def fixture_db(tmp_path_factory) -> sqlite3.Connection:
    import os

    from voc.config import reset_settings_cache

    d = tmp_path_factory.mktemp("emerging") / "data"
    build_fixture(d)
    os.environ["VOC_DATA_DIR"] = str(d)
    os.environ["VOC_LLM"] = "fake"
    reset_settings_cache()
    build(get_paths(d), quiet=True)
    con = connect(d / "voc.sqlite")
    yield con
    con.close()
    os.environ.pop("VOC_DATA_DIR", None)
    reset_settings_cache()


def theme_id(con: sqlite3.Connection, letter: str) -> str:
    row = con.execute("SELECT theme_id FROM themes WHERE name LIKE ?", (f"Theme {letter}:%",)).fetchone()
    assert row is not None, f"theme {letter} missing"
    return row["theme_id"]


def score(con: sqlite3.Connection, letter: str, as_of: str | None = None) -> sqlite3.Row | None:
    as_of = as_of or get_meta(con, "as_of_week")
    return con.execute(
        "SELECT * FROM emerging_scores WHERE entity_type='theme' AND entity_id=? AND as_of_week=?",
        (theme_id(con, letter), as_of)).fetchone()


def test_ramping_theme_is_flagged(fixture_db):
    row = score(fixture_db, "B")
    assert row["status"] in ("emerging", "growing")
    assert row["n_recent"] > row["expected_recent"] * 2
    assert row["z"] >= 2.5
    assert row["weeks_recent"] >= 2


def test_brand_new_theme_is_new(fixture_db):
    row = score(fixture_db, "C")
    assert row["status"] == "new"
    assert row["n_baseline"] <= 1
    assert row["weeks_recent"] >= 2
    assert row["n_recent"] >= 5


def test_flat_theme_is_not_flagged(fixture_db):
    row = score(fixture_db, "A")
    assert row["status"] not in ("new", "emerging", "growing")


def test_fading_theme_is_fading_or_stable(fixture_db):
    row = score(fixture_db, "E")
    assert row["status"] in ("fading", "stable", "insufficient")
    assert row["n_recent"] <= row["expected_recent"] + 1


def test_false_positive_line_is_reported(fixture_db):
    row = score(fixture_db, "B")
    assert row["n_tested"] >= 1
    assert 0 <= row["expected_false_positives"] < row["n_tested"]


def test_as_of_replay_shows_the_signal_growing(fixture_db):
    """Ten weeks earlier the ramp is not yet a signal and the new theme does not exist at all."""
    weeks = [r["as_of_week"] for r in fixture_db.execute(
        "SELECT DISTINCT as_of_week FROM emerging_scores ORDER BY as_of_week")]
    earlier = weeks[-11]
    b_then, b_now = score(fixture_db, "B", earlier), score(fixture_db, "B")
    assert b_now["n_recent"] > b_then["n_recent"], "the ramp must be larger at the later as-of week"
    assert b_then["status"] not in ("growing",) or b_then["z"] < b_now["z"]
    c_then = score(fixture_db, "C", earlier)
    assert c_then is None or c_then["n_recent"] == 0, "the new theme has no calls ten weeks earlier"


def test_every_as_of_week_is_precomputed(fixture_db):
    weeks = fixture_db.execute("SELECT COUNT(DISTINCT as_of_week) AS n FROM emerging_scores").fetchone()["n"]
    assert weeks >= 20, "the slider needs a score for every as-of week"


def test_as_of_week_is_never_a_partial_trailing_week(fixture_db):
    """A corpus ending mid-week must not use that week: a half-empty week inside the recent
    four-week window would understate every emerging signal."""
    import datetime

    as_of = get_meta(fixture_db, "as_of_week")
    last_date = datetime.date.fromisoformat(
        fixture_db.execute("SELECT MAX(date) AS d FROM calls").fetchone()["d"])
    year, week = as_of.split("-W")
    week_end = datetime.date.fromisocalendar(int(year), int(week), 7)
    assert week_end <= last_date, f"{as_of} ends {week_end}, after the corpus ends {last_date}"
