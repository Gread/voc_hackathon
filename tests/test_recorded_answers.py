"""The offline demo's backbone: drive the tools, record an answer, verify it, replay it.

This runs without an API key, which is the point - it is how the demo answers are produced and shown.
"""
from __future__ import annotations

import argparse
import asyncio
import gc
import json
import os
from pathlib import Path

import pytest

from tests.fixtures.make_fixture import build_fixture
from voc.agent import cache as cache_mod
from voc.agent import record
from voc.agent.service import collect, stream_answer
from voc.agent.tool_cli import run as tool_run
from voc.config import reset_settings_cache
from voc.paths import get_paths
from voc.store.build import build
from voc.store.db import connect

QUESTION = "Which issues are growing fastest, and are any of them new?"


@pytest.fixture
def demo_dir(tmp_path, monkeypatch):
    d = tmp_path / "data"
    build_fixture(d)
    monkeypatch.setenv("VOC_DATA_DIR", str(d))
    monkeypatch.setenv("VOC_LLM", "fake")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    reset_settings_cache()
    build(get_paths(d), quiet=True)
    yield d
    reset_settings_cache()


def call_tool(name: str, args: dict, session: Path, capsys) -> dict:
    tool_run(argparse.Namespace(name=name, args=json.dumps(args), as_of=None,
                                session=str(session), compact=True))
    return json.loads(capsys.readouterr().out.strip().splitlines()[-1])


def test_record_verify_and_replay_a_demo_answer(demo_dir, capsys):
    started = json.loads(_capture(capsys, lambda: record.start(argparse.Namespace(
        question=QUESTION, filters="{}", as_of=None, session_id=None))))
    session = Path(started["tools_file"])

    emerging = call_tool("emerging_themes", {"as_of_week": None, "min_recent": 5, "only_new": False,
                                             "filters": {}, "limit": 5}, session, capsys)
    assert emerging["rows"], "the fixture must have an emerging theme to record an answer about"
    top = emerging["rows"][0]
    detail = call_tool("theme_detail", {"theme_id": top["theme_id"], "filters": {}, "as_of_week": None},
                       session, capsys)
    quotes = call_tool("get_quotes", {"entity_type": "theme", "entity_id": top["theme_id"], "call_ids": None,
                                      "filters": {}, "n": 2, "polarity": "any", "diverse": True}, session, capsys)

    Path(started["answer_file"]).write_text(json.dumps({
        "answer_markdown": f"**{top['name']}** is growing [c1].",
        "claims": [{"id": "c1", "statement": f"{top['name']} is growing", "headline": True,
                    "result_ids": [detail["result_id"]], "call_ids": [],
                    "n_calls": detail["data"]["n_calls"], "theme_ids": [top["theme_id"]],
                    "key_numbers": [{"label": "recent calls", "value": float(top["n_recent"]),
                                     "result_id": emerging["result_id"]}]}],
        "quotes": [{"evidence_id": r["evidence_id"], "call_id": r["call_id"], "quote": r["quote"], "why": ""}
                   for r in quotes["rows"][:2]],
        "charts": [], "caveats": [], "followups": [],
    }, ensure_ascii=False), encoding="utf-8")

    code = record.finalize(argparse.Namespace(session_id=started["session_id"], model="claude-agent-build",
                                              allow_unverified_headline=False))
    assert code == 0, "a well-cited answer must finalize"

    stored = cache_mod.load_answer(None, started["qhash"])
    assert stored is not None and stored.mode == "recorded"
    claim = stored.answer["claims"][0]
    assert claim["verified"] and claim["verified_n"] > 0
    assert stored.answer["quotes"], "verified quotes must survive"

    con = connect(demo_dir / "voc.sqlite")
    events = asyncio.run(collect(stream_answer(QUESTION, {}, con)))
    names = [n for n, _ in events]
    assert names[-1] == "done" and "answer" in names
    assert "tool_call" in names, "the replay must show the agent working, not just the answer"
    replayed = next(p["answer"] for n, p in events if n == "answer")
    assert replayed["mode"] == "recorded"
    assert replayed["claims"][0]["verified_n"] == claim["verified_n"]


def test_a_differently_worded_question_finds_the_recording(demo_dir, capsys):
    test_record_verify_and_replay_a_demo_answer(demo_dir, capsys)
    con = connect(demo_dir / "voc.sqlite")
    events = asyncio.run(collect(stream_answer("what is growing fastest and is anything new?", {}, con)))
    answer = next(p["answer"] for n, p in events if n == "answer")
    assert answer["mode"] == "recorded"
    assert answer["recorded_question"] == QUESTION


def test_an_answer_citing_nothing_is_refused(demo_dir, capsys):
    started = json.loads(_capture(capsys, lambda: record.start(argparse.Namespace(
        question="What are the main causes of negative sentiment?", filters="{}", as_of=None, session_id=None))))
    Path(started["answer_file"]).write_text(json.dumps({
        "answer_markdown": "Fees are the biggest problem [c1].",
        "claims": [{"id": "c1", "statement": "fees dominate", "headline": True, "result_ids": ["r99"],
                    "call_ids": [], "n_calls": 900, "theme_ids": [], "key_numbers": []}],
        "quotes": [], "charts": [], "caveats": [], "followups": [],
    }), encoding="utf-8")
    code = record.finalize(argparse.Namespace(session_id=started["session_id"], model="claude-agent-build",
                                              allow_unverified_headline=False))
    assert code == 1, "an unsupported headline must not be recordable"
    assert cache_mod.load_answer(None, started["qhash"]) is None


def _capture(capsys, fn) -> str:
    capsys.readouterr()
    fn()
    return capsys.readouterr().out


def test_the_calls_behind_a_recorded_number_survive_an_index_rebuild(demo_dir, capsys):
    """The demo clicks "n calls" on a recorded claim. Tool results live only in the derived index,
    so without restoring them a fresh clone replays the answer and 404s on every drill-down."""
    test_record_verify_and_replay_a_demo_answer(demo_dir, capsys)
    stored = next(s for s in cache_mod.load_files())
    result_id = next(ev["payload"]["result_id"] for ev in stored.trace if ev.get("name") == "tool_result")

    gc.collect()                                # drop the connections the replay opened
    build(get_paths(demo_dir), quiet=True)      # rebuilds the index from files, as a fresh clone does

    con = connect(demo_dir / "voc.sqlite")
    row = con.execute("SELECT sql FROM tool_results WHERE result_id = ? AND qhash = ?",
                      (result_id, stored.qhash)).fetchone()
    assert row is not None, "the rebuild must re-register the recorded answer's tool results"

    from voc.store import queries as Q
    assert Q.rerun_call_ids(con, json.loads(row["sql"])), "re-executing the stored query must find its calls"
