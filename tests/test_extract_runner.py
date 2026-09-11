"""End-to-end extract stage on the fixture with VOC_LLM=fake: cache files, consolidation, resumability,
export/load round trip with an agent-shaped cache file, dry run and report."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from voc.cli import main
from voc.extract import load, runner
from voc.extract.prompt import PROMPT_VERSION, cache_key
from voc.paths import get_paths
from voc.schemas.extraction import SCHEMA_VERSION

FIXTURE = Path(__file__).parent / "fixtures" / "calls_sample.jsonl"


@pytest.fixture
def calls_dir(data_dir: Path) -> Path:
    shutil.copy(FIXTURE, data_dir / "calls.jsonl")
    return data_dir


def _rows(data_dir: Path) -> list[dict]:
    return load.read_jsonl(data_dir / "extractions.jsonl")


def test_fake_run_writes_cache_files_and_extractions(calls_dir: Path):
    assert main(["extract"]) == 0
    calls = load.load_calls(calls_dir / "calls.jsonl")
    files = sorted((calls_dir / "cache" / "extract").glob("*.json"))
    assert len(files) == len(calls) == 8
    payload = json.loads(files[0].read_text(encoding="utf-8"))
    assert payload["produced_by"] == "fake" and payload["prompt_version"] == PROMPT_VERSION
    assert payload["schema_version"] == SCHEMA_VERSION and payload["key"] == cache_key(payload["text_sha"])
    rows = _rows(calls_dir)
    assert [r["call_id"] for r in rows] == sorted(c.call_id for c in calls)
    assert all(r["status"] == "ok" and r["produced_by"] == "fake" for r in rows)
    ok = {r["call_id"]: r for r in rows}
    assert ok["cfpb_9000006"]["extraction"]["redaction_heavy"] is True or "heavy_redaction" in ok["cfpb_9000006"]["flags"]
    transcript = ok["conv_0000101"]["extraction"]
    speakers = {ev["speaker"] for t in transcript["topics"] for ev in t["evidence"] if ev["verified"]}
    assert speakers <= {"customer", "agent"} and speakers
    assert all(r["quote_verify_rate"] == 1.0 for r in rows)
    run_log = load.read_jsonl(calls_dir / "work" / "extract_runs.jsonl")
    assert len(run_log) == 1 and run_log[0]["n_ok"] == 8


def test_second_run_touches_nothing(calls_dir: Path):
    main(["extract"])
    cache_dir = calls_dir / "cache" / "extract"
    before = {p.name: p.stat().st_mtime_ns for p in cache_dir.glob("*.json")}
    calls = load.load_calls(calls_dir / "calls.jsonl")
    assert runner.select_pending(calls) == []
    assert main(["extract"]) == 0
    after = {p.name: p.stat().st_mtime_ns for p in cache_dir.glob("*.json")}
    assert before == after
    assert len(_rows(calls_dir)) == 8


def test_limit_ids_and_round_robin(calls_dir: Path):
    calls = load.load_calls(calls_dir / "calls.jsonl")
    order = runner.round_robin_by_month(calls)
    assert [c.month for c in order] == sorted({c.month for c in calls})   # one per month, months ascending
    assert main(["extract", "--limit", "3"]) == 0
    assert len(_rows(calls_dir)) == 3
    ids = calls_dir / "ids.txt"
    ids.write_text("cfpb_9000007\n", encoding="utf-8")
    assert main(["extract", "--ids", str(ids)]) == 0
    assert {r["call_id"] for r in _rows(calls_dir)} >= {"cfpb_9000007"} and len(_rows(calls_dir)) == 4


def test_export_and_load_round_trip_with_agent_file(calls_dir: Path):
    out = calls_dir / "bundles"
    assert main(["extract", "--export", str(out), "--bundle-size", "3"]) == 0
    bundles = sorted(out.glob("bundle_*.json"))
    assert len(bundles) == 3 and (out / "README.md").exists()
    b0 = json.loads(bundles[0].read_text(encoding="utf-8"))
    assert b0["bundle_id"] == "bundle_000" and b0["schema"]["type"] == "object"
    assert "Worked example 1" in b0["system_prompt"] and len(b0["records"]) == 3
    rec = next(r for b in bundles for r in json.loads(b.read_text(encoding="utf-8"))["records"] if r["call_id"] == "cfpb_9000002")
    assert rec["cache_key"] == cache_key(rec["text_sha"]) and rec["cache_name"] == "cfpb_9000002"

    # an agent writes one good file and one broken file by hand
    cache_dir = get_paths().cache_extract
    good = {"call_id": rec["call_id"], "key": rec["cache_key"], "prompt_version": PROMPT_VERSION,
            "schema_version": SCHEMA_VERSION, "taxonomy_version": b0["taxonomy_version"], "text_sha": rec["text_sha"],
            "model": "claude-agent-build", "produced_by": "claude_agent", "created_at": "2026-09-12T10:00:00+00:00",
            "usage": None, "response": _agent_extraction(rec["text"])}
    (cache_dir / "cfpb_9000002.json").write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
    broken = dict(good, call_id="cfpb_9000001", key=cache_key(_sha(calls_dir, "cfpb_9000001")),
                  response={"contact_reasons": [], "topics": []})
    (cache_dir / "cfpb_9000001.json").write_text(json.dumps(broken), encoding="utf-8")

    assert main(["extract", "--load"]) == 0
    rows = {r["call_id"]: r for r in _rows(calls_dir)}
    assert set(rows) == {"cfpb_9000001", "cfpb_9000002"}
    assert rows["cfpb_9000002"]["status"] == "ok" and rows["cfpb_9000002"]["produced_by"] == "claude_agent"
    assert rows["cfpb_9000002"]["extracted_at"] == "2026-09-12T10:00:00+00:00"
    ev = rows["cfpb_9000002"]["extraction"]["topics"][0]["evidence"][0]
    assert ev["verified"] == 1 and ev["match_kind"] == "normalized"
    assert rows["cfpb_9000001"]["status"] == "error" and "no contact_reasons" in rows["cfpb_9000001"]["error"]

    # the runner treats the agent file as done and re-requests only the broken one with --retry-errors
    calls = load.load_calls(calls_dir / "calls.jsonl")
    pending = runner.select_pending(calls)
    assert "cfpb_9000002" not in {c.call_id for c in pending} and "cfpb_9000001" not in {c.call_id for c in pending}
    pending = runner.select_pending(calls, retry_errors=True)
    assert {c.call_id for c in pending} == {c.call_id for c in calls} - {"cfpb_9000002"}
    assert main(["extract"]) == 0
    rows = {r["call_id"]: r for r in _rows(calls_dir)}
    assert len(rows) == 8 and rows["cfpb_9000002"]["produced_by"] == "claude_agent"
    assert rows["cfpb_9000001"]["status"] == "ok" and rows["cfpb_9000001"]["produced_by"] == "fake"

    # a second export has nothing left to hand out
    out2 = calls_dir / "bundles2"
    assert main(["extract", "--export", str(out2)]) == 0
    assert list(out2.glob("bundle_*.json")) == []


def test_stale_key_and_error_marker_are_pending(calls_dir: Path):
    main(["extract"])
    calls = load.load_calls(calls_dir / "calls.jsonl")
    cache_dir = get_paths().cache_extract
    p = cache_dir / "cfpb_9000003.json"
    payload = json.loads(p.read_text(encoding="utf-8"))
    payload["key"] = "0" * 64
    p.write_text(json.dumps(payload), encoding="utf-8")
    main(["extract", "--load"])
    row = next(r for r in _rows(calls_dir) if r["call_id"] == "cfpb_9000003")
    assert row["status"] == "error" and row["error"].startswith("stale cache key")
    assert {c.call_id for c in runner.select_pending(calls)} == {"cfpb_9000003"}
    assert main(["extract"]) == 0
    assert all(r["status"] == "ok" for r in _rows(calls_dir))


def test_dry_run_and_report(calls_dir: Path, capsys: pytest.CaptureFixture[str]):
    assert main(["extract", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert '"pending": 8' in out and '"counted_via": "estimate"' in out and "projected_usd" in out
    main(["extract"])
    assert main(["extract", "--report"]) == 0
    rep = json.loads((calls_dir / "work" / "extract_report.json").read_text(encoding="utf-8"))
    assert rep["n_ok"] == 8 and rep["n_error"] == 0 and rep["n_missing"] == 0
    assert rep["quote_verify_rate"] == 1.0 and rep["topics_per_call"] >= 1
    assert 0 <= rep["primary_reason_agreement"] <= 1 and rep["primary_reason_agreement_n"] == 7
    assert rep["produced_by"] == {"fake": 8}


# --- helpers ---------------------------------------------------------------------------------

def _sha(data_dir: Path, call_id: str) -> str:
    return next(c.text_sha for c in load.load_calls(data_dir / "calls.jsonl") if c.call_id == call_id)


def _agent_extraction(text: str) -> dict:
    """A hand-shaped agent answer for cfpb_9000002 with a curly-quote variant of a real span."""
    quote = "the agent on the phone told me the $95.00 annual fee would be waived"
    assert quote in text
    return {
        "contact_reasons": [{"reason": "fees_and_charges", "specific_reason": "annual fee charged after a promised waiver", "is_primary": True}],
        "products": ["credit_card"], "services": ["phone_support"], "customer_ask": "refund_or_reversal",
        "stated_reason": "wants the $95.00 annual fee reversed",
        "underlying_driver": "a phone agent promised the fee would be waived at renewal; a supervisor says there is no record",
        "reason_differs": False,
        "topics": [{"topic_label": "annual fee after promised waiver",
                    "issue_statement": "The $95.00 annual fee was charged although the renewal agent said it would be waived, and a supervisor refused to remove it.",
                    "product": "credit_card", "sentiment": -1, "driver_category": "unexpected_charge",
                    "driver": "$95.00 fee appeared two months after a waiver promise; no record of the promise",
                    "outcome": "unresolved",
                    "evidence": [{"quote": quote.replace("$95.00 annual fee", "$95.00  annual fee"), "speaker": "narrative"}]}],
        "overall_sentiment": -1, "resolution_status": "unresolved", "positive_moments": [],
        "redaction_heavy": False, "summary": "Annual fee charged despite a promised waiver; supervisor refused to reverse it.",
    }
