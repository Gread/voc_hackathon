"""Theme registry (registry.json), members.jsonl and merges.json I/O, id allocation, prompt views."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from voc.config import get_settings
from voc.llm.client import LLMCacheMiss, LLMClient, LLMRequest, LLMResult, Usage
from voc.llm.cost import estimate_usd
from voc.schemas.theme import THEME_PROMPT_VERSION, Member, MergeRecord, Theme
from voc.theme.buckets import bucket_slug, split_bucket

CAP_PER_BUCKET = 60
MIN_CONFIDENCE = 0.5
MAX_EXAMPLES = 2
CATCH_ALL_PREFIX = "other: "
LIMITS = {"name": 60, "problem_statement": 200, "root_cause": 200}
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


# --- small file helpers ------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def write_json(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=1))


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    atomic_write_text(path, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


@lru_cache(maxsize=8)
def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def clip(text: Any, limit: int) -> str:
    s = " ".join(str(text or "").split())
    return s[:limit].rstrip()


def content_hash(*parts: Any) -> str:
    raw = "|".join(p if isinstance(p, str) else json.dumps(p, ensure_ascii=False, sort_keys=True) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# --- registry ------------------------------------------------------------------------------

def normalize_theme(d: dict[str, Any]) -> dict[str, Any]:
    """Theme dict validated through the contract, keeping grouping_quality (not in the frozen model)."""
    out = Theme.model_validate(d).model_dump()
    out["grouping_quality"] = d.get("grouping_quality", "ok")
    return out


class Registry:
    def __init__(self) -> None:
        self.themes: dict[str, dict[str, Any]] = {}
        self.codebook_version = 1
        self.produced_by: str | None = None
        self.passes_done: list[str] = []
        self.stability: dict[str, Any] | None = None

    @classmethod
    def load(cls, path: Path) -> "Registry":
        reg = cls()
        data = read_json(path, {}) or {}
        for t in data.get("themes", []):
            t = normalize_theme(t)
            reg.themes[t["theme_id"]] = t
        reg.codebook_version = int(data.get("codebook_version", 1))
        reg.produced_by = data.get("produced_by")
        reg.passes_done = list(data.get("passes_done", []))
        reg.stability = data.get("stability")
        return reg

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"theme_prompt_version": THEME_PROMPT_VERSION, "codebook_version": self.codebook_version,
                               "produced_by": self.produced_by, "passes_done": self.passes_done,
                               "themes": list(self.themes.values())}
        if self.stability is not None:
            out["stability"] = self.stability
        return out

    def save(self, path: Path) -> None:
        write_json(path, self.to_dict())

    def _next_id(self, bucket: str) -> str:
        """Ids are numbered within their own bucket.

        A global counter made a bucket's ids depend on how many themes every other bucket had already
        created, so one bucket gaining a theme renumbered another's. That invalidated cached batches and,
        worse, could re-point assignments already written against the old numbering."""
        slug = bucket_slug(bucket)
        n = sum(1 for t in self.themes.values() if t.get("bucket") == bucket)
        while True:
            n += 1
            candidate = f"thm_{slug}_{n:03d}"
            if candidate not in self.themes:
                return candidate

    def get(self, theme_id: str) -> dict[str, Any]:
        return self.themes[theme_id]

    def catch_all_id(self, bucket: str) -> str | None:
        for t in self.themes.values():
            if t["bucket"] == bucket and t["status"] == "catch_all":
                return t["theme_id"]
        return None

    def ensure_catch_all(self, bucket: str) -> str:
        existing = self.catch_all_id(bucket)
        if existing:
            return existing
        dc, pol = split_bucket(bucket)
        t = self._new(bucket, f"{CATCH_ALL_PREFIX}{dc}", f"Statements about {dc.replace('_', ' ')} that fit no specific theme.",
                      "unassigned or low-confidence rows", created_pass="seed", status="catch_all")
        return t["theme_id"]

    def add(self, bucket: str, name: str, problem_statement: str, root_cause: str,
            created_pass: str = "seed", examples: list[str] | None = None) -> dict[str, Any]:
        return self._new(bucket, name, problem_statement, root_cause, created_pass, "active", examples)

    def _new(self, bucket: str, name: str, problem: str, root_cause: str, created_pass: str, status: str,
             examples: list[str] | None = None) -> dict[str, Any]:
        dc, pol = split_bucket(bucket)
        t = normalize_theme({
            "theme_id": self._next_id(bucket), "name": clip(name, LIMITS["name"]) or f"theme {len(self.themes) + 1}",
            "problem_statement": clip(problem, LIMITS["problem_statement"]), "root_cause": clip(root_cause, LIMITS["root_cause"]),
            "polarity": pol, "driver_category": dc, "bucket": bucket, "status": status, "merged_into": None,
            "created_pass": created_pass, "codebook_version": self.codebook_version,
            "examples": list(examples or [])[:MAX_EXAMPLES],
        })
        self.themes[t["theme_id"]] = t
        return t

    def active(self, bucket: str | None = None) -> list[dict[str, Any]]:
        return [t for t in self.themes.values() if t["status"] == "active" and (bucket is None or t["bucket"] == bucket)]

    def effective(self, theme_id: str) -> str:
        seen = set()
        while theme_id in self.themes and self.themes[theme_id].get("merged_into") and theme_id not in seen:
            seen.add(theme_id)
            theme_id = self.themes[theme_id]["merged_into"]
        return theme_id

    def mark_merged(self, loser: str, winner: str) -> None:
        lt, wt = self.themes[loser], self.themes[winner]
        lt["status"], lt["merged_into"] = "merged", winner
        for ex in lt.get("examples", []):
            self.add_example(winner, ex)
        if wt["status"] != "catch_all":
            wt["status"] = "active"

    def add_example(self, theme_id: str, statement: str) -> None:
        ex = self.themes[theme_id].setdefault("examples", [])
        if len(ex) < MAX_EXAMPLES and statement and statement not in ex:
            ex.append(statement)

    def offered(self, bucket: str) -> list[dict[str, Any]]:
        """Themes a bucket's rows may be assigned to: its active themes plus cross-bucket absorbers."""
        out = {t["theme_id"]: t for t in self.active(bucket)}
        for t in self.themes.values():
            if t["bucket"] == bucket and t["status"] == "merged":
                eff = self.themes.get(self.effective(t["theme_id"]))
                if eff and eff["status"] == "active":
                    out.setdefault(eff["theme_id"], eff)
        return list(out.values())

    def rename(self, theme_id: str, name: str, problem_statement: str, root_cause: str) -> None:
        t = self.themes[theme_id]
        t["name"] = clip(name, LIMITS["name"]) or t["name"]
        t["problem_statement"] = clip(problem_statement, LIMITS["problem_statement"]) or t["problem_statement"]
        t["root_cause"] = clip(root_cause, LIMITS["root_cause"]) or t["root_cause"]
        t["codebook_version"] = self.codebook_version


def prompt_view(themes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """What the model sees of a theme: id, name, definition, two example statements."""
    return [{"theme_id": t["theme_id"], "name": t["name"], "problem_statement": t["problem_statement"],
             "root_cause": t["root_cause"], "examples": list(t.get("examples", []))[:MAX_EXAMPLES]} for t in themes]


def registry_hash(view: list[dict[str, Any]]) -> str:
    return content_hash(view)[:12]


def row_view(row: dict[str, Any]) -> dict[str, Any]:
    return {k: row[k] for k in ("topic_id", "product", "sentiment", "issue_statement", "driver", "driver_category")}


def render_registry(view: list[dict[str, Any]]) -> str:
    if not view:
        return "(the registry is empty)"
    lines = []
    for t in view:
        ex = "; ".join(f'"{e}"' for e in t.get("examples", [])) or "none yet"
        lines.append(f"- {t['theme_id']} | {t['name']} | problem: {t['problem_statement']} | cause: {t['root_cause']} | examples: {ex}")
    return "\n".join(lines)


def render_rows(rows: list[dict[str, Any]]) -> str:
    return "\n".join(f"{i + 1}. [{r['topic_id']}] product={r['product']} sentiment={r['sentiment']} "
                     f"category={r['driver_category']}\n   statement: {r['issue_statement']}\n   driver: {r['driver']}"
                     for i, r in enumerate(rows))


# --- members and merges ---------------------------------------------------------------------

def member(topic_id: str, theme_id: str, confidence: float, pass_name: str, batch_id: str) -> dict[str, Any]:
    m = Member(topic_id=topic_id, theme_id=theme_id, confidence=round(float(confidence), 3), pass_=pass_name, batch_id=batch_id)
    return m.model_dump(by_alias=True)


def write_members(path: Path, members: list[dict[str, Any]]) -> None:
    write_jsonl(path, members)


def read_members(path: Path) -> list[dict[str, Any]]:
    return [Member.model_validate(m).model_dump(by_alias=True) for m in read_jsonl(path)]


def merge_record(from_theme: str, into_theme: str, pass_name: str, reason: str, judged_by: str) -> dict[str, Any]:
    r = MergeRecord(from_theme=from_theme, into_theme=into_theme, pass_=pass_name, reason=clip(reason, 120),
                    judged_by=judged_by, created_at=utc_now())
    return r.model_dump(by_alias=True)


def read_merges(path: Path) -> dict[str, Any]:
    data = read_json(path, {}) or {}
    return {"merges": list(data.get("merges", [])), "decisions": list(data.get("decisions", []))}


def write_merges(path: Path, merges: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> None:
    write_json(path, {"merges": merges, "decisions": decisions})


# --- run plumbing ----------------------------------------------------------------------------

@dataclass
class ThemeOptions:
    batch_size: int = 100
    sequential: int = 5          # batches per bucket that grow the registry one at a time
    concurrency: int = 4
    cap: int = CAP_PER_BUCKET
    limit_buckets: int | None = None
    on_miss: str = "raise"       # raise | skip (skip: a cache miss leaves the bucket pending)


# A 100-row batch answers with ~3k tokens of JSON, and models whose reasoning cannot be disabled
# spend part of the completion budget before writing any of it. At 8192 a third of the batches came
# back truncated, and the statements they dropped silently became unassigned.
THEME_MAX_TOKENS = 32000


def make_request(stage: str, cache_name: str, cache_key: str, prompt_name: str, user: str,
                 schema: dict[str, Any], meta: dict[str, Any], effort: str | None = None) -> LLMRequest:
    settings = get_settings()
    return LLMRequest(stage=stage, model=settings.theme_model, system=load_prompt(prompt_name), user=user,
                      schema=schema, effort=effort or settings.theme_effort, max_tokens=THEME_MAX_TOKENS,
                      cache_name=cache_name, cache_key=cache_key, meta=meta)


async def _gather(client: LLMClient, reqs: list[LLMRequest], concurrency: int) -> list[Any]:
    sem = asyncio.Semaphore(max(1, concurrency))

    async def one(req: LLMRequest) -> LLMResult:
        async with sem:
            return await client.acomplete_json(req)

    return list(await asyncio.gather(*(one(r) for r in reqs), return_exceptions=True))


def gather_requests(client: LLMClient, reqs: list[LLMRequest], concurrency: int,
                    tolerate: type[BaseException] | tuple[type[BaseException], ...] = ()) -> list[Any]:
    """Run requests concurrently; cache misses win over other errors so the caller can report pending work.

    Exceptions listed in `tolerate` are handed back in place of their result, so the caller can decide
    what to do with that one batch instead of losing the whole run.
    """
    if not reqs:
        return []
    results = asyncio.run(_gather(client, reqs, concurrency))
    errors = [r for r in results if isinstance(r, BaseException) and not isinstance(r, tolerate or ())]
    if errors:
        misses = [e for e in errors if isinstance(e, LLMCacheMiss)]
        raise (misses[0] if misses else errors[0])
    return results


@dataclass
class RunStats:
    model: str = ""
    requests: int = 0
    cached: int = 0
    usage: Usage = field(default_factory=Usage)
    produced_by: set[str] = field(default_factory=set)

    def record(self, result: LLMResult) -> None:
        self.requests += 1
        self.cached += int(result.cached)
        self.usage = self.usage.add(result.usage)
        self.produced_by.add(result.produced_by)

    def produced_by_label(self) -> str:
        if not self.produced_by:
            return "none"
        if "fake" in self.produced_by:
            return "fake"
        return "+".join(sorted(self.produced_by))

    def summary(self) -> str:
        usd = estimate_usd(self.model, self.usage)
        return (f"{self.requests} requests ({self.cached} from cache), produced_by={self.produced_by_label()}, "
                f"tokens in={self.usage.input_tokens} out={self.usage.output_tokens} est=${usd:.2f}")
