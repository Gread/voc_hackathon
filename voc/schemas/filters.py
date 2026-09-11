"""Shared filter object for tools, REST endpoints and cached-answer keys."""
from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel

from voc.taxonomy import loader as tx

DIMENSIONS = ("product", "channel", "region_group", "region", "segment", "company")


class Filters(BaseModel):
    product: list[str] | None = None
    channel: list[str] | None = None
    region_group: list[str] | None = None
    region: list[str] | None = None
    segment: list[str] | None = None
    company: list[str] | None = None
    date_from: str | None = None
    date_to: str | None = None

    def canonical(self) -> dict[str, Any]:
        """Sorted, null-free dict used for cache keys and display."""
        out: dict[str, Any] = {}
        for dim in DIMENSIONS:
            vals = getattr(self, dim)
            if vals:
                out[dim] = sorted(set(vals))
        if self.date_from:
            out["date_from"] = self.date_from
        if self.date_to:
            out["date_to"] = self.date_to
        return out

    def canonical_json(self) -> str:
        return json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))

    def is_empty(self) -> bool:
        return not self.canonical()

    def describe(self) -> str:
        parts = [f"{k}={','.join(v) if isinstance(v, list) else v}" for k, v in self.canonical().items()]
        return "; ".join(parts) if parts else "all calls"

    @classmethod
    def from_query(cls, params: dict[str, Any]) -> "Filters":
        """Build from query-string style params where list values may be repeated or comma-separated."""
        kw: dict[str, Any] = {}
        for dim in DIMENSIONS:
            raw = params.get(dim)
            if raw is None:
                continue
            items = raw if isinstance(raw, list) else [raw]
            vals = [v.strip() for item in items for v in str(item).split(",") if v.strip()]
            if vals:
                kw[dim] = vals
        for k in ("date_from", "date_to"):
            if params.get(k):
                kw[k] = str(params[k])
        return cls(**kw)

    @classmethod
    def from_any(cls, value: Any) -> "Filters":
        if value is None:
            return cls()
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            value = json.loads(value) if value.strip() else {}
        return cls.model_validate({k: v for k, v in dict(value).items() if v is not None})


def _nullable_list(enum: list[str] | None) -> dict:
    items: dict = {"type": "string"}
    if enum:
        items["enum"] = enum
    return {"type": ["array", "null"], "items": items}


FILTERS_API_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": list(DIMENSIONS) + ["date_from", "date_to"],
    "properties": {
        "product": _nullable_list(tx.codes("products")),
        "channel": _nullable_list(tx.codes("channel")),
        "region_group": _nullable_list(tx.codes("region_group")),
        "region": _nullable_list(None),
        "segment": _nullable_list(tx.codes("segment")),
        "company": _nullable_list(None),
        "date_from": {"type": ["string", "null"]},
        "date_to": {"type": ["string", "null"]},
    },
}
