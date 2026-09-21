// Ask panel: streams the trace, then renders the verified answer with badges, quotes and charts.

import { askStream, api } from "./api.js";
import { openCall, openCallList } from "./calldrawer.js";
import { openTheme } from "./themecard.js";
import { badge, clear, el, esc, label, markdown, num, plural } from "./format.js";
import { queryParams, state } from "./state.js";
import { barsChart, trendChart } from "./charts.js";

let busy = false;
let controller = null;
let chartSeq = 0;

const out = () => document.getElementById("askOutput");

function traceBox() {
  return el("div", { class: "trace", id: "askTrace" });
}

// The tool name is the system's own vocabulary. A judge reading the trace over someone's shoulder
// should see what was checked, not the function that checked it.
const TOOL_LABELS = {
  get_overview: "Read the overview numbers", contact_reasons: "Checked contact reasons",
  list_themes: "Listed themes", theme_detail: "Looked at a theme in detail",
  theme_trend: "Checked a theme's trend over time", emerging_themes: "Checked what's emerging",
  sentiment_drivers: "Checked what drives sentiment", breakdown: "Broke the numbers down",
  compare: "Compared two groups", get_quotes: "Pulled supporting quotes",
  search_calls: "Searched the calls", get_call: "Opened one call", submit_answer: "Wrote the answer",
};
const toolLabel = (name) => TOOL_LABELS[name] || label(name || "tool");

/** A verification result as a Carbon inline notification rather than a bare tinted paragraph: the
 *  server correcting the model's own number is the product's whole argument, and it should look
 *  like a deliberate system message, not a styling accident. Falls back to the old paragraph if
 *  the vendored component isn't there. */
function notice(kind, title, body) {
  if (!window.customElements?.get("cds-inline-notification")) {
    return el("p", { class: kind === "error" ? "correction" : "caveat", text: `${title}: ${body}` });
  }
  return el("cds-inline-notification", {
    kind, title, subtitle: body, "hide-close-button": "", "low-contrast": "",
    style: "margin:8px 0; max-width:none",
  });
}

/** Decide what can honestly be drawn BEFORE reserving space for it.
 *
 *  This used to append the box first and fill it inside a setTimeout, which meant that whenever the
 *  data didn't support a chart the answer was left with an empty 190px rectangle under it - two of
 *  them, on the first demo question. /api/results/{id}/rows answers with the calls behind a result
 *  (Q.call_list, capped at 200), not the tool's own aggregate rows, so a trend's per-period series
 *  simply isn't in there to plot. Drawing one anyway from a capped sample of calls would be a chart
 *  that lies, which is the one thing this product exists not to do, so it draws only what the rows
 *  actually carry and renders nothing at all otherwise. */
function renderChart(chart, results) {
  const source = results[chart.result_id];
  if (!source) return null;
  const rows = source.rows || [];

  let draw = null;
  if (chart.kind === "trend") {
    const series = rows.map((r) => ({
      label: r.name || r.entity_id || chart.series_key,
      points: (r.series || r.points || []).map((p) => ({ period: p.period, share: p.share, n_calls: p.n_calls })),
    })).filter((s) => s.points.length);
    if (series.length) draw = (id) => trendChart(id, series, { valueKey: "share" });
  } else {
    const bars = rows.slice(0, 8).map((r) => ({
      label: label(r.name || r.label || r.value || r.key || r.reason || ""),
      value: Number(r.n_calls ?? r.n_recent ?? r.n ?? 0),
    })).filter((b) => b.label && b.value > 0);
    if (bars.length) draw = (id) => barsChart(id, bars);
  }
  if (!draw) return null;

  const id = `askChart${++chartSeq}`;
  // .chart-box, not a one-off inline height: an answer's chart is the same box the dashboard's
  // panels use, and it had drifted from it.
  const wrap = el("div", { class: "chart-box", style: "margin:8px 0" }, [el("canvas", { id })]);
  setTimeout(() => draw(id), 0);
  return el("div", {}, [el("p", { class: "row-meta", text: chart.title || "" }), wrap]);
}

function renderAnswer(answer, results, trace, toolCalls) {
  const node = clear(out());
  if (trace) {
    // Collapsed, not gone: how the answer was reached stays one click away instead of
    // disappearing the moment the answer itself is ready to read.
    node.appendChild(el("details", { class: "trace-summary" }, [
      el("summary", { text: `How this answer was reached · ${plural(toolCalls, "tool call")}` }),
      trace,
    ]));
  }
  const modeText = answer.mode === "recorded"
    ? `recorded run${answer.recorded_question && answer.recorded_question !== answer.question ? ` · matched to "${answer.recorded_question}"` : ""}`
    : answer.mode === "templated" ? "templated (no model)" : `live · ${answer.model || ""}`;
  node.appendChild(el("p", {}, [
    el("span", { class: "mode", text: modeText }), document.createTextNode(" "), badge(answer.confidence),
  ]));

  node.appendChild(el("div", { class: "answer-md", html: markdown(answer.answer_markdown || "") }));

  for (const claim of answer.claims || []) {
    const unverified = claim.verified === false;
    const card = el("div", { class: `claim${claim.headline ? " headline" : ""}${unverified ? " unverified" : ""}` }, [
      el("div", { class: "statement" }, [
        el("span", { class: "marker", text: `[${claim.id}] ` }),
        document.createTextNode(claim.statement || ""),
      ]),
      el("div", {}, [
        badge(claim.confidence),
        claim.verified_n ? document.createTextNode(" ") : null,
        claim.verified_n && claim.result_ids?.length
          ? el("button", { class: "linkish", text: `${num(claim.verified_n)} calls`,
                           onclick: () => openCallList(claim.result_ids[0], claim.statement?.slice(0, 60) || "Calls",
                                                       answer.result_qhash) })
          : null,
        ...(claim.theme_ids || []).map((t) =>
          el("button", { class: "linkish", text: " theme", onclick: () => openTheme(t) })),
      ]),
      unverified ? notice("error", "Not confirmed",
                          "This couldn't be confirmed in the actual calls, so it isn't counted.") : null,
      ...(claim.corrections || []).map((c) =>
        notice("info", "Corrected",
               `This first said ${num(c.model)}. The real number, recounted from the calls, is ${num(c.server)}.`)),
      state.dev && claim.model_n !== claim.verified_n
        ? el("p", { class: "devonly footnote", text: `model_n ${claim.model_n} · server_n ${claim.verified_n}` }) : null,
    ]);
    node.appendChild(card);
  }

  for (const chart of answer.charts || []) {
    const rendered = renderChart(chart, results);
    if (rendered) node.appendChild(rendered);
  }

  if ((answer.quotes || []).length) {
    node.appendChild(el("h3", { text: "In the customers' own words" }));
    for (const q of answer.quotes) {
      node.appendChild(el("p", { class: "quote" }, [
        el("button", { class: "linkish", text: `"${q.quote}"`, onclick: () => openCall(q.call_id, q.quote) }),
        el("span", { class: "row-meta", text: ` ${q.call_id}` }),
      ]));
    }
  }

  for (const caveat of answer.caveats || []) node.appendChild(el("p", { class: "caveat", text: `Caveat: ${caveat}` }));
  if (answer.coverage_line) node.appendChild(el("p", { class: "footnote", text: answer.coverage_line }));
  if (answer.footnote) node.appendChild(el("p", { class: "footnote", text: answer.footnote }));

  if ((answer.followups || []).length) {
    const chips = el("div", { class: "chips" });
    for (const f of answer.followups) chips.appendChild(el("button", { type: "button", text: f, onclick: () => ask(f) }));
    node.appendChild(chips);
  }

  if (state.dev) {
    node.appendChild(el("details", { class: "devonly" }, [
      el("summary", { text: "validation report" }),
      el("pre", { text: JSON.stringify(answer.validation || {}, null, 1) }),
    ]));
  }
}

export async function ask(question, { fresh = false } = {}) {
  if (busy) { controller?.abort(); }
  busy = true;
  chartSeq = 0;
  document.getElementById("askBtn").disabled = true;
  document.getElementById("askInput").value = question;
  const node = clear(out());
  const trace = traceBox();
  node.appendChild(trace);
  const results = {};
  let answered = false;
  let toolCalls = 0;
  const deltaNode = el("div", { class: "answer-md" });
  const status = document.getElementById("askStatus");
  if (status) status.textContent = "Reading your question…";

  const addTrace = (text, extra = null) => {
    const line = el("div", { text });
    if (extra) line.appendChild(extra);
    trace.appendChild(line);
    trace.scrollTop = trace.scrollHeight;
  };

  controller = new AbortController();
  let answerQhash = null;   // result ids restart at r1 per question
  try {
    await askStream({ question, filters: queryParams(), as_of: state.asOf || null, fresh }, (name, payload) => {
      if (name === "status") { if (payload.qhash) answerQhash = payload.qhash; addTrace(`· ${payload.text ?? ""}`); }
      else if (name === "thinking") addTrace(`· thinking: ${(payload.text ?? "").slice(0, 120)}`);
      else if (name === "tool_call") {
        toolCalls++;
        // The tool's own arguments are debugging detail, not something a demo audience reads -
        // shown only in ?dev=1, same rule the validation report and model/server diffs already use.
        addTrace(`→ ${toolLabel(payload.name)}`,
                 state.dev ? el("pre", { text: JSON.stringify(payload.args ?? {}, null, 1) }) : null);
      }
      else if (name === "tool_result") {
        results[payload.result_id] = { rows: [] };
        const details = el("details", {}, [
          el("summary", { text: `   ${payload.result_id}: ${payload.summary ?? ""}` }),
          el("pre", { text: (payload.sql || []).map((s) => s.sql).join("\n\n") || "no sql" }),
        ]);
        trace.appendChild(details);
        if (payload.result_id) {
          api.resultRows(payload.result_id, answerQhash).then((r) => { results[payload.result_id] = r; }).catch(() => {});
        }
      } else if (name === "answer_delta") {
        if (!node.contains(deltaNode)) node.appendChild(deltaNode);
        deltaNode.innerHTML = markdown((deltaNode.dataset.text = (deltaNode.dataset.text || "") + payload.text));
      } else if (name === "answer") {
        answered = true;
        answerQhash = payload.answer?.result_qhash || answerQhash;
        renderAnswer({ ...payload.answer, question }, results, trace, toolCalls);
        if (status) status.textContent = "Answer ready.";
      } else if (name === "error") {
        addTrace(`! ${payload.message ?? "error"}`);
      }
    }, controller.signal);
    if (!answered) node.appendChild(el("p", { class: "muted", text: "the stream ended without an answer" }));
  } catch (err) {
    if (err.name !== "AbortError") node.appendChild(el("p", { class: "muted", text: `ask failed: ${err.message}` }));
  } finally {
    busy = false;
    document.getElementById("askBtn").disabled = false;
  }
}

export function initAsk(questions) {
  const form = document.getElementById("askForm");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = document.getElementById("askInput").value.trim();
    if (q) ask(q);
  });
  const chips = clear(document.getElementById("questionChips"));
  const heading = document.getElementById("questionChipsLabel");
  if (heading) heading.hidden = !(questions || []).length;
  // Each briefing question already carries a short alias in questions/demo.yaml ("Top contact
  // reasons" for "What are customers contacting us about most, and what is changing?"). The card
  // leads with that and keeps the exact briefing wording underneath, so the grid is scannable
  // without paraphrasing the bank's own questions away. No alias means no second line.
  (questions || []).forEach((q, i) => {
    const short = (q.aliases || [])[0] || q.question;
    chips.appendChild(el("button", {
      type: "button", class: "q-card", title: q.question, style: `--i:${i}`,
      onclick: () => ask(q.question),
    }, [
      el("span", { class: "q-label", text: short }),
      short === q.question ? null : el("span", { class: "q-full", text: q.question }),
    ]));
  });
}
