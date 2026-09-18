"""A call that was pulled but never read must stay out of the index.

Growing a corpus in stages leaves calls.jsonl ahead of extractions.jsonl. `scope()` divides by
COUNT(*) over calls, so an unread call in the index silently shrinks every share while the answer
still looks clean. That is the worst failure shape this project has: confidently wrong arithmetic.
"""
from __future__ import annotations

import json
import os

import pytest

from tests.fixtures.make_fixture import build_fixture
from voc.config import reset_settings_cache
from voc.paths import get_paths
from voc.schemas.filters import Filters
from voc.store import queries as Q
from voc.store.build import build, read_calls_only
from voc.store.db import connect


def test_read_calls_only_drops_unread_and_counts_them():
    class Call:
        def __init__(self, call_id):
            self.call_id = call_id

    calls = [Call("a"), Call("b"), Call("c")]
    extractions = [{"call_id": "a", "status": "ok"},
                   {"call_id": "b", "status": "error"}]     # read, but the reading failed
    kept, coverage = read_calls_only(calls, extractions)

    assert [c.call_id for c in kept] == ["a"]
    assert coverage == {"n_pulled": 3, "n_read": 1, "n_pulled_not_read": 2}


@pytest.fixture
def staged_dir(tmp_path):
    d = tmp_path / "data"
    build_fixture(d)
    os.environ["VOC_DATA_DIR"] = str(d)
    os.environ["VOC_LLM"] = "fake"
    reset_settings_cache()
    yield d
    os.environ.pop("VOC_DATA_DIR", None)
    reset_settings_cache()


def test_unread_call_does_not_move_the_denominator(staged_dir):
    paths = get_paths(staged_dir)
    meta = build(paths, quiet=True)
    con = connect(paths.sqlite)          # closed explicitly: `with` on a connection only scopes the transaction
    try:
        before = Q.scope(Q.Q(con), Filters())["n_calls_in_scope"]
    finally:
        con.close()

    # Pull one more call without reading it: the exact shape of a corpus grown in stages.
    rows = [json.loads(line) for line in paths.calls.read_text(encoding="utf-8").splitlines() if line.strip()]
    unread = dict(rows[0])
    unread["call_id"] = "pulled_but_unread_1"
    with paths.calls.open("a", encoding="utf-8") as f:
        f.write(json.dumps(unread, ensure_ascii=False) + "\n")

    meta2 = build(paths, quiet=True)
    con = connect(paths.sqlite)
    try:
        after = Q.scope(Q.Q(con), Filters())["n_calls_in_scope"]
        indexed = {r[0] for r in con.execute("SELECT call_id FROM calls").fetchall()}
    finally:
        con.close()

    assert after == before, "an unread call changed the denominator every share divides by"
    assert "pulled_but_unread_1" not in indexed
    assert meta2["n_pulled"] == meta["n_pulled"] + 1
    assert meta2["n_pulled_not_read"] == 1
