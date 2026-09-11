"""The agent's read-only tool surface: strict schemas, one envelope per result, every result persisted
with its SQL and full call-id list so the server can recount any claim later."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from voc.schemas.answer import ANSWER_API_SCHEMA
from voc.schemas.filters import FILTERS_API_SCHEMA, Filters
from voc.store import queries as Q
from voc.store.db import get_meta
from voc.taxonomy import loader as tx

MAX_CALL_IDS_SHOWN = 50


# --- schema helpers -----------------------------------------------------------------------

def _obj(props: dict[str, Any]) -> dict[str, Any]:
    """Strict object schema: every property required (nullable ones carry a null type)."""
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


_STR = {"type": "string"}
_INT = {"type": "integer"}
_BOOL = {"type": "boolean"}
_FILTERS = FILTERS_API_SCHEMA


def _enum(values: list[str], nullable: bool = False) -> dict[str, Any]:
    if nullable:
        return {"type": ["string", "null"], "enum": [*values, None]}
    return {"type": "string", "enum": values}


def _nullable(kind: str) -> dict[str, Any]:
    return {"type": [kind, "null"]}


ENTITY_TYPES = list(Q.ENTITY_TYPES)
SORT_BY = ["n_calls", "neg_mass", "pos_mass", "emerging_score", "n_wordings"]
POLARITY = ["negative", "positive", "any"]


TOOL_SPECS: list[dict[str, Any]] = [
    {
        "name": "get_overview",
        "description": ("Totals, calls per month, the top contact reasons with their change versus the previous "
                        "equal period, the top themes, and the sentiment, resolution and customer-ask splits. "
                        "Call this first for any broad question about what customers contact us about or what is changing."),
        "strict": True,
        "input_schema": _obj({"filters": _FILTERS}),
    },
    {
        "name": "contact_reasons",
        "description": ("Contact reasons ranked with counts, shares, change versus the previous period, direction, "
                        "and the most common specific reasons in the customers' own words under each label. "
                        "Call this when the question is about why customers are contacting us or what is rising or falling."),
        "strict": True,
        "input_schema": _obj({"filters": _FILTERS, "compare_with_previous": _BOOL}),
    },
    {
        "name": "list_themes",
        "description": ("Themes ranked by calls, negative mass, positive mass, emerging score or number of distinct "
                        "wordings. Call this to find the biggest problems (sort_by=neg_mass), what goes right "
                        "(polarity=positive, sort_by=pos_mass), or problems described in many different ways "
                        "(sort_by=n_wordings)."),
        "strict": True,
        "input_schema": _obj({"filters": _FILTERS, "sort_by": _enum(SORT_BY), "polarity": _enum(POLARITY),
                              "driver_category": _enum(tx.codes("driver_categories"), nullable=True),
                              "limit": _INT}),
    },
    {
        "name": "theme_detail",
        "description": ("One theme in depth: definition, root cause, the distinct wordings customers use, the top "
                        "specific drivers, breakdowns by product and segment, the weekly series, and merge history. "
                        "Call this when you need the evidence behind a theme or to show that one problem is described "
                        "in different words."),
        "strict": True,
        "input_schema": _obj({"theme_id": _STR, "filters": _FILTERS, "as_of_week": _nullable("string")}),
    },
    {
        "name": "theme_trend",
        "description": ("Weekly or monthly series for up to six themes or contact reasons, with the direction and the "
                        "change in share points. Call this to show how something moved over time."),
        "strict": True,
        "input_schema": _obj({"entity_ids": {"type": "array", "items": _STR}, "grain": _enum(["week", "month"]),
                              "filters": _FILTERS}),
    },
    {
        "name": "emerging_themes",
        "description": ("Themes that are new, emerging, growing or fading at the as-of week, with the recent count "
                        "versus the expected count, the z score, the weeks involved, when it was first seen, whether "
                        "it is robust at eight weeks, and how many themes could pass by chance. Call this for any "
                        "question about what is growing fastest or whether anything is new."),
        "strict": True,
        "input_schema": _obj({"as_of_week": _nullable("string"), "min_recent": _INT, "only_new": _BOOL,
                              "filters": _FILTERS, "limit": _INT}),
    },
    {
        "name": "sentiment_drivers",
        "description": ("What drives negative or positive sentiment, grouped by theme, driver category or contact "
                        "reason, with the specific triggers in the customers' words and two verified quotes each. "
                        "Call this for the causes of dissatisfaction or for what customers are happy about."),
        "strict": True,
        "input_schema": _obj({"polarity": _enum(["negative", "positive"]),
                              "group_by": _enum(["theme", "driver_category", "reason"]),
                              "filters": _FILTERS, "limit": _INT}),
    },
    {
        "name": "breakdown",
        "description": ("How one entity (or all calls) differs by product, channel, region group, region, segment or "
                        "month, with counts, shares, lift versus the overall rate and minimum-support suppression. "
                        "Call this for questions about how pain points differ between groups."),
        "strict": True,
        "input_schema": _obj({"entity_type": _enum([*ENTITY_TYPES, "all"]), "entity_id": _nullable("string"),
                              "by": _enum(list(Q.BREAKDOWN_DIMS)), "filters": _FILTERS, "min_n": _INT}),
    },
    {
        "name": "compare",
        "description": ("Two filtered scopes side by side (two periods, two products, two segments): the themes and "
                        "reasons whose share differs most, with both counts and both shares. Call this for explicit "
                        "comparisons."),
        "strict": True,
        "input_schema": _obj({"filters_a": _FILTERS, "filters_b": _FILTERS, "label_a": _STR, "label_b": _STR,
                              "limit": _INT}),
    },
    {
        "name": "get_quotes",
        "description": ("Verified verbatim customer statements for a theme, contact reason, driver category or a list "
                        "of call ids, spread over months and products. Call this whenever the answer should carry the "
                        "customers' own words. Only quotes returned here may be quoted."),
        "strict": True,
        "input_schema": _obj({"entity_type": _enum([*ENTITY_TYPES, "call_list"]), "entity_id": _nullable("string"),
                              "call_ids": {"type": ["array", "null"], "items": _STR}, "filters": _FILTERS,
                              "n": _INT, "polarity": _enum(POLARITY), "diverse": _BOOL}),
    },
    {
        "name": "search_calls",
        "description": ("Full-text search over the contact texts and the extracted issue statements. Call this when "
                        "the wording you are looking for may not be a theme name, or to check whether customers use a "
                        "particular word."),
        "strict": True,
        "input_schema": _obj({"query": _STR, "filters": _FILTERS, "limit": _INT}),
    },
    {
        "name": "get_call",
        "description": ("One contact in full: the customer's text, the metadata, everything extracted from it "
                        "(reasons, products, topics with sentiment and drivers, evidence offsets, positive moments) "
                        "and its themes. Call this to check a single example before citing it."),
        "strict": True,
        "input_schema": _obj({"call_id": _STR}),
    },
    {
        "name": "submit_answer",
        "description": ("Submit the final answer. Call this ALONE in its own turn once you have the data. Every claim "
                        "must cite the result_ids it rests on and the call ids behind it; the server recounts them."),
        "strict": True,
        "input_schema": ANSWER_API_SCHEMA,
    },
]

TOOL_NAMES = [t["name"] for t in TOOL_SPECS]
READ_TOOLS = [t["name"] for t in TOOL_SPECS if t["name"] != "submit_answer"]


@dataclass
class ToolContext:
    con: sqlite3.Connection
    qhash: str = ""
    as_of_week: str | None = None
    counter: int = 0
    results: dict[str, dict[str, Any]] = field(default_factory=dict)

    def next_id(self) -> str:
        self.counter += 1
        return f"r{self.counter}"


def _filters(args: dict[str, Any]) -> Filters:
    return Filters.from_any(args.get("filters"))


def _int(args: dict[str, Any], key: str, default: int, lo: int = 1, hi: int = 100) -> int:
    value = args.get(key)
    if value is None:
        return default
    return max(lo, min(hi, int(value)))


# --- dispatch -----------------------------------------------------------------------------

def _get_overview(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.get_overview(con, _filters(args), ctx.as_of_week)


def _contact_reasons(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.contact_reasons(con, _filters(args), bool(args.get("compare_with_previous", True)))


def _list_themes(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.list_themes(con, _filters(args), args.get("sort_by") or "n_calls", args.get("polarity") or "any",
                         args.get("driver_category"), _int(args, "limit", 10, 1, 25), ctx.as_of_week)


def _theme_detail(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.theme_detail(con, str(args["theme_id"]), _filters(args), args.get("as_of_week") or ctx.as_of_week)


def _theme_trend(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    ids = [str(x) for x in (args.get("entity_ids") or [])][:6]
    if not ids:
        raise Q.QueryError("entity_ids must contain at least one theme id or reason code")
    return Q.theme_trend(con, ids, args.get("grain") or "month", _filters(args))


def _emerging(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.emerging_themes(con, args.get("as_of_week") or ctx.as_of_week, _filters(args),
                             _int(args, "min_recent", Q.MIN_SUPPORT, 1, 50), bool(args.get("only_new")),
                             _int(args, "limit", 10, 1, 25))


def _drivers(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.sentiment_drivers(con, args.get("polarity") or "negative", args.get("group_by") or "theme",
                               _filters(args), _int(args, "limit", 10, 1, 25))


def _breakdown(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.breakdown(con, args.get("entity_type") or "all", args.get("entity_id"), args.get("by") or "product",
                       _filters(args), _int(args, "min_n", Q.MIN_SUPPORT, 1, 100))


def _compare(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.compare(con, Filters.from_any(args.get("filters_a")), Filters.from_any(args.get("filters_b")),
                     str(args.get("label_a") or "A"), str(args.get("label_b") or "B"), _int(args, "limit", 8, 1, 20))


def _quotes(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    call_ids = [str(x) for x in (args.get("call_ids") or [])] or None
    return Q.get_quotes(con, args.get("entity_type") or "theme", args.get("entity_id"), call_ids, _filters(args),
                        _int(args, "n", 5, 1, 10), args.get("polarity") or "any",
                        True if args.get("diverse") is None else bool(args["diverse"]))


def _search(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.search_calls(con, str(args.get("query") or ""), _filters(args), _int(args, "limit", 10, 1, 20))


def _get_call(args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    return Q.get_call(con, str(args["call_id"]))


DISPATCH: dict[str, Callable[[dict[str, Any], sqlite3.Connection, ToolContext], dict[str, Any]]] = {
    "get_overview": _get_overview, "contact_reasons": _contact_reasons, "list_themes": _list_themes,
    "theme_detail": _theme_detail, "theme_trend": _theme_trend, "emerging_themes": _emerging,
    "sentiment_drivers": _drivers, "breakdown": _breakdown, "compare": _compare, "get_quotes": _quotes,
    "search_calls": _search, "get_call": _get_call,
}


def persist_result(con: sqlite3.Connection, qhash: str, result_id: str, tool: str, args: dict[str, Any],
                   sql: list[dict[str, Any]], call_ids: list[str]) -> None:
    """Store the SQL and the full call-id list so a claim can be recounted and its rows re-listed."""
    try:
        con.execute(
            "INSERT INTO tool_results(result_id, qhash, tool, args, sql, call_ids, created_at) VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(qhash, result_id) DO UPDATE SET tool=excluded.tool, args=excluded.args, "
            "sql=excluded.sql, call_ids=excluded.call_ids, created_at=excluded.created_at",
            (result_id, qhash, tool, json.dumps(args, ensure_ascii=False, default=str),
             json.dumps(sql, ensure_ascii=False, default=str), json.dumps(call_ids),
             datetime.now(timezone.utc).isoformat(timespec="seconds")))
        con.commit()
    except sqlite3.Error:
        pass  # a read-only index still answers questions; persistence is best effort


def summarize(tool: str, payload: dict[str, Any], scope: dict[str, Any]) -> str:
    """One line the model and the trace timeline can read without parsing the rows."""
    rows = payload.get("rows") or []
    data = payload.get("data") or {}
    n_scope = scope.get("n_calls_in_scope", 0)
    if tool == "get_overview":
        t = data.get("totals", {})
        top = ", ".join(f"{r.get('label') or r.get('reason')} {r.get('n_calls')}" for r in (data.get("top_reasons") or [])[:3])
        return f"{t.get('n_calls', 0)} calls, {t.get('n_topics', 0)} topics, {t.get('n_active_themes', 0)} themes; top reasons: {top}"
    if tool in ("contact_reasons", "list_themes", "sentiment_drivers", "emerging_themes", "breakdown", "compare"):
        head = ", ".join(str(r.get("name") or r.get("label") or r.get("reason") or r.get("value") or r.get("key"))
                         + f" ({r.get('n_calls', r.get('n_a', 0))})" for r in rows[:3])
        return f"{len(rows)} rows over {n_scope} calls in scope" + (f"; {head}" if head else "")
    if tool == "theme_detail":
        d = data or {}
        return (f"{d.get('name', payload.get('data', {}).get('theme_id', ''))}: {d.get('n_calls', 0)} calls, "
                f"{d.get('n_wordings', 0)} wordings, {d.get('n_products', 0)} products")
    if tool == "theme_trend":
        return f"{len(rows)} series over {n_scope} calls in scope"
    if tool == "get_quotes":
        return f"{len(rows)} verified quotes"
    if tool == "search_calls":
        return f"{len(rows)} matching calls of {n_scope} in scope"
    if tool == "get_call":
        return f"call {data.get('call_id', '')} ({data.get('date', '')}, {data.get('product', '')})"
    return f"{len(rows)} rows"


def run_tool(name: str, args: dict[str, Any], con: sqlite3.Connection, ctx: ToolContext) -> dict[str, Any]:
    """Execute one read tool and wrap it in the envelope the agent and the UI both consume."""
    if name == "submit_answer":
        raise Q.QueryError("submit_answer is terminal and is handled by the runner")
    fn = DISPATCH.get(name)
    if fn is None:
        raise Q.QueryError(f"unknown tool {name}; available: {', '.join(READ_TOOLS)}")
    payload = fn(args or {}, con, ctx)
    call_ids = [str(x) for x in (payload.pop("call_ids", None) or [])]
    sql = payload.pop("sql", [])
    sc = payload.pop("scope", None) or {"n_calls_in_scope": len(call_ids)}
    sc = dict(sc)
    sc.setdefault("as_of_week", ctx.as_of_week)
    result_id = ctx.next_id()
    envelope = {
        "result_id": result_id, "tool": name, "args": args or {}, "scope": sc,
        "summary": summarize(name, payload, sc),
        "rows": payload.get("rows", []), "data": payload.get("data", {}),
        "call_ids": call_ids[:MAX_CALL_IDS_SHOWN], "n_call_ids": len(call_ids), "sql": sql,
        "data_version": get_meta(con, "data_version", "") or "",
    }
    persist_result(con, ctx.qhash, result_id, name, args or {}, sql, call_ids)
    ctx.results[result_id] = {**envelope, "call_ids_full": call_ids}
    return envelope
