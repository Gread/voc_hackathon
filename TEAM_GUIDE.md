# Team guide

How the pieces fit, who can work where without colliding, and three recipes for extending it.

## Run it in two minutes

```bash
pip install -e ".[dev]"
python -m voc serve          # http://127.0.0.1:8000
pytest                       # the suite runs on fixtures, no network, no API key
```

`data/` is committed, so a clone serves the finished demo immediately. Put `ANTHROPIC_API_KEY` in `.env`
to switch the Ask panel from recorded to live.

## The shape of the system

```
data/calls.jsonl      one normalised contact per line        <- voc/ingest
data/extractions.jsonl one extraction per contact            <- voc/extract   (LLM)
data/themes/*         registry, memberships, merge log       <- voc/theme     (LLM)
data/voc.sqlite       derived index, rebuilt in seconds      <- voc/store/build.py
data/answers/*.json   recorded answers with their traces     <- voc/agent/record.py
```

Two rules keep this honest and make it safe to work on in parallel:

1. **Files are the truth, SQLite is an index.** `voc build-db` drops and recreates the database from the
   files. Never hand-edit the database; change a file and rebuild.
2. **Every model call is cached by content hash.** `data/cache/<stage>/<name>.json` holds the response.
   Re-running a stage costs nothing, and a killed run resumes. Changing a prompt version or the taxonomy
   changes the hash, which re-runs exactly what it should.

## Module ownership

Five people can work at once with almost no overlap:

| Area | Files | Depends on |
|---|---|---|
| Data | `voc/ingest/*` | the record contract in `voc/schemas/call.py` |
| Extraction | `voc/extract/*` | `voc/schemas/extraction.py`, the taxonomy |
| Theming and trends | `voc/theme/*`, `voc/analytics/*` | the extraction row shape |
| Agent and API | `voc/agent/*`, `voc/api/*`, `voc/store/queries.py` | the SQLite schema |
| UI | `voc/web/*` | the REST endpoints and the event vocabulary |

The frozen contracts everyone shares are `voc/taxonomy/taxonomy.json`, `voc/schemas/*` and
`voc/store/schema.sql`. Changing one of those is a team decision, not a lane decision: the taxonomy version
is part of every extraction cache key, so editing it invalidates the extractions on purpose.

## Working without an API key

Every LLM stage has the same three-way switch, `VOC_LLM`:

- `cached` (default): replay cache files; fall through to the API when a key exists.
- `live`: always call the API and refresh the cache.
- `fake`: deterministic heuristics, for tests and CI. A fake-produced index is refused by `build-db`
  unless `VOC_LLM=fake`, and then the UI shows a red FAKE DATA banner so it can never be mistaken for real.

To have Claude agents do the reading instead of the API:

```bash
python -m voc extract --export data/work/extract_bundles --bundle-size 25
# agents write data/cache/extract/<call_id>.json per docs/cache_formats.md
python -m voc extract --load
```

Theming works the same way but iteratively, because a batch's cache identity depends on the registry the
earlier batches built: `voc theme export --dir DIR --pass seed`, fill the bundles, `voc theme import
--dir DIR --pass seed`, export again. When export reports 0 bundles the pass is done.

## Three extension recipes

### 1. Add a contact reason (or any enum value)

Edit `voc/taxonomy/taxonomy.json`, bump `taxonomy_version`, and add the mapping rows in `cfpb_map.json` if
the new value corresponds to a complaint-form issue. Everything downstream follows automatically: the
pydantic model, the extraction JSON schema, the prompt section, the SQL `CHECK` constraints, the filter
enums and the UI labels are all rendered from that one file. Then re-run `voc extract` (the version bump
invalidates the cache) and `voc build-db`.

### 2. Add an analysis tool the agent can call

1. Write the query in `voc/store/queries.py` returning `q.result(rows=..., data=..., scope=...)`; use
   `q.calls(...)` for the statement whose rows carry the call ids, so the result's call list is recorded.
2. Add a spec to `TOOL_SPECS` and a dispatch entry in `voc/agent/tools.py`. The description should say
   *when* to call it, not just what it does.
3. Add a REST route in `voc/api/app.py` if the dashboard needs it.

The envelope, the result persistence, the "rows" link and the claim verification all come for free.

### 3. Add a dashboard panel

Add the markup to `voc/web/index.html`, a render function in `voc/web/js/dashboard.js` following the
existing pattern (one API call, build nodes with `el()`, never `innerHTML` with data), and call it from
`renderAll()`. There is no build step: refresh the page.

## Things that will bite you

- **Quotes must be exact substrings.** The verifier accepts an exact match or a whitespace and
  punctuation-normalised match, and nothing else. Unverified quotes are kept in the JSON but never reach
  the UI, a tool result or the agent.
- **Counting unit is the call.** A theme, reason or driver counts at most once per call, and every share is
  over the calls in the same filtered slice. Do not count topics.
- **Minimum support.** Nothing is ranked below five calls, and a segment cell is blanked below fifty calls
  in the slice. This is deliberate; do not relax it to make a chart look fuller.
- **Never feed the complaint form's labels to the extractor.** They are the free agreement metric; using
  them as a hint destroys it and biases reasons toward the form's dropdown.
- **The server decides confidence.** The model proposes claims; `voc/agent/answer.py` recounts them from
  call ids and computes the tier. If you add a claim path, route it through `verify_answer`.
- **Windows paths and encodings.** Everything opens files with `encoding="utf-8"` and writes atomically
  (temp file then replace). Keep it that way.

## Where to look first

| Question | File |
|---|---|
| What exactly does the extractor ask for? | `voc/extract/prompt_system.md` |
| How is a theme decided? | `voc/theme/prompts/seed.md`, `voc/theme/consolidate.py` |
| How is "emerging" computed? | `voc/analytics/emerging.py` (and `docs/DESIGN.md` section 7.2) |
| What can the agent do? | `voc/agent/tools.py` |
| How is an answer checked? | `voc/agent/answer.py` |
| What does the demo say? | `docs/demo_script.md` |
