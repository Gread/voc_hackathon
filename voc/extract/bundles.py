"""Export bundles for build-time Claude agents: record text + the identical system prompt + the
precomputed cache key, so an agent can write data/cache/extract/<call_id>.json directly."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from voc.extract.prompt import PROMPT_VERSION, build_system_prompt, cache_key
from voc.paths import get_paths
from voc.schemas.call import CallRecord
from voc.schemas.extraction import EXTRACTION_API_SCHEMA, SCHEMA_VERSION
from voc.taxonomy import loader as tx

INSTRUCTIONS = (
    "For every record in `records`, act exactly as the system prompt in `system_prompt` instructs: read the "
    "record text and produce one Extraction JSON object that validates against `schema`. Then write the file "
    "`<cache_dir>/<cache_name>.json` with the cache-file contract described in README.md, copying `key`, "
    "`text_sha` and `call_id` verbatim from the record entry and putting your Extraction JSON under `response`. "
    "Quotes must be exact substrings of `text`. Do not use any information outside the record text."
)

README = """# Extraction bundles for build-time Claude agents

Each `bundle_NNN.json` holds up to N records that have no valid extraction yet, in round-robin order by month.

Bundle fields: `bundle_id`, `instructions`, `system_prompt` (the exact prompt the API path uses; follow it
literally), `schema` (the strict JSON schema of the Extraction object), `cache_dir` (where to write files),
`prompt_version`, `schema_version`, `taxonomy_version`, and `records`, each with
`call_id`, `text_sha`, `shape`, `cache_key`, `cache_name`, `text`.

## Cache-file contract (one file per record: `<cache_dir>/<cache_name>.json`)

```json
{
  "call_id": "<record.call_id>",
  "key": "<record.cache_key>",
  "prompt_version": "%(prompt_version)s",
  "schema_version": "%(schema_version)s",
  "taxonomy_version": "%(taxonomy_version)s",
  "text_sha": "<record.text_sha>",
  "model": "claude-agent-build",
  "produced_by": "claude_agent",
  "created_at": "2026-09-12T10:00:00+00:00",
  "usage": null,
  "response": { "...the Extraction JSON object..." }
}
```

Rules: write UTF-8 JSON with `ensure_ascii=false` semantics (keep non-ASCII characters as they are); write to a
`.tmp` file and rename it so a half-written file is never read; never edit the record text; `key`, `text_sha`
and `call_id` are copied from the bundle, never recomputed. Every quote in `response` must be a verbatim
substring of `text`; unverifiable quotes are kept but excluded from every UI surface.

Afterwards `python -m voc extract --load` validates each file through the same pydantic model and quote
verifier as the API path and consolidates everything into `data/extractions.jsonl` with `produced_by`
preserved. A file whose `response` cannot be repaired becomes a `status="error"` row with the message, and
`python -m voc extract --report` prints the invariants.
"""


def build_bundle(bundle_id: str, records: list[CallRecord], cache_dir: Path) -> dict[str, Any]:
    return {
        "bundle_id": bundle_id,
        "instructions": INSTRUCTIONS,
        "prompt_version": PROMPT_VERSION, "schema_version": SCHEMA_VERSION, "taxonomy_version": tx.version(),
        "cache_dir": str(cache_dir),
        "system_prompt": build_system_prompt(),
        "schema": EXTRACTION_API_SCHEMA,
        "records": [{"call_id": c.call_id, "text_sha": c.text_sha, "shape": c.shape,
                     "cache_key": cache_key(c.text_sha), "cache_name": c.call_id, "text": c.text}
                    for c in records],
    }


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def export_bundles(records: list[CallRecord], out_dir: Path, bundle_size: int) -> list[Path]:
    """Write DIR/bundle_000.json ... and DIR/README.md; records are already ordered and filtered."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = get_paths().cache_extract
    written: list[Path] = []
    for i in range(0, len(records), max(1, bundle_size)):
        bundle_id = f"bundle_{len(written):03d}"
        path = out_dir / f"{bundle_id}.json"
        _write_atomic(path, json.dumps(build_bundle(bundle_id, records[i:i + bundle_size], cache_dir),
                                       ensure_ascii=False, indent=1))
        written.append(path)
    _write_atomic(out_dir / "README.md", README % {"prompt_version": PROMPT_VERSION,
                                                    "schema_version": SCHEMA_VERSION,
                                                    "taxonomy_version": tx.version()})
    print(f"exported {len(records)} records in {len(written)} bundles -> {out_dir}")
    return written
