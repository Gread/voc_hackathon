"""Templated analyst used when no model is available: a keyword router over the same tools, producing
an Answer that goes through the same server verifier. Always badged "templated (no model)"."""
from __future__ import annotations

import re
import sqlite3
from typing import Any

from voc.agent.tools import ToolContext, run_tool
from voc.schemas.answer import Answer, Chart, Claim, KeyNumber, Quote
from voc.schemas.filters import Filters

ARCHETYPES = [
    ("emerging", r"\b(new|newest|emerging|grow\w*|fastest|accelerat\w*|rising|spike|early signal)\b"),
    ("same_problem", r"\b(same (underlying )?problem|different ways|different words|wording|describ\w* the same)\b"),
    ("satisfaction", r"\b(satisf\w*|happy|positive|delight\w*|protect|good experience|works well|praise)\b"),
    ("segments", r"\b(differ\w*|by product|by segment|by region|segment\w*|breakdown|compare|between)\b"),
    ("evidence", r"\b(evidence|support\w*|how many calls|based on|which statements|back (this|it) up)\b"),
    ("quotes", r"\b(what did|actual\w*|verbatim|say|said|quote\w*|their words)\b"),
    ("drivers", r"\b(negative|dissatisf\w*|complain\w*|frustrat\w*|anger|angry|pain|cause\w*|driver\w*|trigger\w*|worst|problem\w*)\b"),
    ("volume", r"\b(most|top|volume|contact\w*|about what|chang\w*|trend\w*)\b"),
]


def classify(question: str) -> str:
    q = question.lower()
    for name, pattern in ARCHETYPES:
        if re.search(pattern, q):
            return name
    return "volume"


def _pct(x: Any) -> str:
    try:
        return f"{float(x):.1f}%"
    except (TypeError, ValueError):
        return "?"


def _call(ctx: ToolContext, con: sqlite3.Connection, name: str, args: dict[str, Any],
          results: dict[str, dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any] | None:
    t = len(events) * 700
    events.append({"name": "tool_call", "payload": {"id": f"off_{len(events)}", "name": name, "args": args}, "t_ms": t})
    try:
        env = run_tool(name, args, con, ctx)
    except Exception as exc:
        events.append({"name": "status", "payload": {"text": f"{name} failed: {exc}"}, "t_ms": t + 200})
        return None
    results[env["result_id"]] = ctx.results.get(env["result_id"], env)
    rows = env.get("rows")
    events.append({"name": "tool_result", "payload": {"id": f"off_{len(events) - 1}", "result_id": env["result_id"],
                                                      "name": name, "summary": env.get("summary", ""),
                                                      "n_rows": len(rows) if isinstance(rows, list) else None,
                                                      "sql": env.get("sql", [])}, "t_ms": t + 400})
    return env


def _quotes_for(ctx: ToolContext, con: sqlite3.Connection, entity_type: str, entity_id: str | None,
                filters: Filters, results: dict[str, dict[str, Any]], events: list[dict[str, Any]],
                n: int = 3) -> list[Quote]:
    env = _call(ctx, con, "get_quotes", {"entity_type": entity_type, "entity_id": entity_id, "call_ids": None,
                                         "filters": filters.model_dump(), "n": n, "polarity": "any", "diverse": True},
                results, events)
    if not env:
        return []
    return [Quote(evidence_id=r["evidence_id"], call_id=r["call_id"], quote=r["quote"], why="") for r in env.get("rows", [])[:n]]


def answer_offline(question: str, filters: Filters, con: sqlite3.Connection, *, as_of_week: str | None = None,
                   results: dict[str, dict[str, Any]] | None = None) -> tuple[Answer, dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Build a templated answer from real tool results. Returns (answer, results, trace events)."""
    results = dict(results or {})
    events: list[dict[str, Any]] = [{"name": "status", "payload": {"text": "templated analyst: planning tools"}, "t_ms": 0}]
    ctx = ToolContext(con=con, qhash="offline", as_of_week=as_of_week, counter=len(results))
    fdump = filters.model_dump()
    kind = classify(question)
    claims: list[Claim] = []
    quotes: list[Quote] = []
    charts: list[Chart] = []
    caveats: list[str] = []
    lines: list[str] = []

    def add_claim(statement: str, env: dict[str, Any], rows: list[dict[str, Any]], headline: bool,
                  n_calls: int, theme_ids: list[str] | None = None, numbers: list[KeyNumber] | None = None) -> str:
        cid = f"c{len(claims) + 1}"
        claims.append(Claim(id=cid, statement=statement, headline=headline, result_ids=[env["result_id"]],
                            call_ids=list(env.get("call_ids") or [])[:50], n_calls=n_calls,
                            theme_ids=theme_ids or [], key_numbers=numbers or []))
        return cid

    if kind in ("volume",):
        env = _call(ctx, con, "contact_reasons", {"filters": fdump, "compare_with_previous": True}, results, events)
        rows = (env or {}).get("rows", [])[:5]
        if rows:
            top = rows[0]
            cid = add_claim(f"The most common contact reason is {top.get('label', top.get('reason'))} "
                            f"({top.get('n_calls')} calls, {_pct(top.get('share_pct'))} of the scope).", env, rows, True,
                            int(top.get("n_calls", 0)),
                            numbers=[KeyNumber(label="calls", value=float(top.get("n_calls", 0)), result_id=env["result_id"])])
            lines.append(f"Customers contact us most about **{top.get('label', top.get('reason'))}**: "
                         f"{top.get('n_calls')} calls, {_pct(top.get('share_pct'))} of the scope [{cid}].")
            movers = [r for r in rows if (r.get("direction") or "flat") != "flat"]
            if movers:
                m = movers[0]
                cid2 = add_claim(f"{m.get('label', m.get('reason'))} is {m.get('direction')} "
                                 f"({m.get('n_calls')} calls, {m.get('delta_share_pts', 0)} share points).", env, rows, False,
                                 int(m.get("n_calls", 0)))
                lines.append(f"The clearest movement is **{m.get('label', m.get('reason'))}**, {m.get('direction')} "
                             f"by {m.get('delta_share_pts', 0)} share points [{cid2}].")
            lines.append("Other frequent reasons: " + ", ".join(
                f"{r.get('label', r.get('reason'))} ({r.get('n_calls')})" for r in rows[1:4]) + ".")
            charts.append(Chart(kind="bars", title="Contact reasons", result_id=env["result_id"], series_key="n_calls"))

    elif kind == "drivers":
        env = _call(ctx, con, "sentiment_drivers", {"polarity": "negative", "group_by": "theme",
                                                    "filters": fdump, "limit": 5}, results, events)
        rows = (env or {}).get("rows", [])
        if rows:
            top = rows[0]
            cid = add_claim(f"The largest source of negative sentiment is {top.get('name')} "
                            f"({top.get('n_calls')} calls).", env, rows, True, int(top.get("n_calls", 0)),
                            theme_ids=[str(top.get("key"))] if top.get("key") else [])
            triggers = ", ".join(t.get("text", "")[:80] for t in (top.get("top_specific_drivers") or [])[:2])
            lines.append(f"The largest driver of negative sentiment is **{top.get('name')}** "
                         f"({top.get('n_calls')} calls) [{cid}].")
            if triggers:
                lines.append(f"What specifically triggers it: {triggers}.")
            for r in rows[1:4]:
                lines.append(f"- {r.get('name')}: {r.get('n_calls')} calls.")
            quotes = [Quote(evidence_id=q["evidence_id"], call_id=q["call_id"], quote=q["quote"], why="")
                      for r in rows[:2] for q in (r.get("quotes") or [])[:1]]

    elif kind == "satisfaction":
        env = _call(ctx, con, "sentiment_drivers", {"polarity": "positive", "group_by": "driver_category",
                                                    "filters": fdump, "limit": 5}, results, events)
        rows = (env or {}).get("rows", [])
        caveats.append("This is a complaint corpus, so these are positive moments inside complaints, "
                       "not a measure of overall satisfaction.")
        if rows:
            top = rows[0]
            cid = add_claim(f"The most frequent positive moment is {top.get('name')} ({top.get('n_calls')} calls).",
                            env, rows, True, int(top.get("n_calls", 0)))
            lines.append(f"Even inside complaints, customers name things that went right. The most frequent is "
                         f"**{top.get('name')}** ({top.get('n_calls')} calls) [{cid}].")
            for r in rows[1:4]:
                lines.append(f"- {r.get('name')}: {r.get('n_calls')} calls.")
            quotes = [Quote(evidence_id=q["evidence_id"], call_id=q["call_id"], quote=q["quote"], why="")
                      for r in rows[:3] for q in (r.get("quotes") or [])[:1]]

    elif kind == "emerging":
        env = _call(ctx, con, "emerging_themes", {"as_of_week": as_of_week, "min_recent": 5, "only_new": False,
                                                  "filters": fdump, "limit": 8}, results, events)
        rows = (env or {}).get("rows", [])
        data = (env or {}).get("data", {})
        if rows:
            top = rows[0]
            cid = add_claim(f"{top.get('name')} is {top.get('status')}: {top.get('n_recent')} calls in the last four "
                            f"weeks against {top.get('expected_recent')} expected.", env, rows, True,
                            int(top.get("n_recent", 0)), theme_ids=[str(top.get("theme_id"))] if top.get("theme_id") else [])
            lines.append(f"**{top.get('name')}** is {top.get('status')}: {top.get('n_recent')} calls in the last four "
                         f"weeks against {top.get('expected_recent')} expected, first seen "
                         f"{top.get('first_seen_week')} [{cid}].")
            for r in rows[1:4]:
                lines.append(f"- {r.get('name')}: {r.get('status')}, {r.get('n_recent')} recent vs "
                             f"{r.get('expected_recent')} expected.")
            if data.get("expected_false_positives") is not None:
                caveats.append(f"About {data['expected_false_positives']} of {data.get('n_tested', '?')} themes tested "
                               f"could pass this threshold by chance.")
            quotes = _quotes_for(ctx, con, "theme", str(top.get("theme_id")), filters, results, events, 2)
            charts.append(Chart(kind="bars", title="Emerging themes", result_id=env["result_id"], series_key="n_recent"))
        else:
            caveats.append("No theme passed the emerging threshold at this as-of week.")

    elif kind == "same_problem":
        env = _call(ctx, con, "list_themes", {"filters": fdump, "sort_by": "n_wordings", "polarity": "negative",
                                              "driver_category": None, "limit": 5}, results, events)
        rows = (env or {}).get("rows", [])
        if rows:
            top = rows[0]
            det = _call(ctx, con, "theme_detail", {"theme_id": top["theme_id"], "filters": fdump,
                                                   "as_of_week": as_of_week}, results, events)
            cid = add_claim(f"{top.get('name')} is described in {top.get('n_wordings')} distinct wordings across "
                            f"{top.get('n_products')} products by {top.get('n_calls')} customers.",
                            det or env, rows, True, int(top.get("n_calls", 0)), theme_ids=[top["theme_id"]])
            lines.append(f"Yes. **{top.get('name')}** is one problem stated in {top.get('n_wordings')} different "
                         f"wordings by {top.get('n_calls')} customers across {top.get('n_products')} products [{cid}].")
            for w in ((det or {}).get("data", {}).get("wordings") or [])[:4]:
                lines.append(f"- \"{w.get('issue_statement', '')[:140]}\"")
            quotes = _quotes_for(ctx, con, "theme", top["theme_id"], filters, results, events, 2)

    elif kind == "segments":
        env = _call(ctx, con, "breakdown", {"entity_type": "all", "entity_id": None, "by": "product",
                                            "filters": fdump, "min_n": 5}, results, events)
        rows = [r for r in (env or {}).get("rows", []) if not r.get("suppressed")]
        if rows:
            top = max(rows, key=lambda r: r.get("n_calls", 0))
            cid = add_claim(f"{top.get('value')} accounts for {top.get('n_calls')} calls "
                            f"({_pct(top.get('share', 0) * 100 if top.get('share', 0) <= 1 else top.get('share'))}).",
                            env, rows, True, int(top.get("n_calls", 0)))
            lines.append(f"By product, **{top.get('value')}** carries the most contacts "
                         f"({top.get('n_calls')} calls) [{cid}].")
            for r in sorted(rows, key=lambda r: -r.get("n_calls", 0))[1:5]:
                lines.append(f"- {r.get('value')}: {r.get('n_calls')} calls, lift {r.get('lift')}.")
            charts.append(Chart(kind="bars", title="By product", result_id=env["result_id"], series_key="n_calls"))
            caveats.append("Rows below minimum support are not ranked.")

    else:  # evidence / quotes
        env = _call(ctx, con, "list_themes", {"filters": fdump, "sort_by": "neg_mass", "polarity": "negative",
                                              "driver_category": None, "limit": 3}, results, events)
        rows = (env or {}).get("rows", [])
        if rows:
            top = rows[0]
            cid = add_claim(f"{top.get('name')} rests on {top.get('n_calls')} calls.", env, rows, True,
                            int(top.get("n_calls", 0)), theme_ids=[top["theme_id"]])
            lines.append(f"**{top.get('name')}** rests on {top.get('n_calls')} calls; here is what those customers "
                         f"said [{cid}].")
            quotes = _quotes_for(ctx, con, "theme", top["theme_id"], filters, results, events, 4)

    if not claims:
        lines.append("No result in this scope carried enough calls to state a finding.")
        caveats.append("Nothing met the minimum support of 5 calls.")
    events.append({"name": "status", "payload": {"text": "templated answer assembled"}, "t_ms": len(events) * 700})
    answer = Answer(answer_markdown="\n\n".join(lines) if lines else "No finding available in this scope.",
                    claims=claims or [Claim(id="c1", statement="No finding available in this scope.", headline=True)],
                    quotes=quotes, charts=charts, caveats=caveats,
                    followups=["Which calls support this?", "How does this differ by product?",
                               "Is anything new in the last four weeks?"])
    return answer, results, events
