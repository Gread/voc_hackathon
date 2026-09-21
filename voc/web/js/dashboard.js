// The four dashboard panels. Each is one call to the same function the agent calls.

import { api } from "./api.js";
import { openCall, openCallList } from "./calldrawer.js";
import { openTheme } from "./themecard.js";
import { attachChartTable, bar, clear, el, label, num, pct, pctOf, plural, shortDate, signed, statusPill, truncate } from "./format.js";
import { queryParams, state } from "./state.js";
import { seriesToTable, sparkline, trendChart } from "./charts.js";

let driverPolarity = "negative";
let lastTrendIds = [];

function panel(id) { return document.getElementById(id); }

/** Toggling a class is invisible to a screen reader; aria-pressed says which tab is active in
 *  words, not just colour. */
function setActiveTab(groupSelector, active) {
  for (const t of document.querySelectorAll(groupSelector)) {
    const on = t === active;
    t.classList.toggle("active", on);
    t.setAttribute("aria-pressed", String(on));
  }
}

function failed(node, err) {
  clear(node).appendChild(el("p", { class: "muted", text: `could not load: ${err.message}` }));
}

function callsLink(resultId, text, title) {
  return el("button", { class: "linkish", text, onclick: () => openCallList(resultId, title) });
}

/** "mean -1.2" is the -2..+2 sentiment scale showing through. Nobody outside the team reads that
 *  as "these customers are angry", so say it in words and keep the number in the tooltip. */
function sentimentWord(mean) {
  const v = Number(mean);
  if (!Number.isFinite(v)) return null;
  if (v <= -1.5) return "very negative";
  if (v <= -0.5) return "negative";
  if (v < 0.5) return "mixed";
  if (v < 1.5) return "positive";
  return "very positive";
}

export async function renderReasons() {
  const node = panel("reasonsBody");
  try {
    const payload = await api.reasons(queryParams());
    const rows = (payload.rows || []).slice(0, 8);
    const max = Math.max(1, ...rows.map((r) => r.n_calls || 0));
    const out = clear(node);
    if (!rows.length) { out.appendChild(el("p", { class: "muted", text: "no reasons above minimum support in this scope" })); return; }
    // Only claim a comparison when one exists. The API always hands back a previous window of the
    // same length, but here that lands on 2020-11..2023-08, where this corpus has no calls at all -
    // announcing it implied these shares were measured against something real. They weren't.
    const prevWindow = payload.data?.previous_period;
    const comparable = rows.some((r) => Number(r.n_previous) > 0);
    if (prevWindow && comparable) {
      out.appendChild(el("p", { class: "footnote", text:
        `Change is against ${shortDate(prevWindow[0])} to ${shortDate(prevWindow[1])} - the same length of time, immediately before.` }));
    } else {
      out.appendChild(el("p", { class: "footnote", text:
        "Share of all contacts in view. There is no earlier period in this data to compare against." }));
    }
    for (const row of rows) {
      // A delta needs a comparable previous period; without one only the trend direction is meaningful.
      const comparable = Number(row.n_previous) > 0;
      const delta = comparable ? row.delta_share_pts : null;
      const dir = row.direction || "flat";
      const specifics = (row.top_specific_reasons || []).map((s) => `${s.text} (${s.n})`).join(" · ");
      out.appendChild(el("div", { class: "row", title: specifics }, [
        el("div", { class: "row-head" }, [
          el("span", { class: "row-name", text: label(row.label || row.reason) }),
          el("span", { class: "row-meta" }, [
            document.createTextNode(`${num(row.n_calls)} · ${row.share !== undefined && row.share !== null ? pct(row.share) : pctOf(row.share_pct)}`),
            delta ? el("span", { class: `delta ${delta > 0 ? "up" : "down"}`, text: ` ${signed(delta)} pts` }) : null,
            dir && dir !== "flat" ? el("span", { class: `delta ${dir === "rising" ? "up" : "down"}`, text: ` ${dir}` }) : null,
          ]),
        ]),
        bar((row.n_calls || 0) / max),
        specifics ? el("p", { class: "quote", text: truncate(specifics, 160) }) : null,
      ]));
    }
    if (payload.result_id) {
      // Say what the link opens: a result covers the calls that carry a reason, which is fewer than
      // the scope whenever some calls are not yet read.
      const inResult = payload.n_call_ids ?? 0;
      const inScope = payload.scope?.n_calls_in_scope ?? 0;
      out.appendChild(el("p", { class: "footnote" }, [
        callsLink(payload.result_id, `${num(inResult)} calls carry a contact reason`, "Calls with a contact reason"),
        inScope > inResult
          ? el("span", { class: "muted", text: ` of ${num(inScope)} in scope` })
          : null,
      ]));
    }
  } catch (err) { failed(node, err); }
}

export async function renderDrivers() {
  const node = panel("driversBody");
  try {
    const payload = await api.drivers(queryParams(), {
      polarity: driverPolarity, group_by: driverPolarity === "positive" ? "driver_category" : "theme", limit: 6,
    });
    const rows = payload.rows || [];
    const moments = (payload.data || {}).positive_moments_by_category || [];
    const out = clear(node);
    if (driverPolarity === "positive") {
      out.appendChild(el("p", { class: "footnote", text: payload.data?.corpus_note
        ? `What went right, ${payload.data.corpus_note}.`
        : "Positive moments inside complaints - this corpus is complaints, not a satisfaction survey." }));
      // Positive topics rarely clear minimum support on a complaint corpus; the moments carry this panel.
      for (const m of moments) {
        const quote = (m.quotes || [])[0];
        out.appendChild(el("div", { class: "row" }, [
          el("div", { class: "row-head" }, [
            el("span", { class: "row-name", text: label(m.category) }),
            el("span", { class: "row-meta", text: `${plural(m.n_calls, "call")} · ${pctOf(m.share_pct)}` }),
          ]),
          bar((m.n_calls || 0) / Math.max(1, ...moments.map((x) => x.n_calls || 0)), "pos"),
          quote ? el("p", { class: "quote" }, [
            el("button", { class: "linkish", text: `"${quote.quote.slice(0, 150)}"`,
                           onclick: () => openCall(quote.call_id, quote.quote) })]) : null,
        ]));
      }
    }
    if (!rows.length) {
      if (!moments.length) out.appendChild(el("p", { class: "muted", text: "nothing above minimum support in this scope" }));
      return;
    }
    const max = Math.max(1, ...rows.map((r) => r.n_calls || 0));
    for (const row of rows) {
      const quote = (row.quotes || [])[0];
      const themeId = row.theme_id || (String(row.key || "").startsWith("thm_") ? row.key : null);
      const name = el(themeId ? "button" : "span", themeId
        ? { class: "linkish", text: row.name || themeId, onclick: () => openTheme(themeId) }
        : { class: "row-name", text: label(row.name || row.key) });
      const mood = sentimentWord(row.mean_sentiment);
      out.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [name,
          el("span", { class: "row-meta",
                       title: `mean sentiment ${Number(row.mean_sentiment ?? 0).toFixed(2)} on a -2 to +2 scale`,
                       text: `${plural(row.n_calls, "call")}${mood ? ` · ${mood}` : ""}` })]),
        bar((row.n_calls || 0) / max, driverPolarity === "positive" ? "pos" : "neg"),
        el("div", {}, (row.top_driver_categories || []).slice(0, 2).map((c) =>
          el("span", { class: "chip",
                       text: `${label(typeof c === "string" ? c : c.driver_category || c.key)}${c.n_calls ? ` · ${num(c.n_calls)}` : ""}` }))),
        (row.top_specific_drivers || []).length
          ? el("p", { class: "quote", text: row.top_specific_drivers[0].text }) : null,
        quote ? el("p", { class: "quote" }, [
          el("button", { class: "linkish", text: `"${quote.quote.slice(0, 150)}"`,
                         onclick: () => openCall(quote.call_id, quote.quote) })]) : null,
      ]));
    }
    if (payload.result_id) {
      out.appendChild(el("p", { class: "footnote" }, [callsLink(payload.result_id, "which calls?", "Calls behind these drivers")]));
    }
  } catch (err) { failed(node, err); }
}

export async function renderEmerging() {
  const node = panel("emergingBody");
  try {
    const payload = await api.emerging(queryParams(), { limit: 8, min_recent: 5 });
    const rows = payload.rows || [];
    const data = payload.data || {};
    const out = clear(node);
    if (!rows.length) {
      out.appendChild(el("p", { class: "muted", text: `no theme passed the threshold at ${payload.as_of_week || "this week"}` }));
    }
    // One weekly-trend call covers the whole panel; the endpoint takes six entity ids at a time.
    // A failure here costs the sparklines and nothing else, so the panel still renders without it.
    const ids = rows.map((r) => r.theme_id).filter(Boolean).slice(0, 6);
    let seriesById = {};
    if (ids.length) {
      try {
        const trend = await api.trend(ids, "week", queryParams());
        seriesById = Object.fromEntries((trend.rows || []).map((r) => [r.entity_id, r.series || []]));
      } catch { /* sparklines are an enhancement, never a dependency */ }
    }
    for (const row of rows) {
      const recent = Number(row.n_recent) || 0;
      const expected = Number(row.expected_recent ?? 0);
      const ratio = expected > 0 ? recent / expected : null;
      // The statistic (z, weeks, first-seen) is what built the detector; the pace is what a reader
      // needs first. Plain sentence leads, the numbers that back it sit underneath in .row-meta.
      const plain = ratio && ratio >= 1.15
        ? `${plural(recent, "call")} in the last 4 weeks — about ${ratio.toFixed(1)}× the usual pace`
        : `${plural(recent, "call")} in the last 4 weeks`;
      out.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [
          el("button", { class: "linkish", text: row.name || row.theme_id, onclick: () => openTheme(row.theme_id) }),
          statusPill(row.status),
        ]),
        el("p", { style: "margin:2px 0 0", text: plain }),
        el("div", { class: "row-meta",
          title: `expected ${expected.toFixed(1)} · z ${Number(row.z ?? 0).toFixed(1)} · ${plural(row.weeks_recent, "week")} with activity`,
          text: `First seen ${row.first_seen_week || "?"}`
          + (row.robust_8w ? " · confirmed over 8 weeks, not just 4" : "")
          + (row.novel_vocabulary ? " · wording not seen before" : "") }),
        (seriesById[row.theme_id] || []).length
          ? el("div", { class: "spark-wrap" }, [
              sparkline(seriesById[row.theme_id]),
              el("span", { class: "spark-caption", text: "weekly calls, last 6 months · red = the last 4 weeks" }),
            ])
          : bar(Math.min(1, recent / Math.max(5, ...rows.map((r) => r.n_recent || 0))), "neg"),
      ]));
    }
    if (data.expected_false_positives !== undefined && data.expected_false_positives !== null) {
      const fp = Number(data.expected_false_positives);
      out.appendChild(el("p", { class: "footnote", text:
        `${fp < 0.1 ? "Fewer than 0.1" : `About ${fp.toFixed(1)}`} of ${num(data.n_tested)} themes tested could pass this threshold by chance.` }));
    }
  } catch (err) { failed(node, err); }
}

let trendGrain = "month";

export async function renderTrend(entityIds = null) {
  const subtitle = document.getElementById("trendSubtitle");
  try {
    let ids = entityIds;
    if (!ids) {
      const themes = await api.themes(queryParams(), { sort_by: "n_calls", limit: 4 });
      ids = (themes.rows || []).map((r) => r.theme_id).filter(Boolean);
    }
    lastTrendIds = ids;
    if (!ids.length) { subtitle.textContent = "no themes in this scope"; return; }
    const payload = await api.trend(ids, trendGrain, queryParams());
    const series = (payload.rows || []).map((r) => ({
      label: r.name || r.entity_id,
      points: (r.series || r.points || []).map((p) => ({ period: p.period, share: p.share, n_calls: p.n_calls })),
    })).filter((s) => s.points.length);
    subtitle.textContent = `${trendGrain}ly share · ${series.length} themes`;
    trendChart("trendChart", series, { valueKey: "share" });
    const { columns, rows } = seriesToTable(series, "share");
    // The table/toggle append after the chart, but must sit outside .chart-box: Chart.js
    // (responsive: true, maintainAspectRatio: false) sizes the canvas from that box's own
    // height, and adding sibling content inside it breaks that measurement.
    attachChartTable(document.getElementById("trendChart").closest(".panel-body"), columns, rows);
  } catch (err) { subtitle.textContent = `trend unavailable: ${err.message}`; }
}

export function initDashboard() {
  for (const tab of document.querySelectorAll("#panelDrivers .tab")) {
    tab.setAttribute("aria-pressed", String(tab.classList.contains("active")));
    tab.addEventListener("click", () => {
      setActiveTab("#panelDrivers .tab", tab);
      driverPolarity = tab.dataset.polarity;
      renderDrivers();
    });
  }
  for (const tab of document.querySelectorAll("#trendGrain .tab")) {
    tab.setAttribute("aria-pressed", String(tab.classList.contains("active")));
    tab.addEventListener("click", () => {
      setActiveTab("#trendGrain .tab", tab);
      trendGrain = tab.dataset.grain;
      renderTrend(lastTrendIds.length ? lastTrendIds : null);
    });
  }
}

export function renderAll() {
  renderReasons();
  renderDrivers();
  renderEmerging();
  renderTrend(lastTrendIds.length ? lastTrendIds : null);
}

export function renderAsOfOnly() { renderEmerging(); }
