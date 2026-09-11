"""Theme registry, membership and the strict output schemas of the three theming passes."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

THEME_PROMPT_VERSION = "thm-1.0"
POLARITIES = ["negative", "positive", "neutral"]


class Theme(BaseModel):
    theme_id: str                      # thm_0042
    name: str
    problem_statement: str
    root_cause: str
    polarity: str
    driver_category: str
    bucket: str                        # "<driver_category>|<polarity>"
    status: str = "active"             # active | merged | catch_all
    merged_into: str | None = None
    created_pass: str = "seed"
    codebook_version: int = 1
    examples: list[str] = Field(default_factory=list)   # two example statements for prompts


class Member(BaseModel):
    topic_id: str
    theme_id: str
    confidence: float
    pass_: str = Field(alias="pass")   # seed | reassign | fallback | fake
    batch_id: str = ""

    model_config = {"populate_by_name": True}


class MergeRecord(BaseModel):
    from_theme: str
    into_theme: str
    pass_: str = Field(alias="pass")
    reason: str
    judged_by: str
    created_at: str

    model_config = {"populate_by_name": True}


# --- pass outputs -----------------------------------------------------------------------

class Assignment(BaseModel):
    topic_id: str
    theme_id: str                      # existing id | NEW-k | NONE
    confidence: float


class NewTheme(BaseModel):
    tmp_id: str                        # NEW-1 ...
    name: str
    problem_statement: str
    root_cause: str
    polarity: str


class SeedOutput(BaseModel):
    assignments: list[Assignment]
    new_themes: list[NewTheme]


class MergeDecision(BaseModel):
    a: str
    b: str
    merge: bool
    into: str
    reason: str


class ConsolidateOutput(BaseModel):
    decisions: list[MergeDecision]


class ReassignOutput(BaseModel):
    assignments: list[Assignment]


class Rename(BaseModel):
    theme_id: str
    name: str
    problem_statement: str
    root_cause: str


class RenameOutput(BaseModel):
    themes: list[Rename]


def _obj(required: list[str], props: dict[str, Any]) -> dict:
    return {"type": "object", "additionalProperties": False, "required": required, "properties": props}


ASSIGNMENT_SCHEMA = _obj(["topic_id", "theme_id", "confidence"],
                         {"topic_id": {"type": "string"}, "theme_id": {"type": "string"}, "confidence": {"type": "number"}})

SEED_API_SCHEMA = _obj(["assignments", "new_themes"], {
    "assignments": {"type": "array", "items": ASSIGNMENT_SCHEMA},
    "new_themes": {"type": "array", "items": _obj(["tmp_id", "name", "problem_statement", "root_cause", "polarity"], {
        "tmp_id": {"type": "string"}, "name": {"type": "string"}, "problem_statement": {"type": "string"},
        "root_cause": {"type": "string"}, "polarity": {"type": "string", "enum": POLARITIES}})},
})

CONSOLIDATE_API_SCHEMA = _obj(["decisions"], {
    "decisions": {"type": "array", "items": _obj(["a", "b", "merge", "into", "reason"], {
        "a": {"type": "string"}, "b": {"type": "string"}, "merge": {"type": "boolean"},
        "into": {"type": "string"}, "reason": {"type": "string"}})},
})

REASSIGN_API_SCHEMA = _obj(["assignments"], {"assignments": {"type": "array", "items": ASSIGNMENT_SCHEMA}})

RENAME_API_SCHEMA = _obj(["themes"], {
    "themes": {"type": "array", "items": _obj(["theme_id", "name", "problem_statement", "root_cause"], {
        "theme_id": {"type": "string"}, "name": {"type": "string"},
        "problem_statement": {"type": "string"}, "root_cause": {"type": "string"}})},
})
