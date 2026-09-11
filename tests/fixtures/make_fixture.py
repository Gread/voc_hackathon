"""Seeded synthetic corpus with planted patterns, for tests only.

Never write this into the repo's data/ directory: it exists so the analytics can be checked against
known answers (theme B ramps, C is brand new, D is concentrated in one region, E fades, A is flat).
Run directly: python tests/fixtures/make_fixture.py <dir>
"""
from __future__ import annotations

import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

WEEKS = 60
END_MONDAY = date(2026, 6, 22)          # a Monday; the fixture window ends here
PRODUCTS = ["checking_or_savings", "credit_card", "mortgage", "money_transfer_or_p2p"]
REGION_GROUPS = ["west", "southeast", "northeast", "midwest", "southwest"]
STATES = {"west": ["CA", "WA", "OR", "NV"], "southeast": ["FL", "GA", "NC"], "northeast": ["NY", "NJ", "PA"],
          "midwest": ["OH", "IL", "MI"], "southwest": ["TX", "AZ", "NM"]}
SEGMENTS = ["none", "none", "none", "older_american", "servicemember"]

# theme_key -> (driver_category, sentiment, wording templates)
THEMES = {
    "A": ("unexpected_charge", -1, [
        "A monthly fee of {amt} appeared although the account was advertised as free",
        "I was charged {amt} in maintenance fees nobody told me about",
        "The account fee went up to {amt} at renewal with no notice"]),
    "B": ("system_or_app_failure", -2, [
        "After the app update I cannot log in and the reset link never arrives",
        "The mobile app crashes on the login screen since the last update",
        "Online banking rejects my password after the new app version"]),
    "C": ("money_held_or_not_returned", -2, [
        "My deposit of {amt} has been held for ten days with no explanation",
        "The bank froze {amt} of my money and will not say why"]),
    "D": ("no_response_or_follow_up", -1, [
        "I was promised a callback about my dispute and nobody ever called",
        "Three weeks after the branch visit there is still no answer"]),
    "E": ("long_wait_or_delay", -1, [
        "I waited over an hour on hold and then the call dropped",
        "Every call means forty minutes of hold music"]),
    "P": ("helpful_staff", 1, [
        "The branch manager sorted the problem out in ten minutes",
        "The representative was patient and fixed the error the same day"]),
}


def week_start(index: int) -> date:
    return END_MONDAY - timedelta(weeks=WEEKS - 1 - index)


def plan_counts() -> dict[str, list[int]]:
    """Calls per theme per week index. B ramps over the last 8 weeks, C only in the last 3."""
    counts = {key: [0] * WEEKS for key in THEMES}
    for w in range(WEEKS):
        counts["A"][w] = 4                                    # flat
        counts["D"][w] = 3 if w % 2 == 0 else 2               # steady
        counts["E"][w] = max(0, 6 - w // 8)                   # fading
        counts["P"][w] = 2
        counts["B"][w] = 1 if w < WEEKS - 8 else 1 + int((w - (WEEKS - 9)) * 3)   # ramp to ~25
        counts["C"][w] = 3 if w >= WEEKS - 3 else 0           # brand new, 3 weeks, >= 2 weeks of support
    return counts


def build_fixture(data_dir: Path, seed: int = 7) -> dict:
    """Write calls.jsonl, extractions.jsonl and the theme files into data_dir."""
    rng = random.Random(seed)
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "themes").mkdir(exist_ok=True)
    counts = plan_counts()

    calls, extractions, members = [], [], []
    theme_ids = {key: f"thm_{i + 1:04d}" for i, key in enumerate(THEMES)}
    call_seq = 0

    for w in range(WEEKS):
        monday = week_start(w)
        for key, per_week in counts.items():
            driver, sentiment, wordings = THEMES[key]
            for _ in range(per_week[w]):
                call_seq += 1
                call_id = f"fx_{call_seq:05d}"
                day = monday + timedelta(days=rng.randrange(5))
                # D is concentrated in the west so a segment lift is detectable
                group = "west" if (key == "D" and rng.random() < 0.75) else rng.choice(REGION_GROUPS)
                product = "credit_card" if key == "A" else rng.choice(PRODUCTS)
                amount = f"${rng.choice([12, 25, 34, 95, 150, 300])}.00"
                statement = rng.choice(wordings).format(amt=amount)
                quote = f"{statement}, and I want this fixed."
                text = (f"On {day.isoformat()} I contacted the bank about my {product.replace('_', ' ')}. "
                        f"{quote} I have been a customer for years and expect better.")
                iso_year, iso_week, _ = day.isocalendar()
                calls.append({
                    "call_id": call_id, "source": "fixture", "shape": "narrative",
                    "date": day.isoformat(), "week": f"{iso_year}-W{iso_week:02d}", "month": day.isoformat()[:7],
                    "text": text, "text_sha": f"sha{call_seq:06d}", "product": product,
                    "product_raw": product, "sub_product_raw": None, "issue_raw": None, "sub_issue_raw": None,
                    "region": rng.choice(STATES[group]), "region_group": group, "channel": "web",
                    "segment": rng.choice(SEGMENTS), "company": "FIXTURE BANK", "sampling_fraction": 0.25,
                    "n_turns": None, "customer_char_ranges": None, "meta": {"fixture_theme": key},
                })
                start = text.index(quote)
                topic = {
                    "topic_label": driver.replace("_", " ")[:60], "issue_statement": statement,
                    "product": product, "sentiment": sentiment, "driver_category": driver,
                    "driver": f"{statement[:120]}", "outcome": "unresolved", "evidence_ok": 1,
                    "evidence": [{"quote": quote, "speaker": "narrative", "char_start": start,
                                  "char_end": start + len(quote), "verified": 1, "match_kind": "exact"}],
                }
                reason = {"unexpected_charge": "fees_and_charges", "system_or_app_failure": "access_or_digital_banking",
                          "money_held_or_not_returned": "funds_hold_or_account_restriction",
                          "no_response_or_follow_up": "customer_service_experience",
                          "long_wait_or_delay": "customer_service_experience",
                          "helpful_staff": "customer_service_experience"}[driver]
                extractions.append({
                    "call_id": call_id, "status": "ok", "error": None, "produced_by": "fixture",
                    "model": "fixture", "prompt_version": "ext-1.0", "schema_version": "1",
                    "extracted_at": "2026-09-11T00:00:00Z", "flags": [], "quote_verify_rate": 1.0,
                    "extraction": {
                        "contact_reasons": [{"reason": reason, "specific_reason": statement[:160], "is_primary": True}],
                        "products": [product], "services": [], "customer_ask": "fix_error",
                        "stated_reason": statement[:160], "underlying_driver": statement[:200],
                        "reason_differs": False, "topics": [topic], "overall_sentiment": sentiment,
                        "resolution_status": "unresolved", "positive_moments": [], "redaction_heavy": False,
                        "summary": statement[:200]},
                })
                members.append({"topic_id": f"{call_id}:0", "theme_id": theme_ids[key], "confidence": 0.95,
                                "pass": "reassign", "batch_id": f"fx:{key}"})

    themes = []
    for key, (driver, sentiment, wordings) in THEMES.items():
        themes.append({
            "theme_id": theme_ids[key],
            "name": f"Theme {key}: {driver.replace('_', ' ')}",
            "problem_statement": wordings[0].format(amt="$34.00"),
            "root_cause": f"fixture cause for {key}",
            "polarity": "positive" if sentiment > 0 else "negative",
            "driver_category": driver, "bucket": f"{driver}|{'positive' if sentiment > 0 else 'negative'}",
            "status": "active", "merged_into": None, "created_pass": "seed", "codebook_version": 1,
            "examples": [w.format(amt="$34.00") for w in wordings[:2]],
        })

    def write_jsonl(path: Path, rows: list[dict]) -> None:
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    write_jsonl(data_dir / "calls.jsonl", calls)
    write_jsonl(data_dir / "extractions.jsonl", extractions)
    write_jsonl(data_dir / "themes" / "members.jsonl", members)
    (data_dir / "themes" / "registry.json").write_text(json.dumps(
        {"theme_prompt_version": "thm-1.0", "codebook_version": 1, "produced_by": "fixture", "themes": themes},
        ensure_ascii=False, indent=1), encoding="utf-8")
    (data_dir / "themes" / "merges.json").write_text(json.dumps({"merges": [], "decisions": []}), encoding="utf-8")
    (data_dir / "profile.json").write_text(json.dumps({
        "company": "FIXTURE BANK", "source": "fixture", "sampling_fraction": 0.25, "seed": seed,
        "window": {"start": calls[0]["month"], "end": calls[-1]["month"]},
        "population_by_month": {}}, indent=1), encoding="utf-8")

    return {"n_calls": len(calls), "theme_ids": theme_ids, "counts": counts,
            "last_week": calls[-1]["week"], "weeks": [f"{week_start(w).isocalendar()[0]}-W{week_start(w).isocalendar()[1]:02d}" for w in range(WEEKS)]}


if __name__ == "__main__":
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture_data")
    info = build_fixture(target)
    print(f"wrote {info['n_calls']} calls to {target} (themes: {', '.join(info['theme_ids'].values())})")
