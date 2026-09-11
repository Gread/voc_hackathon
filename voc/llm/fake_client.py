"""Deterministic stand-in for tests and CI. Outputs validate against the real schemas but are
heuristic; files it produces carry produced_by="fake" and never enter data/."""
from __future__ import annotations

import re
from typing import Any

from voc.llm.client import LLMRequest, LLMResult, Usage

# keyword -> (contact reason, driver category)
RULES: list[tuple[str, str, str]] = [
    (r"\b(fee|fees|overdraft|interest|charged)\b", "fees_and_charges", "unexpected_charge"),
    (r"\b(fraud|scam|unauthori[sz]ed|stolen|identity)\b", "unauthorized_or_fraud", "fraud_not_stopped_or_not_refunded"),
    (r"\b(dispute|chargeback|merchant)\b", "dispute_or_chargeback", "denied_or_declined_without_explanation"),
    (r"\b(zelle|wire|transfer|deposit|payment)\b", "payment_or_transfer_problem", "money_held_or_not_returned"),
    (r"\b(hold|froze|frozen|restricted|locked)\b", "funds_hold_or_account_restriction", "money_held_or_not_returned"),
    (r"\b(app|login|online|website|password)\b", "access_or_digital_banking", "system_or_app_failure"),
    (r"\b(closed|close|closing|opened|open)\b", "account_opening_or_closure", "denied_or_declined_without_explanation"),
    (r"\b(statement|balance)\b", "balance_or_statement_error", "error_not_corrected"),
    (r"\b(mortgage|escrow|loan|payoff)\b", "loan_servicing", "incorrect_or_conflicting_information"),
    (r"\b(denied|limit|application)\b", "credit_decision_or_limit", "denied_or_declined_without_explanation"),
    (r"\b(credit report|bureau|equifax|experian|transunion)\b", "credit_reporting", "error_not_corrected"),
    (r"\b(collection|collector|debt)\b", "collections_or_debt", "incorrect_or_conflicting_information"),
    (r"\b(callback|call back|hold time|rude|representative|customer service)\b", "customer_service_experience", "no_response_or_follow_up"),
    (r"\b(promotion|bonus|points|rewards)\b", "rewards_or_promotions", "policy_or_terms_change"),
]
PRODUCT_RULES = [
    (r"\b(credit card|card)\b", "credit_card"), (r"\b(checking|savings|debit|atm)\b", "checking_or_savings"),
    (r"\b(mortgage|escrow|home loan)\b", "mortgage"), (r"\b(zelle|wire|transfer)\b", "money_transfer_or_p2p"),
    (r"\b(auto loan|car loan|vehicle)\b", "auto_loan"), (r"\b(collector|collection)\b", "debt_collection"),
]
SERVICE_RULES = [(r"\bapp\b", "mobile_app"), (r"\bonline\b", "online_banking"), (r"\bbranch\b", "branch"),
                 (r"\b(phone|called|call)\b", "phone_support"), (r"\batm\b", "atm"), (r"\b(chat|email)\b", "chat_or_email")]


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) >= 8]


def _quote(text: str, pattern: str) -> str:
    for s in _sentences(text):
        if re.search(pattern, s, re.I):
            return s[:300]
    sents = _sentences(text)
    return (sents[0] if sents else text)[:300]


def fake_extraction(text: str) -> dict[str, Any]:
    low = text.lower()
    hits = [(reason, driver, pat) for pat, reason, driver in RULES if re.search(pat, low)]
    if not hits:
        hits = [("other_or_unclear", "other_or_unclear", r".")]
    hits = hits[:3]
    products = [code for pat, code in PRODUCT_RULES if re.search(pat, low)][:3] or ["other_or_unspecified"]
    services = [code for pat, code in SERVICE_RULES if re.search(pat, low)][:3]
    angry = bool(re.search(r"\b(furious|lawyer|attorney|regulator|cfpb|never again|worst)\b", low))
    sentiment = -2 if angry else -1
    topics = []
    for i, (reason, driver, pat) in enumerate(hits):
        q = _quote(text, pat)
        topics.append({
            "topic_label": reason.replace("_", " ")[:60],
            "issue_statement": f"Customer reports a problem about {reason.replace('_', ' ')}: {q[:120]}",
            "product": products[0], "sentiment": sentiment, "driver_category": driver,
            "driver": f"{driver.replace('_', ' ')} described in the text",
            "outcome": "unknown", "evidence": [{"quote": q, "speaker": "narrative"}],
        })
    positive = []
    m = re.search(r"[^.!?]*\b(thank|helpful|resolved quickly|great service)\b[^.!?]*[.!?]", text, re.I)
    if m and len(m.group(0).strip()) >= 8:
        positive.append({"what": "something went right", "category": "helpful_staff",
                         "quote": m.group(0).strip()[:300], "speaker": "narrative"})
    return {
        "contact_reasons": [{"reason": r, "specific_reason": f"{r.replace('_', ' ')} (fake)", "is_primary": i == 0}
                            for i, (r, _, _) in enumerate(hits)],
        "products": products, "services": services,
        "customer_ask": "refund_or_reversal" if "refund" in low else "fix_error",
        "stated_reason": (_sentences(text) or [text])[0][:160],
        "underlying_driver": hits[0][1].replace("_", " "),
        "reason_differs": False, "topics": topics, "overall_sentiment": sentiment,
        "resolution_status": "resolved" if re.search(r"\bresolved\b", low) else "unresolved",
        "positive_moments": positive, "redaction_heavy": low.count("xxxx") > 12,
        "summary": (_sentences(text) or [text])[0][:200],
    }


def fake_theme_assign(rows: list[dict[str, Any]], registry: list[dict[str, Any]], allow_new: bool) -> dict[str, Any]:
    """Group by (driver_category, product); reuse a registry theme whose name encodes the same key."""
    by_key = {t.get("name", ""): t["theme_id"] for t in registry}
    assignments, new_themes, tmp = [], [], {}
    for r in rows:
        key = f"{r.get('driver_category', 'other')} / {r.get('product', 'other')}"
        if key in by_key:
            assignments.append({"topic_id": r["topic_id"], "theme_id": by_key[key], "confidence": 0.9})
        elif allow_new:
            if key not in tmp:
                tmp[key] = f"NEW-{len(tmp) + 1}"
                new_themes.append({"tmp_id": tmp[key], "name": key,
                                   "problem_statement": f"Customers describe {key.split(' / ')[0].replace('_', ' ')} on {key.split(' / ')[1].replace('_', ' ')}",
                                   "root_cause": "fake grouping by driver category and product",
                                   "polarity": "negative" if int(r.get("sentiment", -1)) < 0 else ("positive" if int(r.get("sentiment", -1)) > 0 else "neutral")})
            assignments.append({"topic_id": r["topic_id"], "theme_id": tmp[key], "confidence": 0.8})
        else:
            assignments.append({"topic_id": r["topic_id"], "theme_id": "NONE", "confidence": 0.0})
    return {"assignments": assignments, "new_themes": new_themes}


class FakeClient:
    def _run(self, req: LLMRequest) -> LLMResult:
        if req.stage == "extract":
            data = fake_extraction(req.meta.get("text", req.user))
        elif req.stage in ("theme_seed", "theme_reassign"):
            data = fake_theme_assign(req.meta.get("rows", []), req.meta.get("registry", []), req.stage == "theme_seed")
            if req.stage == "theme_reassign":
                data = {"assignments": data["assignments"]}
        elif req.stage == "theme_consolidate":
            data = {"decisions": [{"a": p["a"], "b": p["b"], "merge": False, "into": p["a"], "reason": "fake: keep separate"}
                                  for p in req.meta.get("pairs", [])]}
        elif req.stage == "theme_rename":
            data = {"themes": [{"theme_id": t["theme_id"], "name": t["name"], "problem_statement": t["problem_statement"],
                                "root_cause": t["root_cause"]} for t in req.meta.get("registry", [])]}
        else:
            raise ValueError(f"FakeClient has no behaviour for stage {req.stage}")
        return LLMResult(data=data, usage=Usage(), model="fake", produced_by="fake")

    def complete_json(self, req: LLMRequest) -> LLMResult:
        return self._run(req)

    async def acomplete_json(self, req: LLMRequest) -> LLMResult:
        return self._run(req)
