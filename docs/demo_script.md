# Demo script

Seven minutes, the eight questions from the briefing, every number clickable. Run `python -m voc serve`
and open the dashboard before you start. Keep `?dev=1` off until the last minute.

The through-line: **the agent proposes, the server checks, and every claim is a list of real calls you can
open.**

---

## 0:00 – 0:30 Hook

Open **About this data**.

> "These are 4,425 real complaints one bank received over 24 months. Public regulator data. We sample a
> constant 25% of that bank's complaints every month with a fixed seed, so the trends you are about to see
> are the real shape of the intake, not a curated sample. The `XXXX` you will see in the quotes are the
> regulator's redactions. Nobody has read all of these. Our agents have, one by one."

Point at the pipeline strip: calls, topics, themes, and the quality line.

> "Each contact was read into reasons, topics, a sentiment per topic, the specific driver, and verbatim
> evidence. 99% of the quotes we show verify as exact substrings of what the customer actually wrote."

## 0:30 – 1:15 Q1 · What are customers contacting us about most, and what is changing?

Click the first chip. Let the trace stream.

> "It decides what to pull, runs the query, and answers with counts and shares."

Read the headline. Click the **n calls** link on the headline claim: the call list opens.

> "The label comes from a small taxonomy so we can count. The sentence under it comes from the customer's
> own words so we can act. `Pricing complaint` is a tag. `The monthly fee went up at renewal and nobody
> explained why` is something a product team can fix."

## 1:15 – 2:30 Q2 · What are the main causes of negative sentiment, and what specifically triggers them?

Click the chip. When the answer lands, read one specific driver out loud, then click a quote to open the
call drawer.

> "Here is the whole contact. The quote is highlighted where it actually occurs. On the right is everything
> the system extracted: the reasons, the topics with their own sentiment, the driver."

Scroll to the bottom of the drawer.

> "And here is the category this customer picked on the complaint form. We never show that label to the
> extractor. It stays clean as a check: the two agree about three quarters of the time, and where they
> differ it is usually because the customer's own words say something more specific than the dropdown."

Point at the stated reason versus underlying driver.

> "What they asked for, and what actually drove the contact. Worth being straight about this one: in
> written complaints the two usually match, because someone writing to a regulator leads with the real
> grievance. It splits in 55 of the 4,425 here, about one contact in eighty. On phone calls, where people open with
> what they want, we would expect it far more often, and the extraction already captures it."

Pick one of the calls where they do differ before the demo so you can show a real example rather than
hunting for one live. `voc tool search_calls` will not find them; this will:

```bash
python -c "import json;[print(r['call_id'],'|',json.loads(l)['extraction']['stated_reason'][:60]) for l in open('data/extractions.jsonl',encoding='utf-8') if (r:=json.loads(l)).get('status')=='ok' and r['extraction'].get('reason_differs')][:5]"
```

## 2:30 – 3:30 Q5 · Are customers describing the same underlying problem in different ways?

This is the strongest moment in the demo. From that answer, click the top theme name. The card opens:
*Fraud dispute denied without reviewing the evidence*, 394 calls, 397 wordings, 6 products.

> "Three hundred and ninety-four contacts. Three hundred and ninety-seven different ways of saying it.
> Effectively no two customers used the same words."

Expand the wordings list and read three that share no vocabulary at all: a stolen card used at festival
stalls with no cameras, a timeshare company given eighteen months, a document upload page that only
reopened after the weekend.

> "No keyword rule finds those three together. There is no shared phrase to search for. And the ratio
> holds all the way down the top ten: 397 wordings over 394 contacts at the top, 99 over 97 at the tenth."

Then the consequence, which is the part a bank cares about:

> "It spans six products and forty-one states, so every product owner and every regional queue sees a
> handful of unrelated-looking cases instead of the one 394-contact failure they are all part of."

If the theme has merge history, point at it.

> "These two were separate themes until the consolidation pass judged them the same cause. The membership
> is never deleted, so you can always see what was merged and why."

## 3:30 – 4:45 Q4 · Which issues are growing fastest, and are any of them new?

Click the chip. Read the emerging panel.

> "Four weeks against the sixteen before. This one has N calls where the baseline predicts E. Here is the z
> score, the number of distinct weeks, when we first saw it, and whether it still holds at eight weeks."

Point at the footer line.

> "And here is how many of the themes we tested could pass this threshold by chance. We tell you the error
> rate rather than hiding it."

At the latest week exactly one theme clears the bar, and saying so is part of the point.

> "One theme clears it today. A detector that fires every week is a detector nobody reads."

Now the replay, which is the real moment. Set the **as-of slider** to **2025-W38** and step forward a week
at a time. Watch *Claim investigation runs past its deadline with no status*:

| As-of week | Recent calls | Expected | z | Status |
|---|---|---|---|---|
| 2025-W38 | 1 | 3.2 | -1.14 | nothing |
| 2025-W40 | 6 | 1.9 | 2.63 | **emerging** |
| 2025-W42 | 9 | 2.1 | 4.33 | growing |
| 2025-W45 | 7 | 3.3 | 1.86 | settled |

> "Quiet, quiet, then six calls against two expected and it fires. By the time it is nine calls a monthly
> report would still be a month away. Nothing here is planted: these scores are precomputed for every week
> in the window, so this is genuinely what the system would have told you that Monday."

## 4:45 – 5:20 Q3 · Which experiences create satisfaction, what should we protect?

Click the chip. Let the caveat be the point.

> "This is a complaints corpus, so the honest answer is not a satisfaction score. Ranking positive themes
> returns nothing at all. What it can show is the 421 contacts that carry a moment which went right:
> helpful staff in 169, a fair outcome in 124, a fast resolution in 102. The system says what its evidence
> can and cannot bear, and it says it without being asked."

## 5:20 – 5:50 Q6 · How do pain points differ by product, segment or region?

Ask it, or open a theme card and switch to the breakdown tabs.

> "Share, and lift against the overall rate. Customers on this product mention it at 2.1 times the rate."

Point at a blanked cell.

> "And this one is below minimum support, so it is not ranked and not shown. Fifty calls in the slice, five
> in the cell. We would rather show a gap than a number nobody should act on."

## 5:50 – 6:20 Q7 and Q8 · Which statements support that, and what did those customers say?

Type a follow-up, or click one of the suggested chips.

> "Broad pattern. N calls, across M months and P products. That badge is not the model's opinion. The
> server recounted it from the call ids before it was rendered."

Open two quotes.

Now turn on **dev mode** (`?dev=1`) and open the validation report.

> "This is the part I would want to see as a bank. The model proposes a claim; the server re-executes the
> query, recounts the calls, checks every number against the tool result it cites, and drops any quote that
> is not verified evidence. If it cannot support a claim, it greys it out and puts the real number beside
> it rather than deleting it quietly."

## 6:20 – 7:00 Close

Point at the mode badge.

> "Today's answers replay real runs through these same tools, re-verified on the way out. With an API key
> it runs live against the same tools, and the code is the same either way."

> "One command to run. The pipeline re-runs on tomorrow's contacts for the price of the new ones only,
> because every call is cached by content. Minutes instead of weeks; the small signal while it is still
> small; causes in the customer's own words; and every number on this screen is a list of calls you can
> open and read."

---

## If something goes wrong

| Problem | What to do |
|---|---|
| A question hangs | It falls back to a templated answer after 90 seconds, badged as such. Keep talking; it will land. |
| An unscripted question from the audience | Ask it. Without a key it answers from the same tools with a "templated (no model)" badge. Say so. |
| The dashboard looks empty | A filter is probably still set. Click **Clear**. |
| The trend chart is blank | Only themes above minimum support are plotted; widen the filters. |

## Before you present

```bash
python -m voc build-db && python -m voc qa && pytest
python -m voc serve
```

Check the mode badge does not say FAKE DATA, walk the eight chips once, and leave the as-of slider at the
latest week. All eight replay from recordings, each one about two seconds, so none of them needs a key.

Numbers as of the current index, in case a slide needs them:

| | |
|---|---|
| Contacts read | 4,425 over 24 months, 5,827 topics |
| Themes | 128 active, 154 counted, 1,478 distinct wordings |
| Largest theme | fraud dispute denied without reviewing the evidence, 394 contacts, 397 wordings |
| Grouping agreement | 0.881 on a 563-statement re-judgement |
| Quotes verifying | 99.7% |
