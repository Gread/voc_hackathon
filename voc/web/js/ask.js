// Ask panel: streams the trace, then renders the verified answer with badges, quotes and charts.

import { askStream, api } from "./api.js";
import { openCall, openCallList } from "./calldrawer.js";
import { openTheme } from "./themecard.js";
import { badge, clear, el, esc, label, markdown, num } from "./format.js";
import { queryParams, state } from "./state.js";
import { barsChart, trendChart } from "./charts.js";

let busy = false;
let controller = null;
let chartSeq = 0;

const out = () => document.getElementById("askOutput");

function traceBox() {
  return el("div", { class: "trace", id: "askTrace" });
}

function renderChart(chart, results) {
  const source = results[chart.result_id];
  if (!source) return null;
  const rows = source.rows || [];
  const id = `askChart${++chartSeq}`;
  const wrap = el("div", { style: "height:190px;margin:8px 0" }, [el("canvas", { id, height: "150" })]);
  setTimeout(() => {
    if (chart.kind === "trend") {
      const series = rows.map((r) => ({
        label: r.name || r.entity_id || chart.series_key,
        points: (r.series || r.points || []).map((p) => ({ period: p.period, share: p.share, n_calls: p.n_calls })),
      })).filter((s) => s.points.length);
      if (series.length) trendChart(id, series, { valueKey: "share" });
    } else {
      const bars = rows.slice(0, 8).map((r) => ({
        label: label(r.name || r.label || r.value || r.key || r.reason || ""),
        value: Number(r.n_calls ?? r.n_recent ?? r.n ?? 0),
      })).filter((b) => b.label);
      if (bars.length) barsChart(id, bars);
    }
  }, 0);
  return el("div", {}, [el("p", { class: "row-meta", text: chart.title || "" }), wrap]);
}

function renderAnswer(answer, results) {
  const node = clear(out());
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
      unverified ? el("p", { class: "correction", text: "not supported by retrieved data" }) : null,
      ...(claim.corrections || []).map((c) =>
        el("p", { class: "correction", text: `${c.field}: the model said ${c.model}, the server counted ${c.server}` })),
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
  const deltaNode = el("div", { class: "answer-md" });

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
      else if (name === "tool_call") addTrace(`→ ${payload.name}(${JSON.stringify(payload.args ?? {}).slice(0, 110)})`);
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
        renderAnswer({ ...payload.answer, question }, results);
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
  for (const q of questions || []) {
    chips.appendChild(el("button", { type: "button", text: q.question, title: q.question, onclick: () => ask(q.question) }));
  }
}
