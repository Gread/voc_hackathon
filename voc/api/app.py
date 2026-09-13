"""FastAPI app: the dashboard endpoints (the same functions the agent calls), the ask stream, and the UI."""
from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from voc.config import get_settings
from voc.paths import get_paths
from voc.questions import load_questions
from voc.schemas.filters import DIMENSIONS, Filters
from voc.store import queries as Q
from voc.store.db import connect, db_is_stale, get_meta

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


class NoCacheStatic(StaticFiles):
    """Browsers cache ES modules hard, which makes an edited .js file look unchanged after a refresh.
    There is no build step here, so ask for revalidation on every request instead."""

    def file_response(self, *args: Any, **kwargs: Any) -> Any:
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        return response


# What each corpus is, in the interface's own words. Two corpora that differ in kind must not be
# blended silently: a reader has to know which one a number came from.
SOURCE_LABELS = {
    "cfpb": {"label": "Written complaints", "kind": "real",
             "note": "Real complaints to the US regulator about one bank, 24 months."},
    "talkmap": {"label": "Call transcripts", "kind": "synthetic",
                "note": "Synthetic agent/customer conversations, one month, no trend history."},
}


def _filters_from_request(request: Request) -> Filters:
    params: dict[str, Any] = {}
    for dim in DIMENSIONS:
        values = request.query_params.getlist(dim)
        if values:
            params[dim] = values
    for key in ("date_from", "date_to"):
        if request.query_params.get(key):
            params[key] = request.query_params[key]
    return Filters.from_query(params)


def _as_of(request: Request) -> str | None:
    return request.query_params.get("as_of") or None


def create_app(data_dir: Path | None = None) -> FastAPI:
    paths = get_paths(data_dir)
    settings = get_settings()
    app = FastAPI(title="Voice of the Customer Insights", version="0.1.0",
                  description="Agents read every contact; the server verifies every number.")
    state: dict[str, Any] = {"error": None}
    # One connection per worker thread. FastAPI runs sync endpoints in a threadpool and the
    # dashboard opens several panels at once; sharing one connection interleaves cursors.
    local = threading.local()

    def db() -> sqlite3.Connection:
        con = getattr(local, "con", None)
        if con is None:
            if not paths.sqlite.exists():
                raise HTTPException(503, "no index yet: run `voc build-db`")
            con = local.con = connect(paths.sqlite)
        return con

    def envelope(payload: dict[str, Any], con: sqlite3.Connection) -> JSONResponse:
        payload.setdefault("data_version", get_meta(con, "data_version", "") or "")
        payload.setdefault("as_of_week", get_meta(con, "as_of_week", "") or "")
        return JSONResponse(json.loads(json.dumps(payload, default=str)))

    def wrap(con: sqlite3.Connection, tool: str, result: dict[str, Any]) -> JSONResponse:
        """Persist the tool result so its numbers stay clickable, then return the envelope."""
        from voc.agent.tools import ToolContext, persist_result, summarize

        ctx = ToolContext(con=con, qhash="api", as_of_week=get_meta(con, "as_of_week"))
        call_ids = [str(x) for x in (result.pop("call_ids", None) or [])]
        sql = result.pop("sql", [])
        sc = dict(result.pop("scope", None) or {"n_calls_in_scope": len(call_ids)})
        sc.setdefault("as_of_week", ctx.as_of_week)
        rid = f"api_{abs(hash((tool, json.dumps(sc, sort_keys=True, default=str), len(call_ids)))) % (10 ** 10)}"
        persist_result(con, "api", rid, tool, {}, sql, call_ids)
        return envelope({"result_id": rid, "tool": tool, "scope": sc, "summary": summarize(tool, result, sc),
                         "rows": result.get("rows", []), "data": result.get("data", {}),
                         "call_ids": call_ids[:50], "n_call_ids": len(call_ids), "sql": sql}, con)

    @app.exception_handler(Q.NotFound)
    def _not_found(_request: Request, exc: Q.NotFound) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=404)

    @app.exception_handler(Q.QueryError)
    def _bad_query(_request: Request, exc: Q.QueryError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=400)

    def _rebuild_if_stale() -> None:
        if paths.calls.exists() and db_is_stale(paths):
            try:
                from voc.store.build import build
                build(paths, quiet=True)
            except Exception as exc:  # a stale index is better than no server
                state["error"] = f"automatic rebuild failed: {exc}"

    _rebuild_if_stale()

    @app.get("/api/meta")
    def meta() -> JSONResponse:
        con = db()
        rows = {r["key"]: r["value"] for r in con.execute("SELECT key, value FROM meta")}
        profile: dict[str, Any] = {}
        if paths.profile.exists():
            try:
                profile = json.loads(paths.profile.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                profile = {}
        weeks = [r["as_of_week"] for r in con.execute(
            "SELECT DISTINCT as_of_week FROM emerging_scores ORDER BY as_of_week")]
        sources = [dict(r) for r in con.execute(
            "SELECT c.source, COUNT(*) AS n_calls, MIN(c.date) AS date_from, MAX(c.date) AS date_to, "
            "       COUNT(DISTINCT c.shape) AS n_shapes, MIN(c.shape) AS shape "
            "FROM calls c GROUP BY c.source ORDER BY n_calls DESC")]
        for row in sources:
            row.update(SOURCE_LABELS.get(row["source"], {"label": row["source"], "kind": "unknown",
                                                         "note": ""}))

        def _num(key: str) -> Any:
            v = rows.get(key)
            try:
                return json.loads(v) if v is not None else None
            except (TypeError, json.JSONDecodeError):
                return v

        return envelope({
            "data_version": rows.get("data_version", ""), "as_of_week": rows.get("as_of_week", ""),
            "llm_mode": rows.get("llm_mode", settings.llm_mode), "built_at": rows.get("built_at"),
            "counts": {k: _num(k) for k in ("n_calls", "n_extracted", "n_topics", "n_themes") if k in rows},
            "qa": {k[3:]: _num(k) for k in rows if k.startswith("qa_")},
            "provenance": {
                "source": profile.get("source", "cfpb_api"),
                "company": profile.get("company", settings.company),
                "window": profile.get("window", {}),
                "sampling_fraction": profile.get("sampling_fraction"),
                "seed": profile.get("seed"),
                "n_raw": profile.get("n_raw"), "n_eligible": profile.get("n_eligible"),
                "note": ("Real public complaint narratives from the US CFPB Consumer Complaint Database. "
                         "Redactions such as XXXX are the regulator's. Dates are when the regulator received "
                         "the complaint. The corpus is complaints, so satisfaction findings are positive "
                         "moments inside complaints."),
            },
            "questions": load_questions(),
            "sources": sources,
            "as_of_weeks": weeks,
            "live_model": settings.ask_model if settings.can_call_api else None,
            "warning": state["error"],
        }, con)

    @app.get("/api/overview")
    def overview(request: Request) -> JSONResponse:
        con = db()
        return wrap(con, "get_overview", Q.get_overview(con, _filters_from_request(request), _as_of(request)))

    @app.get("/api/reasons")
    def reasons(request: Request, compare: int = 1) -> JSONResponse:
        con = db()
        return wrap(con, "contact_reasons", Q.contact_reasons(con, _filters_from_request(request), bool(compare)))

    @app.get("/api/themes")
    def themes(request: Request, sort_by: str = "n_calls", polarity: str = "any",
               driver_category: str | None = None, limit: int = 10) -> JSONResponse:
        con = db()
        return wrap(con, "list_themes", Q.list_themes(con, _filters_from_request(request), sort_by, polarity,
                                                      driver_category, min(25, max(1, limit)), _as_of(request)))

    @app.get("/api/themes/{theme_id}")
    def theme(theme_id: str, request: Request) -> JSONResponse:
        con = db()
        try:
            return wrap(con, "theme_detail", Q.theme_detail(con, theme_id, _filters_from_request(request), _as_of(request)))
        except Q.NotFound as exc:
            raise HTTPException(404, str(exc)) from exc

    @app.get("/api/trend")
    def trend(request: Request, ids: str = "", grain: str = "month") -> JSONResponse:
        con = db()
        entity_ids = [x for x in ids.split(",") if x][:6]
        if not entity_ids:
            raise HTTPException(400, "ids is required (comma-separated theme ids or reason codes)")
        return wrap(con, "theme_trend", Q.theme_trend(con, entity_ids, grain, _filters_from_request(request)))

    @app.get("/api/emerging")
    def emerging(request: Request, min_recent: int = Q.MIN_SUPPORT, only_new: int = 0, limit: int = 10) -> JSONResponse:
        con = db()
        return wrap(con, "emerging_themes", Q.emerging_themes(con, _as_of(request), _filters_from_request(request),
                                                              min_recent, bool(only_new), min(25, max(1, limit))))

    @app.get("/api/drivers")
    def drivers(request: Request, polarity: str = "negative", group_by: str = "theme", limit: int = 10) -> JSONResponse:
        con = db()
        return wrap(con, "sentiment_drivers", Q.sentiment_drivers(con, polarity, group_by,
                                                                  _filters_from_request(request), min(25, max(1, limit))))

    @app.get("/api/breakdown")
    def breakdown(request: Request, entity_type: str = "all", entity_id: str | None = None,
                  by: str = "product", min_n: int = Q.MIN_SUPPORT) -> JSONResponse:
        con = db()
        return wrap(con, "breakdown", Q.breakdown(con, entity_type, entity_id, by,
                                                  _filters_from_request(request), min_n))

    @app.get("/api/compare")
    def compare(a: str = "{}", b: str = "{}", label_a: str = "A", label_b: str = "B", limit: int = 8) -> JSONResponse:
        con = db()
        try:
            fa, fb = Filters.from_any(json.loads(a)), Filters.from_any(json.loads(b))
        except json.JSONDecodeError as exc:
            raise HTTPException(400, f"a and b must be JSON filter objects: {exc}") from exc
        return wrap(con, "compare", Q.compare(con, fa, fb, label_a, label_b, limit))

    @app.get("/api/quotes")
    def quotes(request: Request, entity_type: str = "theme", entity_id: str | None = None,
               n: int = 5, polarity: str = "any", diverse: int = 1) -> JSONResponse:
        con = db()
        return wrap(con, "get_quotes", Q.get_quotes(con, entity_type, entity_id, None,
                                                    _filters_from_request(request), min(10, max(1, n)),
                                                    polarity, bool(diverse)))

    @app.get("/api/search")
    def search(request: Request, q: str = "", limit: int = 10) -> JSONResponse:
        con = db()
        if not q.strip():
            raise HTTPException(400, "q is required")
        return wrap(con, "search_calls", Q.search_calls(con, q, _filters_from_request(request), min(20, max(1, limit))))

    @app.get("/api/calls/{call_id}")
    def call(call_id: str) -> JSONResponse:
        con = db()
        try:
            return wrap(con, "get_call", Q.get_call(con, call_id))
        except Q.NotFound as exc:
            raise HTTPException(404, str(exc)) from exc

    @app.get("/api/results/{result_id}/rows")
    def result_rows(result_id: str, qhash: str | None = None) -> JSONResponse:
        con = db()
        # Result ids restart at r1 for every question, so the asking question decides which row
        # this is; without one, fall back to the most recently stored.
        row = None
        if qhash:
            row = con.execute("SELECT tool, args, sql, call_ids FROM tool_results WHERE result_id = ? AND qhash = ?",
                              (result_id, qhash)).fetchone()
        if row is None:
            row = con.execute("SELECT tool, args, sql, call_ids FROM tool_results WHERE result_id = ? "
                              "ORDER BY created_at DESC LIMIT 1", (result_id,)).fetchone()
        if row is None:
            raise HTTPException(404, f"unknown result {result_id}")
        stored_ids = json.loads(row["call_ids"] or "[]")
        statements = json.loads(row["sql"] or "[]")
        rerun = Q.rerun_call_ids(con, statements)
        ids = rerun or stored_ids
        # A result restored from a recorded answer's trace keeps the query, not the id list, so
        # there is nothing to compare against and nothing has drifted.
        matches = None if not stored_ids else sorted(ids) == sorted(stored_ids)
        return envelope({"result_id": result_id, "tool": row["tool"], "n_call_ids": len(ids),
                         "reran": bool(rerun), "matches_stored": matches,
                         "sql": statements, "rows": Q.call_list(con, ids[:200])}, con)

    @app.get("/api/questions")
    def questions() -> JSONResponse:
        from voc.agent import cache as cache_mod

        con = db()
        dv = get_meta(con, "data_version", "") or ""
        return envelope({"questions": load_questions(), "recorded": cache_mod.list_questions(con, dv)}, con)

    @app.get("/api/answers/{qhash}")
    def answer(qhash: str) -> JSONResponse:
        from voc.agent import cache as cache_mod

        con = db()
        stored = cache_mod.load_answer(con, qhash)
        if stored is None:
            raise HTTPException(404, f"no stored answer {qhash}")
        return envelope(stored.to_dict(), con)

    @app.post("/api/ask")
    async def ask(request: Request) -> StreamingResponse:
        con = db()
        body = await request.json()
        question = str(body.get("question") or "").strip()
        if not question:
            raise HTTPException(400, "question is required")
        filters = Filters.from_any(body.get("filters"))
        as_of = body.get("as_of")
        fresh = bool(body.get("fresh"))

        async def stream():
            try:
                from voc.agent.service import stream_answer
            except ImportError as exc:
                from voc.api.sse import encode_event
                yield encode_event("status", {"text": f"agent not available: {exc}"})
                yield encode_event("error", {"message": "the ask service is not installed"})
                yield encode_event("done", {})
                return
            async for chunk in stream_answer(question, filters, con, as_of=as_of, fresh=fresh):
                yield chunk

        return StreamingResponse(stream(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    if WEB_DIR.exists():
        app.mount("/static", NoCacheStatic(directory=WEB_DIR), name="static")

        @app.get("/")
        def index() -> FileResponse:
            page = WEB_DIR / "index.html"
            if not page.exists():
                raise HTTPException(404, "UI not built")
            return FileResponse(page)

    return app


app = None  # created by voc.api.cli; `uvicorn voc.api.app:build` also works


def build() -> FastAPI:
    return create_app()
