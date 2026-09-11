"""Answer cache: question hashes, file + table persistence, near-match routing and replay pacing.
Files under data/answers/ are the truth; the answers_cache table is a rebuildable index."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from voc.paths import get_paths
from voc.schemas.answer import ASK_PROMPT_VERSION
from voc.schemas.filters import Filters

STOPWORDS = {"the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "is", "are", "what", "which", "how",
             "do", "does", "we", "us", "our", "about", "with", "by", "it", "them", "they", "any", "most", "there",
             "this", "that", "be", "customers", "customer", "calls", "call", "did", "actual", "specific", "specifically"}
REPLAY_SPEED = 0.5
REPLAY_CAP_MS = 400


def normalise_question(q: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", q.lower())).strip()


def content_tokens(q: str) -> set[str]:
    return {t for t in normalise_question(q).split() if t not in STOPWORDS and len(t) > 2}


def qhash(question: str, filters: Filters, as_of_week: str, data_version: str) -> str:
    raw = "|".join([normalise_question(question), filters.canonical_json(), as_of_week, data_version, ASK_PROMPT_VERSION])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


@dataclass
class StoredAnswer:
    qhash: str
    question: str
    filters: dict[str, Any]
    as_of_week: str
    data_version: str
    prompt_version: str
    mode: str                     # live | recorded | templated
    model: str
    effort: str
    answer: dict[str, Any]        # VerifiedAnswer as dict
    trace: list[dict[str, Any]]   # [{name, payload, t_ms}]
    validation: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    usage: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "StoredAnswer":
        known = {k: d.get(k) for k in cls.__dataclass_fields__ if k in d}
        known.setdefault("validation", {})
        known.setdefault("usage", {})
        return cls(**known)


def answer_path(h: str) -> Path:
    return get_paths().answers / f"{h}.json"


def save_answer(con: sqlite3.Connection | None, stored: StoredAnswer) -> Path:
    if not stored.created_at:
        stored.created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    p = answer_path(stored.qhash)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(stored.to_dict(), ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, p)
    if con is not None:
        upsert_row(con, stored)
    return p


def upsert_row(con: sqlite3.Connection, s: StoredAnswer) -> None:
    con.execute(
        "INSERT INTO answers_cache(qhash, question, filters, as_of_week, data_version, prompt_version, mode, model, "
        "effort, answer, trace, validation, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(qhash) DO UPDATE SET question=excluded.question, filters=excluded.filters, "
        "as_of_week=excluded.as_of_week, data_version=excluded.data_version, prompt_version=excluded.prompt_version, "
        "mode=excluded.mode, model=excluded.model, effort=excluded.effort, answer=excluded.answer, "
        "trace=excluded.trace, validation=excluded.validation, created_at=excluded.created_at",
        (s.qhash, s.question, json.dumps(s.filters, sort_keys=True), s.as_of_week, s.data_version, s.prompt_version,
         s.mode, s.model, s.effort, json.dumps(s.answer, ensure_ascii=False), json.dumps(s.trace, ensure_ascii=False),
         json.dumps(s.validation, ensure_ascii=False), s.created_at))
    con.commit()


def load_files() -> list[StoredAnswer]:
    out: list[StoredAnswer] = []
    d = get_paths().answers
    if not d.exists():
        return out
    for p in sorted(d.glob("*.json")):
        try:
            out.append(StoredAnswer.from_dict(json.loads(p.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError, TypeError):
            continue
    return out


def sync_table(con: sqlite3.Connection) -> int:
    """Load every answer file into answers_cache (idempotent). Returns the number of files."""
    files = load_files()
    for s in files:
        upsert_row(con, s)
    return len(files)


def load_answer(con: sqlite3.Connection | None, h: str) -> StoredAnswer | None:
    p = answer_path(h)
    if p.exists():
        try:
            return StoredAnswer.from_dict(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    if con is None:
        return None
    row = con.execute("SELECT * FROM answers_cache WHERE qhash = ?", (h,)).fetchone()
    if row is None:
        return None
    return StoredAnswer(
        qhash=row["qhash"], question=row["question"], filters=json.loads(row["filters"] or "{}"),
        as_of_week=row["as_of_week"] or "", data_version=row["data_version"] or "",
        prompt_version=row["prompt_version"] or "", mode=row["mode"] or "", model=row["model"] or "",
        effort=row["effort"] or "", answer=json.loads(row["answer"] or "{}"), trace=json.loads(row["trace"] or "[]"),
        validation=json.loads(row["validation"] or "{}"), created_at=row["created_at"] or "")


def find_exact(con: sqlite3.Connection | None, question: str, filters: Filters, as_of_week: str, data_version: str) -> StoredAnswer | None:
    return load_answer(con, qhash(question, filters, as_of_week, data_version))


def find_near(question: str, filters: Filters, data_version: str, threshold: float = 0.6) -> tuple[StoredAnswer, float] | None:
    """Closest recorded question by content-token Jaccard; same data_version; same filters preferred."""
    toks = content_tokens(question)
    if not toks:
        return None
    best: tuple[StoredAnswer, float] | None = None
    want = filters.canonical()
    for s in load_files():
        if s.data_version != data_version:
            continue
        other = content_tokens(s.question)
        for alias in (s.answer.get("aliases") or []):
            other |= content_tokens(alias)
        if not other:
            continue
        score = len(toks & other) / len(toks | other)
        if s.filters != want:
            score *= 0.85
        if score >= threshold and (best is None or score > best[1]):
            best = (s, score)
    return best


def replay_schedule(trace: list[dict[str, Any]], speed: float = REPLAY_SPEED, cap_ms: int = REPLAY_CAP_MS) -> list[tuple[int, str, dict[str, Any]]]:
    """(delay_ms, name, payload) tuples with the original inter-event gaps scaled and capped."""
    out: list[tuple[int, str, dict[str, Any]]] = []
    prev = 0
    for ev in trace:
        t = int(ev.get("t_ms", 0) or 0)
        delay = max(0, min(cap_ms, int((t - prev) * speed)))
        prev = t
        out.append((delay, str(ev.get("name", "status")), dict(ev.get("payload") or {})))
    return out


def list_questions(con: sqlite3.Connection | None, current_data_version: str) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for s in load_files():
        seen[s.qhash] = {"qhash": s.qhash, "question": s.question, "filters": s.filters, "mode": s.mode,
                         "model": s.model, "as_of_week": s.as_of_week, "data_version": s.data_version,
                         "created_at": s.created_at, "stale": s.data_version != current_data_version}
    return sorted(seen.values(), key=lambda x: x["created_at"])
