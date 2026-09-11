// Call drawer: the full customer text with evidence spans highlighted by their stored offsets.

import { api } from "./api.js";
import { clear, el, esc, label, num, shortDate } from "./format.js";

const drawer = () => document.getElementById("drawer");
const body = () => document.getElementById("drawerBody");

export function closeDrawer() { drawer().hidden = true; }

function highlight(text, spans) {
  // Non-overlapping, ordered spans -> a mix of text nodes and <mark> elements.
  const clean = (spans || [])
    .filter((s) => Number.isInteger(s.char_start) && Number.isInteger(s.char_end) && s.char_end > s.char_start)
    .sort((a, b) => a.char_start - b.char_start);
  const frag = document.createDocumentFragment();
  let cursor = 0;
  for (const span of clean) {
    if (span.char_start < cursor) continue;
    frag.appendChild(document.createTextNode(text.slice(cursor, span.char_start)));
    frag.appendChild(el("mark", { text: text.slice(span.char_start, span.char_end),
                                 title: span.match_kind ? `match: ${span.match_kind}` : "verified quote" }));
    cursor = span.char_end;
  }
  frag.appendChild(document.createTextNode(text.slice(cursor)));
  return frag;
}

function transcriptBubbles(text) {
  const wrap = el("div");
  for (const line of text.split("\n")) {
    const m = /^(CUSTOMER|AGENT):\s?(.*)$/.exec(line);
    if (!m) { if (line.trim()) wrap.appendChild(el("p", { text: line })); continue; }
    wrap.appendChild(el("div", { class: `bubble ${m[1].toLowerCase()}`, text: m[2] }));
  }
  return wrap;
}

function kv(rows) {
  return el("table", { class: "kv" }, rows.filter(Boolean).map(([k, v]) =>
    el("tr", {}, [el("td", { text: k }), el("td", { text: v === null || v === undefined || v === "" ? "-" : String(v) })])));
}

function topicBlock(topic) {
  const tone = topic.sentiment < 0 ? "neg" : topic.sentiment > 0 ? "pos" : "";
  return el("div", { class: "row" }, [
    el("div", { class: "row-head" }, [
      el("span", { class: "row-name", text: topic.topic_label || topic.issue_statement }),
      el("span", { class: "row-meta", text: `sentiment ${topic.sentiment > 0 ? "+" : ""}${topic.sentiment}` }),
    ]),
    el("p", { class: "quote", text: topic.issue_statement }),
    el("div", {}, [
      el("span", { class: "chip", text: label(topic.driver_category) }),
      topic.product ? el("span", { class: "chip", text: label(topic.product) }) : null,
      topic.outcome ? el("span", { class: "chip", text: `outcome: ${topic.outcome}` }) : null,
    ]),
    topic.driver ? el("p", { class: "muted", text: `Driver: ${topic.driver}` }) : null,
    el("div", { class: `bar ${tone}` }, [el("span", { style: `width:${Math.abs(topic.sentiment) * 50}%` })]),
  ]);
}

export async function openCall(callId, focusQuote = null) {
  const node = drawer();
  node.hidden = false;
  clear(body()).appendChild(el("p", { class: "muted", text: `loading ${callId}…` }));
  let payload;
  try {
    payload = await api.call(callId);
  } catch (err) {
    clear(body()).appendChild(el("p", { class: "muted", text: `could not load ${callId}: ${err.message}` }));
    return;
  }
  const d = payload.data || {};
  const extraction = d.extraction || {};
  const spans = (d.evidence || extraction.evidence || []).slice();
  if (!spans.length) {
    for (const t of extraction.topics || []) for (const e of t.evidence || []) if (e.verified) spans.push(e);
  }
  for (const pm of extraction.positive_moments || []) if (pm.verified) spans.push(pm);

  const out = clear(body());
  out.appendChild(el("h2", { text: `${d.call_id || callId}` }));
  out.appendChild(el("p", { class: "muted", text: `${shortDate(d.date)} · ${label(d.product)} · ${d.region || "?"} · ${label(d.segment || "none")}` }));

  const textNode = el("div", { class: "calltext" });
  if (d.shape === "transcript") textNode.appendChild(transcriptBubbles(d.text || ""));
  else textNode.appendChild(highlight(d.text || "", spans));
  out.appendChild(textNode);

  if (focusQuote) {
    const marks = textNode.querySelectorAll("mark");
    for (const m of marks) if (m.textContent.includes(focusQuote.slice(0, 40))) { m.scrollIntoView({ block: "center" }); break; }
  }

  out.appendChild(el("h3", { text: "What the system extracted" }));
  out.appendChild(kv([
    ["Contact reasons", (extraction.contact_reasons || []).map((r) => `${label(r.reason)}${r.is_primary ? " (primary)" : ""}`).join(", ")],
    ["Specific reason", (extraction.contact_reasons || []).find((r) => r.is_primary)?.specific_reason],
    ["Products", (extraction.products || []).map(label).join(", ")],
    ["Services", (extraction.services || []).map(label).join(", ")],
    ["Customer asks for", label(extraction.customer_ask)],
    ["Stated reason", extraction.stated_reason],
    ["Underlying driver", extraction.underlying_driver],
    extraction.reason_differs ? ["Stated vs underlying", "they differ"] : null,
    ["Resolution", label(extraction.resolution_status)],
    ["Overall sentiment", extraction.overall_sentiment],
  ]));

  for (const topic of extraction.topics || []) out.appendChild(topicBlock(topic));

  if ((extraction.positive_moments || []).length) {
    out.appendChild(el("h3", { text: "Positive moments" }));
    for (const pm of extraction.positive_moments) {
      out.appendChild(el("div", { class: "row" }, [
        el("span", { class: "chip", text: label(pm.category) }),
        el("p", { class: "quote", text: `"${pm.quote}"` }),
      ]));
    }
  }

  if ((d.themes || []).length) {
    out.appendChild(el("h3", { text: "Themes" }));
    out.appendChild(el("div", {}, d.themes.map((t) =>
      el("span", { class: "chip", text: t.name || t.theme_id }))));
  }

  out.appendChild(el("h3", { text: "Metadata" }));
  out.appendChild(kv([
    ["Date received", shortDate(d.date)],
    ["Week", d.week], ["Month", d.month],
    ["Channel", label(d.channel)], ["Region", `${d.region || "?"} (${label(d.region_group)})`],
    ["Segment", label(d.segment)], ["Company", d.company],
    ["Sampling fraction", d.sampling_fraction],
  ]));
  out.appendChild(el("p", { class: "footnote", text:
    `For contrast, the category this customer picked on the complaint form: ${d.product_raw || "?"} / ${d.issue_raw || "?"}` +
    (d.sub_issue_raw ? ` / ${d.sub_issue_raw}` : "") + ". That label never reaches the extraction prompt." }));
}

export function initDrawer() {
  document.getElementById("drawerClose").addEventListener("click", closeDrawer);
  drawer().addEventListener("click", (e) => { if (e.target === drawer()) closeDrawer(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeDrawer(); });
}

/** A list of calls behind a number, opened from any "n calls" link. */
export async function openCallList(resultId, title = "Calls behind this number") {
  const node = drawer();
  node.hidden = false;
  clear(body()).appendChild(el("p", { class: "muted", text: "loading calls…" }));
  let payload;
  try {
    payload = await api.resultRows(resultId);
  } catch (err) {
    clear(body()).appendChild(el("p", { class: "muted", text: `could not load: ${err.message}` }));
    return;
  }
  const out = clear(body());
  out.appendChild(el("h2", { text: title }));
  out.appendChild(el("p", { class: "muted", text:
    `${num(payload.n_call_ids)} calls · re-executed from the stored query${payload.matches_stored === false ? " (result changed since it was stored)" : ""}` }));
  for (const row of payload.rows || []) {
    out.appendChild(el("div", { class: "row" }, [
      el("div", { class: "row-head" }, [
        el("button", { class: "linkish", text: row.call_id, onclick: () => openCall(row.call_id) }),
        el("span", { class: "row-meta", text: `${shortDate(row.date)} · ${label(row.product)}` }),
      ]),
      row.summary ? el("p", { class: "quote", text: row.summary }) : null,
    ]));
  }
  if (payload.sql?.length) {
    out.appendChild(el("details", { class: "devonly" }, [
      el("summary", { text: "SQL" }),
      el("pre", { text: payload.sql.map((s) => `${s.sql}\n-- params: ${JSON.stringify(s.params)}`).join("\n\n") }),
    ]));
  }
}
