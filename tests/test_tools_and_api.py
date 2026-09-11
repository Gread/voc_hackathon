"""The tool surface and the REST API, against the fixture index."""
from __future__ import annotations

import json
import os
import sqlite3

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.make_fixture import build_fixture
from voc.agent.tools import DISPATCH, READ_TOOLS, TOOL_SPECS, ToolContext, run_tool
from voc.config import reset_settings_cache
from voc.paths import get_paths
from voc.store.build import build
from voc.store.db import connect

ALLOWED_SCHEMA_KEYWORDS = {"type", "enum", "required", "additionalProperties", "items", "properties", "description"}


@pytest.fixture(scope="module")
def fixture_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("tools") / "data"
    build_fixture(d)
    os.environ["VOC_DATA_DIR"] = str(d)
    os.environ["VOC_LLM"] = "fake"
    reset_settings_cache()
    build(get_paths(d), quiet=True)
    yield d
    os.environ.pop("VOC_DATA_DIR", None)
    reset_settings_cache()


@pytest.fixture(scope="module")
def con(fixture_dir) -> sqlite3.Connection:
    c = connect(fixture_dir / "voc.sqlite")
    yield c
    c.close()


def walk_schema(schema, path="root"):
    if not isinstance(schema, dict):
        return
    for key, value in schema.items():
        if key == "properties":
            for name, sub in value.items():
                walk_schema(sub, f"{path}.{name}")
        elif key == "items":
            walk_schema(value, path + "[]")
        elif key not in ALLOWED_SCHEMA_KEYWORDS:
            raise AssertionError(f"{path}: unsupported schema keyword {key}")
    if schema.get("type") == "object":
        assert set(schema.get("properties", {})) == set(schema.get("required", [])), f"{path}: every property must be required"
        assert schema.get("additionalProperties") is False, f"{path}: additionalProperties must be false"


def test_every_tool_spec_is_strict_compatible():
    assert len(TOOL_SPECS) == 13
    for spec in TOOL_SPECS:
        assert spec["strict"] is True
        assert spec["description"].strip()
        walk_schema(spec["input_schema"], spec["name"])


def tool_args(con: sqlite3.Connection) -> dict[str, dict]:
    theme = con.execute("SELECT theme_id FROM themes WHERE status='active' LIMIT 1").fetchone()["theme_id"]
    call = con.execute("SELECT call_id FROM calls LIMIT 1").fetchone()["call_id"]
    return {
        "get_overview": {"filters": {}},
        "contact_reasons": {"filters": {}, "compare_with_previous": True},
        "list_themes": {"filters": {}, "sort_by": "n_calls", "polarity": "any", "driver_category": None, "limit": 5},
        "theme_detail": {"theme_id": theme, "filters": {}, "as_of_week": None},
        "theme_trend": {"entity_ids": [theme], "grain": "month", "filters": {}},
        "emerging_themes": {"as_of_week": None, "min_recent": 5, "only_new": False, "filters": {}, "limit": 5},
        "sentiment_drivers": {"polarity": "negative", "group_by": "theme", "filters": {}, "limit": 5},
        "breakdown": {"entity_type": "all", "entity_id": None, "by": "product", "filters": {}, "min_n": 5},
        "compare": {"filters_a": {}, "filters_b": {"product": ["credit_card"]}, "label_a": "all",
                    "label_b": "cards", "limit": 5},
        "get_quotes": {"entity_type": "theme", "entity_id": theme, "call_ids": None, "filters": {}, "n": 3,
                       "polarity": "any", "diverse": True},
        "search_calls": {"query": "fee", "filters": {}, "limit": 5},
        "get_call": {"call_id": call},
    }


def test_every_read_tool_returns_the_envelope(con):
    ctx = ToolContext(con=con, qhash="test", as_of_week=None)
    args = tool_args(con)
    assert set(args) == set(DISPATCH) == set(READ_TOOLS)
    for name in READ_TOOLS:
        env = run_tool(name, args[name], con, ctx)
        assert env["tool"] == name
        for key in ("result_id", "scope", "summary", "rows", "data", "call_ids", "n_call_ids", "sql", "data_version"):
            assert key in env, f"{name} is missing {key}"
        assert len(env["call_ids"]) <= 50
        assert env["n_call_ids"] >= len(env["call_ids"])
        stored = con.execute("SELECT call_ids FROM tool_results WHERE result_id=?", (env["result_id"],)).fetchone()
        assert stored is not None, f"{name} did not persist its result"
        assert len(json.loads(stored["call_ids"])) == env["n_call_ids"]


def test_tools_respect_filters(con):
    ctx = ToolContext(con=con, qhash="test", as_of_week=None)
    everything = run_tool("get_overview", {"filters": {}}, con, ctx)
    filtered = run_tool("get_overview", {"filters": {"product": ["credit_card"]}}, con, ctx)
    assert filtered["scope"]["n_calls_in_scope"] < everything["scope"]["n_calls_in_scope"]


def test_minimum_support_suppresses_small_segment_cells(con):
    ctx = ToolContext(con=con, qhash="test", as_of_week=None)
    env = run_tool("breakdown", {"entity_type": "all", "entity_id": None, "by": "region",
                                 "filters": {}, "min_n": 5}, con, ctx)
    assert any(r["suppressed"] for r in env["rows"]), "small state cells must be blanked"


def test_unknown_tool_is_rejected(con):
    with pytest.raises(Exception):
        run_tool("no_such_tool", {}, con, ToolContext(con=con))


@pytest.fixture(scope="module")
def client(fixture_dir):
    from voc.api.app import create_app

    return TestClient(create_app(fixture_dir))


def test_meta_endpoint(client):
    payload = client.get("/api/meta").json()
    assert payload["counts"]["n_calls"] > 0
    assert payload["as_of_week"]
    assert len(payload["questions"]) == 8
    assert payload["as_of_weeks"]


@pytest.mark.parametrize("path", [
    "/api/overview", "/api/reasons?compare=1", "/api/themes?limit=5", "/api/emerging",
    "/api/drivers?polarity=negative", "/api/breakdown?by=product", "/api/search?q=fee", "/api/questions",
])
def test_get_endpoints(client, path):
    res = client.get(path)
    assert res.status_code == 200, res.text
    body = res.json()
    assert "data_version" in body


def test_quotes_endpoint(client, con):
    theme = con.execute("SELECT theme_id FROM themes WHERE status='active' LIMIT 1").fetchone()["theme_id"]
    res = client.get(f"/api/quotes?entity_type=theme&entity_id={theme}&n=3")
    assert res.status_code == 200, res.text
    rows = res.json()["rows"]
    assert rows and all(r["quote"] for r in rows)


def test_a_query_without_its_entity_is_a_clear_400(client):
    """A missing theme id must be a stated error, never a 500."""
    res = client.get("/api/quotes?entity_type=theme")
    assert res.status_code == 400
    assert "theme id" in res.json()["detail"]


def test_result_rows_reexecutes_the_stored_query(client):
    payload = client.get("/api/overview").json()
    rows = client.get(f"/api/results/{payload['result_id']}/rows").json()
    assert rows["n_call_ids"] == payload["n_call_ids"]
    assert rows["reran"] is True


def test_ask_streams_and_always_finishes(client):
    with client.stream("POST", "/api/ask", json={"question": "What are customers contacting us about most?",
                                                 "filters": {}}) as res:
        assert res.status_code == 200
        body = "".join(res.iter_text())
    names = [line[7:].strip() for line in body.splitlines() if line.startswith("event: ")]
    assert names[-1] == "done"
    assert "answer" in names


def test_unknown_theme_is_404(client):
    assert client.get("/api/themes/thm_9999").status_code == 404


def test_satisfaction_rests_on_positive_moments_and_can_be_recounted(con):
    """On a complaint corpus positive topics rarely clear minimum support, so the answer has to come
    from positive moments - and their call ids must be in the result or no claim can be verified."""
    ctx = ToolContext(con=con, qhash="test", as_of_week=None)
    env = run_tool("sentiment_drivers", {"polarity": "positive", "group_by": "driver_category",
                                         "filters": {}, "limit": 5}, con, ctx)
    moments = env["data"]["positive_moments_by_category"]
    assert moments, "the fixture must carry positive moments"
    assert env["data"]["corpus_note"]
    assert env["n_call_ids"] > 0, "a satisfaction claim cannot be verified without call ids"
    quoted = [q for m in moments for q in m.get("quotes", [])]
    assert quoted and all(q["quote"] for q in quoted)


def test_get_call_payload_matches_what_the_call_drawer_reads(con):
    """The drawer highlights evidence by offset and contrasts the form's own label, so this shape is
    a contract: metadata nested, topics carrying evidence with offsets, and the raw labels present."""
    ctx = ToolContext(con=con, qhash="test", as_of_week=None)
    call_id = con.execute("SELECT call_id FROM evidence WHERE verified = 1 LIMIT 1").fetchone()["call_id"]
    data = run_tool("get_call", {"call_id": call_id}, con, ctx)["data"]

    assert data["text"]
    meta = data["metadata"]
    for field in ("date", "week", "month", "product", "product_raw", "issue_raw", "region",
                  "region_group", "channel", "segment", "company", "shape"):
        assert field in meta, f"the drawer reads metadata.{field}"

    topics = data["topics"]
    assert topics, "a call with verified evidence must expose its topics"
    spans = [e for t in topics for e in t.get("evidence", [])]
    assert spans, "topics must carry their evidence"
    for e in spans:
        # get_call returns verified evidence only and drops the flag, so there is nothing to skip
        # on here: every span the drawer receives has to highlight correctly.
        assert "verified" not in e, "an unverified quote must never reach the drawer"
        assert data["text"][e["char_start"]:e["char_end"]] == e["quote"], \
            "offsets must point at the quote or the highlight lands on the wrong words"


def test_panels_loading_at_once_do_not_race(client):
    """The dashboard opens several panels at once. One shared SQLite connection across the
    threadpool interleaves cursors, and a COUNT(*) comes back with no rows at all."""
    import concurrent.futures as cf

    paths = ["/api/overview", "/api/drivers?polarity=negative", "/api/drivers?polarity=positive",
             "/api/emerging", "/api/themes?limit=5", "/api/reasons?compare=1"] * 4
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda p: (p, client.get(p)), paths))
    bad = [(p, r.status_code, r.text[:200]) for p, r in results if r.status_code != 200]
    assert not bad, bad


def test_the_emerging_summary_reports_the_recent_window(con):
    """Emerging rows count the recent window, not the whole scope. Summarizing them with n_calls
    printed every flagged theme as "(0)" - the one line the agent reads to decide what to pull."""
    from voc.agent.tools import summarize

    payload = {"rows": [{"name": "Deposit held far longer than promised", "status": "emerging",
                         "n_recent": 6, "expected_recent": 1.87, "z": 3.11, "n_calls": 0}],
               "data": {"as_of_week": "2026-W26", "n_tested": 11}}
    line = summarize("emerging_themes", payload, {"n_calls_in_scope": 4425})
    assert "6 recent" in line and "1.9 expected" in line
    assert "(0)" not in line
