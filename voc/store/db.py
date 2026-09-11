"""SQLite connection, schema rendering and data_version helpers shared by build, queries and the API."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from voc.paths import Paths, get_paths
from voc.taxonomy import loader as tx

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
ENUM_PLACEHOLDERS = ["shape", "products", "region_group", "channel", "segment",
                     "contact_reasons", "services", "driver_categories", "polarity"]


def render_schema() -> str:
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    for kind in ENUM_PLACEHOLDERS:
        sql = sql.replace("{{" + kind + "}}", tx.sql_enum(kind))
    if "{{" in sql:
        raise RuntimeError("unrendered placeholder in schema.sql")
    return sql


def connect(path: Path | None = None, readonly: bool = False) -> sqlite3.Connection:
    """Open the index (WAL, foreign keys on, Row factory). In-memory when path is ':memory:'."""
    p = str(path or get_paths().sqlite)
    if readonly and p != ":memory:":
        con = sqlite3.connect(f"file:{p}?mode=ro", uri=True, check_same_thread=False)
    else:
        if p != ":memory:":
            Path(p).parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(p, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    if p != ":memory:" and not readonly:
        con.execute("PRAGMA journal_mode = WAL")
    return con


def create_schema(con: sqlite3.Connection) -> None:
    con.executescript(render_schema())


def file_sha(path: Path) -> str:
    """Content hash, ignoring line endings.

    This feeds the data version, which keys every recorded answer. Hashing raw bytes made the
    version depend on how git checked the file out, so a clone on another machine computed a
    different version and found none of the recorded answers."""
    if not path.exists():
        return ""
    h = hashlib.sha256()
    held_cr = False
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            if held_cr:
                chunk = b"\r" + chunk
            held_cr = chunk.endswith(b"\r")   # a CR on a chunk boundary may still start a CRLF
            if held_cr:
                chunk = chunk[:-1]
            h.update(chunk.replace(b"\r\n", b"\n"))
    if held_cr:
        h.update(b"\r")
    return h.hexdigest()


def compute_data_version(paths: Paths | None = None) -> str:
    """Hash of every committed input file plus the taxonomy version. Prompt versions are inside the files."""
    paths = paths or get_paths()
    parts = [file_sha(paths.calls), file_sha(paths.extractions), file_sha(paths.registry),
             file_sha(paths.members), file_sha(paths.merges), tx.version()]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def get_meta(con: sqlite3.Connection, key: str, default: Any = None) -> Any:
    row = con.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return default if row is None else row["value"]


def set_meta(con: sqlite3.Connection, key: str, value: Any) -> None:
    if not isinstance(value, str):
        value = json.dumps(value)
    con.execute("INSERT INTO meta(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value))


def db_exists(paths: Paths | None = None) -> bool:
    return (paths or get_paths()).sqlite.exists()


def db_is_stale(paths: Paths | None = None) -> bool:
    """True when the index is missing or was built from different input files."""
    paths = paths or get_paths()
    if not paths.sqlite.exists():
        return True
    try:
        con = connect(paths.sqlite, readonly=True)
        try:
            return get_meta(con, "data_version") != compute_data_version(paths)
        finally:
            con.close()
    except sqlite3.Error:
        return True
