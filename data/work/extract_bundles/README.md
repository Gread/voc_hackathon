# Extraction bundles for build-time Claude agents

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
  "prompt_version": "ext-1.0",
  "schema_version": "1",
  "taxonomy_version": "1",
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
