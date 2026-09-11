# Build log

What was built, what was decided and why, what real data showed, and what is left. Written for the
hackathon team picking this up. The design itself is in [DESIGN.md](DESIGN.md); this is the record of
building it.

## Where it stands

| | |
|---|---|
| Pipeline stages | all twelve command stages work, no stubs |
| Tests | 103 passing, no network and no API key needed |
| CI | suite plus an end-to-end smoke on Python 3.11 and 3.13 |
| Corpus | 4,425 real complaints, 24 months, one bank |
| Step 1, read every call | **complete** - 4,425 of 4,425, zero errors |
| Step 2, group into themes | in progress - two of roughly five waves |
| Step 3, trends and emerging | working, verified against planted patterns |
| Step 4, plain-language answers | working, verified for all eight questions |
| Step 5, evidence and confidence | working, verified including refusal to support a bad claim |
| Code | ~9,400 lines Python, ~1,200 JavaScript, ~1,500 test |

## Decisions taken, and why

**Real data, not synthetic.** The corpus is consumer complaint narratives about one large US bank, pulled
live from the regulator's public database. Sampling is a constant 25.25% of eligible complaints per month
with a fixed seed, so month-to-month movement is the real shape of the intake rather than an artefact of
how we sampled. Nothing in `data/` is synthetic; the only planted patterns live in `tests/fixtures`, where
the analytics are checked against known answers.

**One bank, 24 months.** A single company matches the briefing (a bank's own contact centre) and avoids
company-mix confounding. 24 months gives weekly trend detection real baselines.

**4,425 records, chosen by a gate not a guess.** The number comes from a support gate: at least 30 sampled
calls in at least 90% of ISO weeks, at least two products and two segments with real volume, every month
present. At the original target of 4,000 the gate failed on weekly support (86% of weeks). 4,425 passes at
92%. The gate is in `voc ingest profile` and prints its own verdict.

**The complaint form's own labels never reach the extractor.** The regulator's product and issue fields are
kept as dimensions and as a free quality metric, but are deliberately withheld from the reading prompt.
Feeding them in would bias the extracted reasons toward the form's dropdown, which is exactly the failure
the briefing describes, and would destroy the only free measure of extraction quality we have.

**The server recomputes every number before it is shown.** The model proposes claims; `voc/agent/answer.py`
re-queries the call ids, recounts them, checks every quoted figure against the tool result it cites, and
drops quotes that are not verified evidence. Claims it cannot support are rendered greyed with the server's
real number beside them rather than quietly deleted.

**Agents did the reading, because there is no API key here.** Every LLM stage can run through the Claude
API or through build-time agents writing the same cache files. All 4,425 contacts were read by agents. The
pipeline does not care which; `produced_by` records it, and a fake-produced index is refused unless
`VOC_LLM=fake`, in which case the interface shows a red warning.

## What the real data showed

**Genuine emerging signals exist, so nothing needed planting.** Across the window, themes and reasons reach
z-scores up to 5.9 against their own 16-week baselines. The as-of slider replays a real theme climbing from
absent, to 34 calls against 6.6 expected, to 82 against 30.4.

**The extracted causes are actionable, not tags.** By volume the leading drivers of dissatisfaction are
refusals without explanation, fraud not stopped or refunded, and money held or not returned. The theme
names the agents produced read like work items: *an overdraft fee charged although the deposit already
showed as available*; *a fraud claim denied by citing the PIN or chip as proof it was authorised*; *branch
and phone support each redirect to the other*. None of those exist as options on a complaint form.

**Grouping converges.** By the second wave, 67% of statements joined a theme that already existed rather
than needing a new one, and two whole categories needed no new themes at all. That is "many complaints
become one problem" measured rather than asserted.

**Satisfaction has to come from positive moments.** On a complaint corpus almost no topic carries positive
sentiment, so ranking positive topics returns nothing. 292 verified positive moments do exist inside these
complaints, across helpful staff, fair outcomes, fast resolution and clear communication. The answer is
built from those and labelled honestly as positive moments inside complaints.

**One briefing expectation does not hold here, and that is worth saying out loud.** The briefing expects
the stated reason ("I want to cancel") to differ often from the real driver. In this corpus it differs in
about 1 contact in 75. The reading is not at fault: where it splits, it splits well. It looks like a
property of the medium, since someone writing a formal complaint leads with the grievance while someone
phoning opens with what they want. On real call transcripts it should be far more common, and the
capability is built and working. Do not oversell this moment on stage.

## Quality of the reading

Measured over all 4,425 contacts:

| Measure | Value | Note |
|---|---|---|
| Evidence quotes verifying as exact substrings | 99.7% | anything else never reaches the interface |
| Validation errors | 0 | |
| Abstained rather than guessed | 1.3% | |
| Agreement with the customer's own form category | 0.69 | agreement between two labelling schemes, not accuracy |
| Topics per contact | 1.32 | 29% of contacts carry more than one topic |
| Negative sentiment | 97.2% | as expected for a complaint corpus |

The agreement figure deserves care. It compares our contact reasons against the category the customer
picked on the form, which the extractor never sees. Disagreements are usually defensible differences, such
as a vanished deposit filed under "deposits and withdrawals" and read as unauthorised activity. Treat it as
a drift alarm, not a score.

## Bugs found and fixed

Most of these only appeared against real data or by clicking through the interface. They are listed because
each one would have shown up on stage.

**Theme ids shifted between runs.** Ids came from one global counter in bucket order, so a theme created in
one category renumbered another category's themes. This invalidated completed grouping work, so the pass
could never converge, and worse, an assignment written against id 13 could later bind to a different theme.
Ids are now scoped to their own category. Cost: one wave of grouping had to be redone.

**The satisfaction question returned nothing.** Positive topics never clear minimum support on a complaint
corpus, so the panel and the answer were empty despite 292 verified positive moments. Both now read the
moments, and the query records their call ids so the claim can actually be recounted; it verifies as a
broad pattern over 288 calls instead of "not supported by retrieved data".

**The as-of week could be a partial trailing week.** The corpus ends mid-week, putting a half-empty week
inside the four-week recent window and suppressing every emerging signal. Using the latest complete week
surfaced real growing signals that had been hidden.

**Percentages were wrong for small values.** The formatter guessed whether a number was a fraction or a
percentage, so 16 of 4,425 rendered as 40.0% instead of 0.4%. Split into two explicit helpers.

**Editing a JavaScript file did nothing.** The browser cached modules, so a refresh served the old copy and
the page died on a missing export, while the README promised "no build step, just refresh". Static files
now ask the browser to revalidate.

**The call drawer showed no quotes and "? / ?" for the form label.** It read the payload at the wrong
nesting level. This is the heart of the evidence moment. A test now pins the shape and checks that every
verified quote's offsets point at that quote in the stored text.

**A link promised more than it delivered.** "4,425 calls in scope" opened a list of 2,980, because a result
covers the calls carrying a reason. The label now names the result's own count and explains the gap.

**32 narratives arrived as Python bytes representations**, some truncated mid-string, showing literal escape
characters instead of line breaks. Decoded on ingest, while genuinely ambiguous text such as a customer
writing "b'cause" is left exactly as written.

**A stale cache entry was reported as an error** when it is simply work to redo after a prompt, taxonomy or
text change. It now reads as stale and is re-queued.

**A finished index rebuild could not replace a database held open by the server**, reporting a bare Windows
file error and leaving a 44MB temp file. It now names the cause, says to stop the server, confirms the old
index is still usable, and cleans up.

**Near-miss values were discarded.** A customer saying a problem is partly fixed now reads as unresolved
rather than unknown, with the substitution flagged.

## What was verified, and how

Not "it compiles" but "it does the thing":

- **Emerging detection** against a seeded fixture with planted patterns: a ramping theme is flagged, a
  brand-new one is flagged as new, a flat one is not flagged, a fading one is not, and a regional
  concentration shows lift 2.77 with small cells suppressed.
- **The as-of replay** stepping back through real weeks and watching a theme climb.
- **Every screen** in a real browser against real data: reasons, negative drivers, satisfaction, emerging,
  trend chart, theme card with its wordings list and breakdown tabs, call drawer with quotes highlighted by
  stored offsets, and the Ask panel.
- **Every interactive path** the demo uses, including the drill-down from a claim to its calls.
- **The verifier**, including that it recounts a model's inflated number, drops an unverifiable quote,
  flags a figure that appears in no tool result, and greys out a claim citing nothing.
- **The recorded-answer round trip**, which is how the demo runs without an API key: drive the real tools,
  finalize through the same verifier a live answer uses, replay in about two seconds with the trace
  visible, match a differently-worded question to the recording, and refuse to store an answer that cites
  nothing.
- **The fresh-clone path**: with no database present, the server rebuilds the index from committed files
  and serves.

## What is left

1. **Finish theme grouping.** Roughly three more waves of the export-fill-import cycle, then consolidation
   of near-duplicate themes and a re-assignment pass against the frozen registry, then a stability check.
   Commands are in the README; the cycle is described in TEAM_GUIDE.
2. **Rebuild the index** (`voc build-db`) so themes reach the interface.
3. **Record the eight demo answers** (`voc record-answer`), so the demo replays instantly offline.
4. **Rehearse** against `docs/demo_script.md`.

With an API key in `.env`, steps 1 and 3 run unattended (`voc theme run`, `voc warm-answers`) instead of
through agents.

## Things to know before changing anything

- Files under `data/` are the truth; the SQLite index is derived and rebuilt in about two seconds.
- Every model call is cached by content hash, so re-running a stage costs nothing and a killed run resumes.
- Changing `taxonomy.json` bumps a version that is part of every extraction cache key, which re-reads the
  corpus on purpose.
- Quotes must be exact substrings. The verifier accepts an exact or whitespace-normalised match and nothing
  else; unverified quotes never reach the interface, a tool result or the agent.
- The counting unit is the contact. A theme, reason or driver counts at most once per contact, and every
  share is over the contacts in the same filtered slice.
- Minimum support is deliberate: nothing is ranked below five contacts, and a segment cell is blanked below
  fifty in the slice. Do not relax it to make a chart look fuller.
