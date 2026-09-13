"""`voc serve`: run the dashboard and the ask API."""
from __future__ import annotations

import argparse
import sys
from typing import Any

from voc.config import get_settings
from voc.paths import get_paths
from voc.store.db import connect, db_is_stale, get_meta


def add_parser(subparsers: Any) -> None:
    p = subparsers.add_parser("serve", help="Serve the dashboard and the ask API")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=None)
    p.add_argument("--reload", action="store_true")
    p.set_defaults(func=run)


def describe_mode() -> str:
    settings = get_settings()
    paths = get_paths()
    if not paths.sqlite.exists():
        return "no index yet (run `voc ingest` -> `voc extract` -> `voc theme run` -> `voc build-db`)"
    con = connect(paths.sqlite, readonly=True)
    llm_mode = get_meta(con, "llm_mode", "") or ""
    n_calls = get_meta(con, "n_calls", "?")
    version = get_meta(con, "data_version", "")
    con.close()
    if llm_mode == "fake":
        return f"FAKE DATA ({n_calls} calls) - heuristic extractions, not model output"
    if settings.can_call_api:
        return f"live · {settings.live_ask_model} · {n_calls} calls · data {version}"
    return f"recorded answers · {n_calls} calls · data {version} (no API key: new questions get a templated answer)"


def run(args: argparse.Namespace) -> int:
    import uvicorn

    from voc.api.app import create_app

    settings = get_settings()
    paths = get_paths()
    if paths.calls.exists() and db_is_stale(paths):
        print("index is stale; rebuilding...")
        try:
            from voc.store.build import build
            build(paths, quiet=True)
        except Exception as exc:
            print(f"rebuild failed: {exc}", file=sys.stderr)
    port = args.port or settings.port
    print(f"mode: {describe_mode()}")
    print(f"open http://{args.host}:{port}/  (API docs at /docs)")
    uvicorn.run(create_app(), host=args.host, port=port, log_level="warning")
    return 0
