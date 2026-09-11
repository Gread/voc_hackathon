"""Loads taxonomy.json and cfpb_map.json and renders them for pydantic, prompts, SQL and the UI."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Literal

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def taxonomy() -> dict:
    return json.loads((HERE / "taxonomy.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def cfpb_map() -> dict:
    return json.loads((HERE / "cfpb_map.json").read_text(encoding="utf-8"))


def version() -> str:
    return taxonomy()["taxonomy_version"]


def codes(kind: str) -> list[str]:
    """Enum values for a taxonomy kind, in file order."""
    return list(taxonomy()[kind]["values"].keys())


def labels(kind: str) -> dict[str, str]:
    return {code: spec.get("label", code) for code, spec in taxonomy()[kind]["values"].items()}


def literal(kind: str):
    """A typing.Literal of the enum values, for pydantic fields."""
    return Literal[tuple(codes(kind))]  # type: ignore[valid-type]


def polarity_of_driver(driver_category: str) -> str:
    return taxonomy()["driver_categories"]["values"].get(driver_category, {}).get("polarity", "other")


def sql_enum(kind: str) -> str:
    """Comma-separated quoted values for a SQL CHECK constraint."""
    return ", ".join(f"'{c}'" for c in codes(kind))


def prompt_section(kind: str, with_examples: bool = True) -> str:
    """Markdown bullet list of codes with definitions and examples, for prompts."""
    lines = []
    for code, spec in taxonomy()[kind]["values"].items():
        line = f"- `{code}`"
        if spec.get("definition"):
            line += f": {spec['definition']}"
        elif spec.get("label"):
            line += f": {spec['label']}"
        if with_examples and spec.get("examples"):
            line += " (e.g. " + "; ".join(spec["examples"]) + ")"
        lines.append(line)
    return "\n".join(lines)


# --- CFPB metadata mapping (dimensions + QA only) --------------------------------------

def map_product(product_raw: str | None, sub_product_raw: str | None = None) -> str:
    m = cfpb_map()
    if sub_product_raw and sub_product_raw in m["sub_product_override"]:
        return m["sub_product_override"][sub_product_raw]
    return m["product"].get(product_raw or "", "other_or_unspecified")


def map_issue_to_reasons(issue_raw: str | None, sub_issue_raw: str | None = None) -> list[str]:
    """Contact reasons a CFPB issue/sub-issue plausibly corresponds to (agreement metric only)."""
    m = cfpb_map()
    if sub_issue_raw and sub_issue_raw in m["sub_issue_override"]:
        return list(m["sub_issue_override"][sub_issue_raw])
    return list(m["issue"].get(issue_raw or "", []))


def map_channel(submitted_via: str | None) -> str:
    return cfpb_map()["channel"].get(submitted_via or "", "other")


def map_segment(tags: str | None) -> str:
    return cfpb_map()["segment"].get(tags or "", "none")


@lru_cache(maxsize=1)
def _state_to_group() -> dict[str, str]:
    return {st: grp for grp, states in cfpb_map()["region_group"].items() for st in states}


def map_region_group(state: str | None) -> str:
    return _state_to_group().get((state or "").upper(), "other")
