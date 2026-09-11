"""CFPB pull (mocked transport), eligibility/dedupe, hash sampling, profile gate."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import httpx
import pytest

from voc.ingest import cfpb
from voc.ingest.normalize import read_jsonl
from voc.ingest.profile import build_profile, evaluate_gate, format_table
from voc.ingest.sample import eligible_rows, implied_fraction, keep_score, sample, select
from voc.paths import get_paths

FIXTURES = Path(__file__).parent / "fixtures"
COMPANY = "EXAMPLE BANK, N.A."


def _page() -> dict:
    return json.loads((FIXTURES / "cfpb_page_sample.json").read_text(encoding="utf-8"))


def _client(requests: list[httpx.Request], *, fail_first: bool = False) -> httpx.Client:
    """Fake API: full first page for 2024-07, empty page after search_after, nothing for other months."""
    state = {"failed": False}

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if fail_first and not state["failed"]:
            state["failed"] = True
            return httpx.Response(429, json={"error": "slow down"})
        q = request.url.params
        if q.get("date_received_min") != "2024-07-01" or q.get("search_after"):
            return httpx.Response(200, json={"hits": {"hits": []}})
        return httpx.Response(200, json=_page())

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_fetch_month_pages_with_search_after():
    seen: list[httpx.Request] = []
    rows = cfpb.fetch_month(_client(seen), COMPANY, cfpb.PRODUCTS, "2024-07", size=7, pause=0, sleep=lambda s: None)
    # the boundary-day row (9000007, received 2024-08-01) is returned by the API but filtered out
    assert [r["complaint_id"] for r in rows] == [f"90000{i:02d}" for i in range(1, 7)]
    assert len(seen) == 2
    first, second = (r.url.params for r in seen)
    assert first["company"] == COMPANY and first["has_narrative"] == "true" and first["no_aggs"] == "true"
    assert first["date_received_min"] == "2024-07-01" and first["date_received_max"] == "2024-08-01"
    assert first.get_list("product") == cfpb.PRODUCTS and "format" not in first
    assert second["search_after"] == "1722481200000_9000007"


def test_get_json_retries_on_429():
    seen: list[httpx.Request] = []
    naps: list[float] = []
    rows = cfpb.fetch_month(_client(seen, fail_first=True), COMPANY, cfpb.PRODUCTS, "2024-07",
                            pause=0, sleep=naps.append)
    assert len(rows) == 6 and len(naps) >= 1


def test_pull_caches_months_and_skips_cached(data_dir: Path, capsys):
    paths = get_paths().ensure()
    seen: list[httpx.Request] = []
    counts = cfpb.pull(paths, COMPANY, "2024-07", "2024-08", client=_client(seen), pause=0, sleep=lambda s: None)
    assert counts == {"2024-07": 6, "2024-08": 0}
    raw = paths.raw_cfpb / "example_bank_n_a" / "2024-07.jsonl"
    assert raw.exists() and len(list(read_jsonl(raw))) == 6 and not raw.with_suffix(".jsonl.tmp").exists()
    n_requests = len(seen)
    counts = cfpb.pull(paths, COMPANY, "2024-07", "2024-08", client=_client(seen), pause=0, sleep=lambda s: None)
    assert counts == {"2024-07": 6, "2024-08": 0} and len(seen) == n_requests
    assert "(cached)" in capsys.readouterr().out


def test_keep_score_is_deterministic_and_uniform_ish():
    assert keep_score(20260911, 9000001) == keep_score(20260911, "9000001")
    assert keep_score(20260911, 9000001) != keep_score(1, 9000001)
    scores = [keep_score(20260911, i) for i in range(2000)]
    assert all(0.0 <= s < 1.0 for s in scores)
    assert 0.4 < sum(s < 0.5 for s in scores) / len(scores) < 0.6


def test_eligible_rows_dedupes_and_drops_short():
    rows = [h["_source"] for h in _page()["hits"]["hits"]]
    eligible = eligible_rows({"2024-07": rows[:6], "2024-08": [rows[6], rows[0]]}, min_words=30)
    ids = [p["_cid"] for p in eligible]
    # sorted by date; 9000003 (same text) and the repeated 9000001 dropped, 9000004 too short
    assert ids == [9000002, 9000006, 9000001, 9000005, 9000007]
    eligible = eligible_rows({"2024-07": rows[:6]}, min_words=30)
    assert implied_fraction(3, len(eligible)) == 0.75 and implied_fraction(10, 4) == 1.0
    chosen = select(eligible, 0.75, 20260911)
    assert [p["_cid"] for p in chosen] == [p["_cid"] for p in eligible if keep_score(20260911, p["_cid"]) < 0.75]


def _seed_raw(paths) -> None:
    cfpb.pull(paths, COMPANY, "2024-07", "2024-07", client=_client([]), pause=0, sleep=lambda s: None)


def test_sample_writes_calls_and_population(data_dir: Path):
    paths = get_paths().ensure()
    _seed_raw(paths)
    profile = sample(paths, COMPANY, "2024-07", "2024-07", target=3, seed=20260911)
    calls = list(read_jsonl(paths.calls))
    assert profile["n_eligible"] == 4 and profile["sampling_fraction"] == 0.75
    assert len(calls) == profile["n_sampled"] == sum(keep_score(20260911, i) < 0.75 for i in (9000001, 9000002, 9000005, 9000006))
    assert calls == sorted(calls, key=lambda r: (r["date"], r["call_id"]))
    assert all(r["sampling_fraction"] == 0.75 and r["source"] == "cfpb" and r["company"] == COMPANY for r in calls)
    assert all(r["text_sha"] and r["week"].startswith("2024-W") for r in calls)
    saved = json.loads(paths.profile.read_text(encoding="utf-8"))
    assert saved["population_by_month"] == {"2024-07": 4}
    # re-running is byte-identical
    before = paths.calls.read_bytes()
    sample(paths, COMPANY, "2024-07", "2024-07", target=3, seed=20260911)
    assert paths.calls.read_bytes() == before


def test_profile_gate_and_table(data_dir: Path, monkeypatch, capsys):
    paths = get_paths().ensure()
    _seed_raw(paths)
    profile = build_profile(paths, COMPANY, "2024-07", "2024-08", target=3)
    assert profile["source"] == "cfpb_api_raw" and profile["n_eligible"] == 4
    assert [m["month"] for m in profile["months"]] == ["2024-07", "2024-08"]
    assert profile["counts"]["product"] == {"checking_or_savings": 1, "credit_card": 1, "money_transfer_or_p2p": 1, "mortgage": 1}
    assert profile["counts"]["segment"]["servicemember"] == 1
    gate = profile["gate"]
    assert gate["pass"] is False and gate["checks"]["months_present"]["missing"] == ["2024-08"]
    table = format_table(profile)
    assert "gate: FAIL" in table and "2024-07" in table
    saved = json.loads(paths.profile.read_text(encoding="utf-8"))
    assert saved["gate"] == gate
    # profile_report.py prints the same table without recomputing
    script = Path(__file__).resolve().parent.parent / "scripts" / "profile_report.py"
    out = subprocess.run([sys.executable, str(script), "--path", str(paths.profile)],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    assert out.stdout.strip() == table.strip()


def test_evaluate_gate_passes_with_enough_support():
    weeks = {f"2025-W{w:02d}": 400 for w in range(1, 11)}
    weeks["2025-W11"] = 10  # one thin week out of eleven is still >= 90 % coverage
    counts = {"month": {"2025-01": 4010}, "week": weeks,
              "product": {"credit_card": 2000, "checking_or_savings": 1500, "mortgage": 510},
              "segment": {"none": 3000, "servicemember": 700, "older_american": 310}, "region_group": {}}
    gate = evaluate_gate(counts, 1.0, ["2025-01"])
    assert gate["pass"] is True and gate["checks"]["weekly_support"]["weeks_ok"] == 10
    thin = evaluate_gate(counts, 0.1, ["2025-01"])
    assert thin["pass"] is False and thin["checks"]["products"]["pass"] is False
