// The four dashboard panels. Each is one call to the same function the agent calls.

import { api } from "./api.js";
import { openCall, openCallList } from "./calldrawer.js";
import { openTheme } from "./themecard.js";
import { bar, clear, el, label, num, pct, signed, statusPill } from "./format.js";
import { queryParams, state } from "./state.js";
import { trendChart } from "./charts.js";

let driverPolarity = "negative";
let lastTrendIds = [];

function panel(id) { return document.getElementById(id); }

function failed(node, err) {
  clear(node).appendChild(el("p", { class: "muted", text: `could not load: ${err.message}` }));
}

function callsLink(resultId, text, title) {
  return el("button", { class: "linkish", text, onclick: () => openCallList(resultId, title) });
}

export async function renderReasons() {
  const node = panel("reasonsBody");
  try {
    const payload = await api.reasons(queryParams());
    const rows = (payload.rows || []).slice(0, 8);
    const max = Math.max(1, ...rows.map((r) => r.n_calls || 0));
    const out = clear(node);
    if (!rows.length) { out.appendChild(el("p", { class: "muted", text: "no reasons above minimum support in this scope" })); return; }
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
            document.createTextNode(`${num(row.n_calls)} · ${pct(row.share ?? row.share_pct)}`),
            delta ? el("span", { class: `delta ${delta > 0 ? "up" : "down"}`, text: ` ${signed(delta)} pts` }) : null,
            dir && dir !== "flat" ? el("span", { class: `delta ${dir === "rising" ? "up" : "down"}`, text: ` ${dir}` }) : null,
          ]),
        ]),
        bar((row.n_calls || 0) / max),
        specifics ? el("p", { class: "quote", text: specifics.slice(0, 160) }) : null,
      ]));
    }
    if (payload.result_id) {
      out.appendChild(el("p", { class: "footnote" }, [
        callsLink(payload.result_id, `${num(payload.scope?.n_calls_in_scope)} calls in scope`, "Calls in scope"),
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
    const out = clear(node);
    if (driverPolarity === "positive") {
      out.appendChild(el("p", { class: "footnote", text: "Positive moments inside complaints - this corpus is complaints, not a satisfaction survey." }));
    }
    if (!rows.length) { out.appendChild(el("p", { class: "muted", text: "nothing above minimum support in this scope" })); return; }
    const max = Math.max(1, ...rows.map((r) => r.n_calls || 0));
    for (const row of rows) {
      const quote = (row.quotes || [])[0];
      const themeId = row.theme_id || (String(row.key || "").startsWith("thm_") ? row.key : null);
      const name = el(themeId ? "button" : "span", themeId
        ? { class: "linkish", text: row.name || themeId, onclick: () => openTheme(themeId) }
        : { class: "row-name", text: label(row.name || row.key) });
      out.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [name,
          el("span", { class: "row-meta", text: `${num(row.n_calls)} calls · mean ${Number(row.mean_sentiment ?? 0).toFixed(1)}` })]),
        bar((row.n_calls || 0) / max, driverPolarity === "positive" ? "pos" : "neg"),
        el("div", {}, (row.top_driver_categories || []).slice(0, 2).map((c) =>
          el("span", { class: "chip",
                       text: `${label(typeof c === "string" ? c : c.driver_category || c.key)}${c.n_calls ? ` ${c.n_calls}` : ""}` }))),
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
    for (const row of rows) {
      out.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [
          el("button", { class: "linkish", text: row.name || row.theme_id, onclick: () => openTheme(row.theme_id) }),
          statusPill(row.status),
        ]),
        el("div", { class: "row-meta", text:
          `${num(row.n_recent)} recent vs ${Number(row.expected_recent ?? 0).toFixed(1)} expected · z ${Number(row.z ?? 0).toFixed(1)}` +
          ` · ${num(row.weeks_recent)} weeks · first seen ${row.first_seen_week || "?"}` +
          (row.robust_8w ? " · robust at 8 weeks" : "") + (row.novel_vocabulary ? " · new vocabulary" : "") }),
        bar(Math.min(1, (Number(row.n_recent) || 0) / Math.max(5, ...rows.map((r) => r.n_recent || 0))), "neg"),
      ]));
    }
    if (data.expected_false_positives !== undefined && data.expected_false_positives !== null) {
      const fp = Number(data.expected_false_positives);
      out.appendChild(el("p", { class: "footnote", text:
        `${fp < 0.1 ? "Fewer than 0.1" : `About ${fp.toFixed(1)}`} of ${num(data.n_tested)} themes tested could pass this threshold by chance.` }));
    }
  } catch (err) { failed(node, err); }
}

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
    const payload = await api.trend(ids, "month", queryParams());
    const series = (payload.rows || []).map((r) => ({
      label: r.name || r.entity_id,
      points: (r.series || r.points || []).map((p) => ({ period: p.period, share: p.share, n_calls: p.n_calls })),
    })).filter((s) => s.points.length);
    subtitle.textContent = `monthly share · ${series.length} themes`;
    trendChart("trendChart", series, { valueKey: "share" });
  } catch (err) { subtitle.textContent = `trend unavailable: ${err.message}`; }
}

export function initDashboard() {
  for (const tab of document.querySelectorAll("#panelDrivers .tab")) {
    tab.addEventListener("click", () => {
      for (const t of document.querySelectorAll("#panelDrivers .tab")) t.classList.remove("active");
      tab.classList.add("active");
      driverPolarity = tab.dataset.polarity;
      renderDrivers();
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
