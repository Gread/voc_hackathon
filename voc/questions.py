"""Demo question list (questions/demo.yaml or .json): the eight briefing questions with aliases and follow-ups."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from voc.config import REPO_ROOT

DEFAULT_PATH = REPO_ROOT / "questions" / "demo.yaml"


def _parse_minimal_yaml(text: str) -> list[dict[str, Any]]:
    """Reads the small subset used by questions/demo.yaml: a top-level `questions:` list of mappings
    with scalar values and simple string lists. No dependency on PyYAML."""
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    list_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#") or line.strip() == "questions:":
            continue
        indent = len(line) - len(line.lstrip())
        body = line.strip()
        if body.startswith("- ") and indent <= 2:
            current = {}
            items.append(current)
            list_key = None
            body = body[2:].strip()
            if not body:
                continue
        if current is None:
            continue
        if body.startswith("- "):
            if list_key:
                current.setdefault(list_key, []).append(_unquote(body[2:].strip()))
            continue
        if ":" in body:
            key, _, value = body.partition(":")
            key, value = key.strip(), value.strip()
            if value == "" or value == "[]":
                list_key = key
                current[key] = [] if value == "[]" else current.get(key, [])
            else:
                list_key = None
                current[key] = _scalar(value)
    return items


def _unquote(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _scalar(value: str) -> Any:
    if value.startswith("{") or value.startswith("["):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return _unquote(value)


def load_questions(path: Path | None = None) -> list[dict[str, Any]]:
    p = path or DEFAULT_PATH
    if not p.exists():
        alt = p.with_suffix(".json")
        if alt.exists():
            p = alt
        else:
            return []
    text = p.read_text(encoding="utf-8")
    if p.suffix == ".json":
        data = json.loads(text)
        items = data.get("questions", data) if isinstance(data, dict) else data
    else:
        items = _parse_minimal_yaml(text)
    out = []
    for i, item in enumerate(items, 1):
        if not item.get("question"):
            continue
        out.append({
            "id": str(item.get("id") or f"q{i}"),
            "question": str(item["question"]),
            "aliases": [str(a) for a in item.get("aliases") or []],
            "followups": [str(f) for f in item.get("followups") or []],
            "filters": item.get("filters") or {},
        })
    return out
