# Voice of the Customer Insights

Turning thousands of contact-centre conversations into evidence-based insight, with agents doing the reading.

A proof of concept for the hackathon briefing of 11 September 2026. It reads every customer contact into
a consistent structure, groups differently-worded descriptions of the same experience into themes, watches
how those themes move week by week, and answers plain-language business questions with counts, trends,
quotes and a confidence that the server computes rather than the model claims.

## Run it

```bash
pip install -e .
python -m voc serve
```

Then open http://127.0.0.1:8000. The index rebuilds itself if the files under `data/` changed.

Without an `ANTHROPIC_API_KEY` the demo still works: recorded answers replay through the same channel as
live ones, and any unscripted question gets a templated answer from the same tools, clearly badged. With a
key in `.env`, the Ask panel runs the agent live.

## The data

Real, public consumer complaint narratives about one large US bank, pulled from the
[CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/).

| | |
|---|---|
| Corpus | 4,425 narratives, 24 months (July 2024 to June 2026) |
| Sampling | constant 25.25% of that bank's eligible narratives per month, fixed seed, hash-based |
| Eligible population | 17,822 of 18,641 pulled (narratives of at least 30 words, deduplicated) |
| Metadata | product, sub-product, issue, state, region group, submission channel, segment tags, dates |
| Redactions | `XXXX` and `XX/XX/XXXX` are the regulator's and are kept verbatim in every quote |

Every record is a real complaint written by a real person who consented to publication. Nothing in `data/`
is synthetic; the only planted patterns live in `tests/fixtures`, where the analytics are checked against
known answers. Three honest caveats, two of which the UI states out loud:

- Dates are when the regulator received the complaint, which lags the contact by days to weeks.
- The corpus is complaints, so satisfaction findings are *positive moments inside complaints*, not a
  measure of overall satisfaction.
- The briefing expects the stated reason ("I want to cancel") to differ often from the real driver ("I was
  charged twice and nobody called back"). In this corpus it differs in only about 1 contact in 75. That
  looks like a property of the medium rather than a gap in the reading: someone writing a formal complaint
  to a regulator leads with their actual grievance, where someone phoning a contact centre opens with what
  they want. The system extracts the distinction and it is worth keeping, because on real call transcripts
  it should be far more common. Where it does occur the reading is good, for example a customer asking for
  a hold to be released whose underlying account is a representative giving wrong advice and the bank then
  blaming them for it.

## The five steps

1. **Read every call.** Each contact goes to Claude once and comes back as a fixed structure: contact
   reasons (a small taxonomy plus the specific reason in the customer's words), products, services, one or
   more topics each with a sentiment from -2 to +2, the specific driver of that feeling, verbatim evidence
   quotes, what the customer asked for, and the stated reason versus the underlying driver. The complaint
   form's own product and issue labels are deliberately never shown to the extractor, which keeps them free
   as an agreement metric.
2. **Connect to the collective.** Topics are bucketed by driver category and polarity, then three LLM
   passes seed a theme registry, consolidate near-duplicates through an audit trail that never deletes
   membership, and re-assign every topic against the frozen registry. A theme is one problem with one
   plausible cause that one team could fix.
3. **Watch the shape over time.** Counts by ISO week, with an emerging score comparing the last four weeks
   against the sixteen before (Poisson z with a Jeffreys pseudo-count, minimum support of five calls in at
   least two weeks). Scores are precomputed for *every* as-of week, so the dashboard slider replays a theme
   from its first handful of calls.
4. **Answer plain-language questions.** An agent takes the question, chooses what to pull from twelve
   read-only tools, and submits a structured answer.
5. **Show evidence and confidence.** The server recounts every claim from call ids before it is rendered,
   checks each quoted number against the tool result it cites, drops quotes that are not verified evidence,
   and computes the confidence tier itself. Claims it cannot support are shown greyed with the correction
   beside them, never silently dropped.

## Commands

```bash
python -m voc ingest pull --start 2024-07 --end 2026-06   # real data into data/raw/ (month by month, cached)
python -m voc ingest profile --target 4500                # per-month/week/product profile and the support gate
python -m voc ingest sample --target 4500 --seed 20260911 # -> data/calls.jsonl
python -m voc extract                                     # step 1 (add --dry-run first to see the cost)
python -m voc theme run                                   # step 2 (seed, consolidate, reassign, stability)
python -m voc build-db                                    # files -> data/voc.sqlite, then materialise trends
python -m voc qa                                          # extraction quality metrics
python -m voc ask "Which issues are growing fastest?"     # step 4 from the shell
python -m voc serve                                       # the dashboard and the Ask API
python -m voc run-all --limit 30                          # the whole chain (VOC_LLM=fake for CI)
pytest
```

Files under `data/` are the source of truth; `data/voc.sqlite` is a derived index that `build-db` recreates
in seconds. Every stage is resumable and caches each model call by content hash, so a re-run costs nothing
and a partial run can be continued.

## Working without an API key

Every LLM stage can be done by build-time Claude agents instead of the API, writing the same cache files:

```bash
python -m voc extract --export data/work/extract_bundles --bundle-size 25
python -m voc theme export --dir data/work/theme_bundles --pass seed
python -m voc record-answer start --question "..."        # then drive `voc tool` and finalize
```

Each bundle carries the exact prompt, the records and the cache identity to write. See
[docs/cache_formats.md](docs/cache_formats.md). The runner does not care who did the reading; `produced_by`
records it, and a fake-produced index is refused unless `VOC_LLM=fake`, in which case the UI shows a red
warning banner.

## Layout

```
voc/taxonomy/   the enums, their definitions, and the CFPB mapping used for dimensions and QA
voc/schemas/    the call, extraction, theme, filter and answer contracts (pydantic + strict JSON schema)
voc/llm/        one interface over live, cached and fake clients, plus the cost table
voc/ingest/     CFPB pull, profile gate, hash sampling, transcript normaliser
voc/extract/    step 1: prompt, async runner, quote verification, validation, work bundles
voc/theme/      step 2: bucketing, the three passes, the merge audit trail, stability
voc/analytics/  step 3: Wilson intervals, the emerging score, segment lift, confidence tiers
voc/store/      the SQLite schema, the builder, and every query the tools and the API run
voc/agent/      step 4 and 5: tools, the manual loop, the verifier, the cache, the offline analyst
voc/api/        FastAPI endpoints and the event stream
voc/web/        the dashboard: static ES modules, vendored Chart.js, no build step
```

See [docs/DESIGN.md](docs/DESIGN.md) for the full design, [docs/BUILD_LOG.md](docs/BUILD_LOG.md) for what
was built and what the real data showed, [TEAM_GUIDE.md](TEAM_GUIDE.md) for how to extend it, and
[docs/demo_script.md](docs/demo_script.md) for the seven-minute walkthrough.

## Extraction quality

`python -m voc qa` prints the metrics and stores them in the index, where the UI and every answer footnote
read them:

| Metric | What it means |
|---|---|
| `reason_agreement` | how often the extracted primary reason is one of the reasons the category the customer themselves picked on the complaint form can plausibly stand for (a label the extractor never sees). This is agreement between two different labelling schemes, not accuracy: a vanished deposit filed under "deposits and withdrawals" and read as unauthorised activity is a defensible difference, not an error. The mapping in `voc/taxonomy/cfpb_map.json` lists the plausible set per form category, so treat this as a drift alarm rather than a score. |
| `product_agreement` | how often an extracted product matches the form's product |
| `other_or_unclear_share` | how often the extractor abstained |
| `quote_verify_rate` | share of evidence quotes that are exact substrings of the source text |
| `topics_per_call` | multi-topic coverage, expected between 1.2 and 3.5 |
| `sentiment_histogram` | the distribution; a complaint corpus should be overwhelmingly negative |

`python -m voc qa export-golden` writes a stratified 40-record sample and a review sheet for two people;
`score-golden` turns their verdicts into accuracy numbers.
