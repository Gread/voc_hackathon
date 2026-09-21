// Composition root: load meta, wire the filters, the as-of slider and the panels.

import { api } from "./js/api.js";
import { initAsk } from "./js/ask.js";
import { initDrawer } from "./js/calldrawer.js";
import { initWeekly } from "./js/weekly.js";
import { initDashboard, renderAll, renderAsOfOnly } from "./js/dashboard.js";
import { initGraph, showGraph } from "./js/graph.js";
import { initNav } from "./js/nav.js";
import { clear, el, esc, label, num, pct } from "./js/format.js";
import { clearFilters, onChange, queryParams, readURL, setAsOf, setFilter, state } from "./js/state.js";
import { initThemeCard } from "./js/themecard.js";

let meta = null;

function fillSelect(id, key, values, labels = label) {
  const select = document.getElementById(id);
  clear(select);
  for (const value of values) {
    const option = el("option", { value, text: labels(value) });
    if ((state.filters[key] || []).includes(value)) option.selected = true;
    select.appendChild(option);
  }
  select.size = Math.min(4, Math.max(2, values.length));
  select.addEventListener("change", () => {
    setFilter(key, [...select.selectedOptions].map((o) => o.value));
  });
}

/** Corpus picker. Two corpora differ in kind, so the choice stays visible and never defaults to a
 *  silent blend: unticking everything shows everything, which is what "no filter" means everywhere
 *  else in this interface. */
function setupSources(sources) {
  const wrap = document.getElementById("sources");
  const boxes = document.getElementById("sourceBoxes");
  if (!sources || sources.length < 2) return;   // one corpus needs no picker
  wrap.hidden = false;
  const all = sources.map((s) => s.source);
  // No filter means every corpus is included, so every box shows ticked. Ticked reads as
  // "included", which is the only mental model that survives ticking the second box.
  const shown = () => (state.filters.source?.length ? state.filters.source : all);

  const render = () => {
    clear(boxes);
    for (const src of sources) {
      const on = shown().includes(src.source);
      const input = el("input", { type: "checkbox" });
      input.checked = on;
      const label = el("label", {
        class: `source-box${on ? " on" : ""}${src.kind === "synthetic" ? " synthetic" : ""}`,
        title: src.note || "",
      }, [
        input,
        el("span", { text: src.label || src.source }),
        src.kind === "synthetic" ? el("span", { class: "tag", text: "synthetic" }) : null,
        el("span", { class: "n", text: num(src.n_calls) }),
      ]);
      input.addEventListener("change", () => {
        const next = input.checked
          ? [...shown(), src.source]
          : shown().filter((v) => v !== src.source);
        // Untick the last one and you would be asking for nothing; that means everything instead.
        // Every box ticked is also everything, so both clear the filter and keep the URL short.
        setFilter("source", next.length === 0 || next.length === sources.length ? [] : next);
        render();
      });
      boxes.appendChild(label);
    }
  };
  render();
  onChange((reason) => { if (reason === "filters") render(); });
}

async function loadFilterOptions() {
  // Options come from the data itself: the breakdown endpoint lists every value with support.
  const dims = [["fProduct", "product"], ["fSegment", "segment"], ["fRegionGroup", "region_group"]];
  for (const [id, dim] of dims) {
    try {
      const payload = await api.breakdown({}, { entity_type: "all", by: dim, min_n: 1 });
      const values = (payload.rows || []).map((r) => r.value).filter(Boolean);
      if (values.length) fillSelect(id, dim, values);
    } catch { /* leave the select empty if the dimension is unavailable */ }
  }
}

function setupAsOf(weeks) {
  const slider = document.getElementById("asOf");
  const output = document.getElementById("asOfLabel");
  if (!weeks.length) { slider.disabled = true; output.textContent = "-"; return; }
  slider.min = "0";
  slider.max = String(weeks.length - 1);
  const initial = state.asOf && weeks.includes(state.asOf) ? weeks.indexOf(state.asOf) : weeks.length - 1;
  slider.value = String(initial);
  output.textContent = weeks[initial];
  slider.addEventListener("input", () => {
    output.textContent = weeks[Number(slider.value)];
  });
  slider.addEventListener("change", () => {
    setAsOf(weeks[Number(slider.value)]);
    renderAsOfOnly();
  });

  let playing = false;
  document.getElementById("replay").addEventListener("click", async () => {
    if (playing) { playing = false; return; }
    playing = true;
    const start = Math.max(0, weeks.length - 16);
    for (let i = start; i < weeks.length && playing; i++) {
      slider.value = String(i);
      output.textContent = weeks[i];
      setAsOf(weeks[i]);
      renderAsOfOnly();
      await new Promise((r) => setTimeout(r, 600));
    }
    playing = false;
  });
}

function modeBadge() {
  const node = document.getElementById("modeBadge");
  const mode = meta.llm_mode === "fake" ? "FAKE DATA"
    : meta.live_model ? `live · ${meta.live_model}`
    : `recorded runs · data ${String(meta.data_version || "").slice(0, 8)}`;
  node.textContent = mode;
  node.classList.toggle("fake", meta.llm_mode === "fake");
  node.title = meta.llm_mode === "fake"
    ? "Extractions came from the heuristic fake client, not a model"
    : "Recorded answers replay real tool runs; with an API key the agent answers live";
}

function pipelineStrip() {
  const counts = meta.counts || {};
  const qa = meta.qa || {};
  const bits = [
    `${num(counts.n_calls)} calls`, `${num(counts.n_topics)} topics`, `${num(counts.n_themes)} themes`,
  ];
  if (qa.reason_agreement) bits.push(`reason agreement ${Number(qa.reason_agreement).toFixed(2)}`);
  if (qa.quote_verify_rate) bits.push(`quotes verified ${pct(qa.quote_verify_rate)}`);
  document.getElementById("pipelineStrip").textContent = bits.join(" · ");
}

/** The first thing a first-time viewer - a judge, not an analyst - sees on Overview. The rail strip
 *  above already carries the same numbers for anyone who's used the tool before; this says what they
 *  mean, once, in plain sentences, so nobody needs the glossary to read the panels below it. */
function renderHero() {
  const counts = meta.counts || {};
  const qa = meta.qa || {};
  const sources = meta.sources || [];
  const strip = document.getElementById("heroStrip");
  if (!counts.n_calls) { strip.hidden = true; return; }
  strip.hidden = false;

  const kinds = [...new Set(sources.map((s) => s.kind))];
  const corpusPhrase = kinds.includes("real") && kinds.includes("synthetic")
    ? "real written complaints and synthetic call transcripts"
    : kinds.includes("synthetic") ? "synthetic call transcripts" : "real written complaints";
  document.getElementById("heroLine").textContent =
    `${num(counts.n_calls)} customer contacts - ${corpusPhrase} - read once each and grouped into `
    + `${num(counts.n_themes)} themes.`;

  const stats = [
    [num(counts.n_calls), "contacts read"],
    [num(counts.n_themes), `themes, from ${num(counts.n_topics)} topics`],
    [qa.quote_verify_rate != null ? pct(qa.quote_verify_rate) : "-", "quotes verify word-for-word"],
    [qa.reason_agreement != null ? pct(qa.reason_agreement) : "-", "match the bank's own category, read blind"],
  ];
  const wrap = clear(document.getElementById("heroStats"));
  for (const [value, caption] of stats) {
    wrap.appendChild(el("div", { class: "hero-stat" }, [el("strong", { text: value }), el("span", { text: caption })]));
  }
}

function aboutModal() {
  const node = document.getElementById("modal");
  const body = clear(document.getElementById("modalBody"));
  const p = meta.provenance || {};
  const qa = meta.qa || {};
  node.hidden = false;
  body.appendChild(el("h2", { text: "About this data" }));
  body.appendChild(el("p", { text: p.note || "" }));
  const rows = [
    ["Source", p.source], ["Company", p.company],
    ["Window", p.window?.start ? `${p.window.start} to ${p.window.end}` : ""],
    ["Sampled", p.sampling_fraction ? `${pct(p.sampling_fraction)} of eligible complaints per month (seed ${p.seed ?? "?"})` : ""],
    ["Eligible population", p.n_eligible ? `${num(p.n_eligible)} of ${num(p.n_raw)} pulled` : ""],
    ["Calls in the index", num((meta.counts || {}).n_calls)],
    ["Topics extracted", num((meta.counts || {}).n_topics)],
    ["Themes", num((meta.counts || {}).n_themes)],
    ["As-of week", meta.as_of_week], ["Data version", meta.data_version],
    ["Extraction mode", meta.llm_mode],
  ];
  body.appendChild(el("table", { class: "kv" }, rows.filter(([, v]) => v !== undefined && v !== "" && v !== null)
    .map(([k, v]) => el("tr", {}, [el("td", { text: k }), el("td", { text: String(v) })]))));
  if (Object.keys(qa).length) {
    body.appendChild(el("h3", { text: "Extraction quality" }));
    body.appendChild(el("table", { class: "kv" }, Object.entries(qa)
      .map(([k, v]) => el("tr", {}, [el("td", { text: label(k) }),
                                     el("td", { text: typeof v === "object" ? JSON.stringify(v) : String(v) })]))));
  }
  body.appendChild(el("p", { class: "footnote", text:
    "Dates are when the regulator received the complaint, which lags the underlying contact. " +
    "Redactions such as XXXX are the regulator's and are kept verbatim in every quote. " +
    "Written complaints are real; call transcripts are synthetic and labelled SYNTHETIC everywhere " +
    "they appear. Nothing is fabricated to fit a narrative - the corpus picker on the left always " +
    "says which kind a number covers." }));
}

async function boot() {
  readURL();
  initDrawer();
  initThemeCard();
  initDashboard();
  document.getElementById("clearFilters").addEventListener("click", () => {
    clearFilters();
    for (const box of document.querySelectorAll("#sourceBoxes input")) box.checked = true;
    for (const box of document.querySelectorAll("#sourceBoxes .source-box")) box.classList.add("on");
    for (const id of ["fProduct", "fSegment", "fRegionGroup"]) {
      for (const o of document.getElementById(id).options) o.selected = false;
    }
    document.getElementById("fFrom").value = "";
    document.getElementById("fTo").value = "";
  });
  for (const [id, key] of [["fFrom", "date_from"], ["fTo", "date_to"]]) {
    const input = document.getElementById(id);
    input.value = state.filters[key] || "";
    input.addEventListener("change", () => setFilter(key, input.value));
  }
  document.getElementById("aboutBtn").addEventListener("click", aboutModal);

  try {
    meta = await api.meta();
  } catch (err) {
    document.getElementById("pipelineStrip").textContent = `API unavailable: ${err.message}`;
    document.getElementById("modeBadge").textContent = "offline";
    return;
  }
  modeBadge();
  pipelineStrip();
  renderHero();
  if (!state.asOf && meta.as_of_week) state.asOf = meta.as_of_week;
  setupAsOf(meta.as_of_weeks || []);
  setupSources(meta.sources || []);
  await initWeekly(meta.as_of_week);
  initAsk(meta.questions || []);
  initGraph();
  initNav({ navGraph: showGraph });      // the scene is built on first visit, not on boot
  await loadFilterOptions();
  renderAll();
  onChange((reason) => { if (reason !== "asof") renderAll(); });
}

boot();
