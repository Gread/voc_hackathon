# Cache file formats (the hand-off between the pipeline and build-time Claude agents)

Every LLM call in the pipeline is cached as one JSON file under `data/cache/<stage>/`. The files are the
contract: whoever writes them (the API path, a build-time Claude agent, or the fake client) produces the same
shape, and the stage's `--load` step validates every file through the same code path. `data/cache/` is
gitignored; the consolidated outputs (`data/extractions.jsonl`, `data/themes/*`) are committed.

## 1. Extraction cache files — `data/cache/extract/<call_id>.json` (DESIGN §5.6)

```json
{
  "call_id": "cfpb_7391825",
  "key": "sha256(prompt_version|schema_version|taxonomy_version|text_sha)",
  "prompt_version": "ext-1.0",
  "schema_version": "1",
  "taxonomy_version": "1",
  "text_sha": "9f2c...",
  "model": "claude-sonnet-5",
  "produced_by": "api",
  "created_at": "2026-09-12T10:00:00+00:00",
  "usage": {"input_tokens": 812, "output_tokens": 690, "cache_read_input_tokens": 6400, "cache_creation_input_tokens": 0},
  "response": { "...the Extraction JSON object exactly as in DESIGN §5.2..." }
}
```

| Field | Value |
|-------|-------|
| `key` | `sha256(f"{prompt_version}|{schema_version}|{taxonomy_version}|{text_sha}")` (`voc.extract.prompt.cache_key`). A file whose key differs from the current one is **stale** and is re-requested (or re-exported) automatically. |
| `model` | `claude-sonnet-5` / `claude-haiku-4-5` for the API path; `claude-agent-build` for build-time agents; `fake` for the fake client. |
| `produced_by` | `api`, `claude_agent` or `fake`. Preserved into `extractions.jsonl`; `build-db` refuses fake files unless `VOC_LLM=fake`. |
| `created_at` | ISO 8601 UTC; becomes `extracted_at` in `extractions.jsonl`. |
| `usage` | Token usage object for API calls; `null` for agents. |
| `response` | The Extraction JSON (`voc.schemas.extraction.EXTRACTION_API_SCHEMA`). |

Files written by the API or fake path also carry `text` (the record text, copied from the request metadata by
`CachedClient`); agents may omit it. Extra fields are ignored by the loader.

**Error markers.** When a request fails (API error, refusal, malformed JSON) the runner writes the same file
with `"response": null` and an `"error"` string. Such a file loads as a `status="error"` row and counts as
pending on the next run, so failures are visible and retried without any bookkeeping.

**Validation on load** (`voc extract --load`, also run at the end of every `voc extract`): key check → 
`normalize_extraction` (bounds, enums, primary-reason rule; repairs are recorded as `flags`) → verbatim quote
verification (`char_start`, `char_end`, `verified`, `match_kind ∈ {exact, normalized}`, never fuzzy) → 
transcript speaker relabelling → consistency flags (`sentiment_inconsistent`, `product_mismatch`,
`no_verified_quotes`, `heavy_redaction`) → one row per call in `data/extractions.jsonl`:

```json
{"call_id": "...", "status": "ok" | "error", "error": null | "message", "produced_by": "...", "model": "...",
 "prompt_version": "ext-1.0", "schema_version": "1", "extracted_at": "...", "flags": ["..."],
 "quote_verify_rate": 0.83, "extraction": { "...normalised Extraction with enriched evidence..." }}
```

Inside `extraction`, every `topics[].evidence[]` and `positive_moments[]` item gains `char_start`, `char_end`,
`verified` (0/1) and `match_kind`; every topic gains `evidence_ok` (1 when at least one quote verified). Rows
are sorted by `call_id`; calls without any cache file have no row (`--report` prints them as `n_missing`).

## 2. Extraction bundles for agents — `voc extract --export DIR --bundle-size 20`

`DIR/bundle_000.json`, `bundle_001.json`, … each hold up to N pending records (no valid cache file, or a stale
key), ordered round-robin by month so that any partially processed set stays uniform over time:

```json
{
  "bundle_id": "bundle_000",
  "instructions": "For every record ... write <cache_dir>/<cache_name>.json ...",
  "prompt_version": "ext-1.0", "schema_version": "1", "taxonomy_version": "1",
  "cache_dir": "C:/.../data/cache/extract",
  "system_prompt": "<the exact text of voc.extract.prompt.build_system_prompt()>",
  "schema": { "...EXTRACTION_API_SCHEMA..." },
  "records": [
    {"call_id": "cfpb_7391825", "text_sha": "9f2c...", "shape": "narrative",
     "cache_key": "<precomputed key>", "cache_name": "cfpb_7391825", "text": "I was charged ..."}
  ]
}
```

`DIR/README.md` restates the cache-file contract for the agent. The agent follows `system_prompt` literally for
each record, writes `<cache_dir>/<cache_name>.json` with `model: "claude-agent-build"`,
`produced_by: "claude_agent"`, `usage: null`, and copies `key`, `text_sha` and `call_id` verbatim. Then:

```
python -m voc extract --load      # validate + consolidate (agent files and API files alike)
python -m voc extract --report    # invariants: ok/error, other share, quote verify rate, agreement, histogram
```

The runner skips any record whose cache file matches the current key whatever `produced_by` says;
`--force-api` re-extracts agent- or fake-produced records through the API when a key exists so the two can be
compared as a QA set.

## 3. Run bookkeeping

- `data/work/extract_runs.jsonl`: one line per `voc extract` run (requested, ok, errors, cached hits, token
  usage, estimated USD, budget-guard hit, arguments). `build-db` may load it into `run_log`.
- `data/work/extract_report.json`: the last `--report` output.

## 4. Theming cache files — `data/cache/theme/…`

Per-batch files of the three theming passes (`seed/<bucket>/<batch>_<registry_hash>.json`,
`reassign/…`, consolidation decisions) follow the same envelope (`key`, `model`, `produced_by`, `created_at`,
`usage`, `response`) with `response` being the pass output schema from `voc/schemas/theme.py`
(`SEED_API_SCHEMA`, `CONSOLIDATE_API_SCHEMA`, `REASSIGN_API_SCHEMA`, `RENAME_API_SCHEMA`). Bundle export and
import for agents are `voc theme --export` / `--import` (DESIGN §6.7); the theme lane documents the bucket-level
bundle fields in its README.
