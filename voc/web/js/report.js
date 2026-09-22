// A downloadable summary of what is currently on screen.
//
// One self-contained HTML file: no stylesheet to lose, no fonts to fetch, opens in any browser and
// prints straight to PDF. That matters more than a prettier format nobody can open - this is the
// artefact someone forwards to a manager who will never log into the tool.
//
// It reports the CURRENT scope, not the whole corpus: the filters and as-of week are printed at the
// top, so a report taken under a filter can never be mistaken for the full picture.

import { api } from "./api.js";
import { esc, num, pct, pctOf } from "./format.js";
import { queryParams, state } from "./state.js";

const sty = {
  page: "font-family:'IBM Plex Sans',system-ui,sans-serif;color:#292929;max-width:900px;margin:32px auto;padding:0 24px;line-height:1.5",
  h1: "font-size:26px;color:#00427a;margin:0 0 4px",
  h2: "font-size:17px;color:#00427a;margin:28px 0 8px;border-bottom:1px solid #d6d6d6;padding-bottom:6px",
  meta: "font-size:12px;color:#666;margin:0",
  table: "border-collapse:collapse;width:100%;font-size:13px;margin-top:6px",
  th: "text-align:left;border-bottom:1px solid #d6d6d6;padding:6px 8px;color:#666;font-weight:600",
  td: "border-bottom:1px solid #f0f0f0;padding:6px 8px",
  tdNum: "border-bottom:1px solid #f0f0f0;padding:6px 8px;text-align:right;font-family:'IBM Plex Mono',monospace",
  note: "font-size:12px;color:#666;margin-top:24px;border-top:1px solid #d6d6d6;padding-top:10px",
};

const rowsToTable = (headers, rows) => `
  <table style="${sty.table}">
    <tr>${headers.map((h, i) => `<th style="${sty.th}${i ? ";text-align:right" : ""}">${esc(h)}</th>`).join("")}</tr>
    ${rows.map((r) => `<tr>${r.map((c, i) =>
      `<td style="${i ? sty.tdNum : sty.td}">${esc(String(c))}</td>`).join("")}</tr>`).join("")}
  </table>`;

function scopeLine(meta) {
  const f = state.filters || {};
  const parts = [];
  for (const [k, v] of Object.entries(f)) {
    parts.push(`${k.replace(/_/g, " ")}: ${Array.isArray(v) ? v.join(", ") : v}`);
  }
  if (state.asOf) parts.push(`as of ${state.asOf}`);
  return parts.length ? parts.join(" · ") : "No filters - every contact in the index";
}

/** Build the report HTML from the same endpoints the dashboard itself renders from. */
export async function buildReportHTML() {
  const f = queryParams();
  const [meta, reasons, emerging, drivers] = await Promise.all([
    api.meta(),
    api.reasons(f).catch(() => ({ rows: [] })),
    api.emerging(f, { limit: 8, min_recent: 5 }).catch(() => ({ rows: [] })),
    api.drivers(f, { polarity: "negative", group_by: "theme", limit: 6 }).catch(() => ({ rows: [] })),
  ]);
  const counts = meta.counts || {};
  const qa = meta.qa || {};
  const generated = new Date().toISOString().slice(0, 16).replace("T", " ");

  const emergingRows = (emerging.rows || []).map((r) => {
    const expected = Number(r.expected_recent ?? 0);
    const ratio = expected > 0 ? (Number(r.n_recent) / expected).toFixed(1) + "x" : "-";
    return [r.name || r.theme_id, num(r.n_recent), expected.toFixed(1), ratio, r.first_seen_week || "-"];
  });
  const reasonRows = (reasons.rows || []).slice(0, 10).map((r) =>
    [r.label || r.reason, num(r.n_calls),
     r.share !== undefined && r.share !== null ? pct(r.share) : pctOf(r.share_pct)]);
  const driverRows = (drivers.rows || []).map((r) =>
    [r.name || r.key, num(r.n_calls), Number(r.mean_sentiment ?? 0).toFixed(2)]);

  return `<!doctype html>
<meta charset="utf-8">
<title>Kundröster report ${esc(generated)}</title>
<body style="${sty.page}">
<h1 style="${sty.h1}">Voice of the Customer - summary</h1>
<p style="${sty.meta}">Generated ${esc(generated)} · data version ${esc(String(meta.data_version || "").slice(0, 8))}</p>
<p style="${sty.meta}">Scope: ${esc(scopeLine(meta))}</p>

<h2 style="${sty.h2}">What was read</h2>
${rowsToTable(["", "Value"], [
  ["Customer contacts read", num(counts.n_calls)],
  ["Topics extracted", num(counts.n_topics)],
  ["Themes", num(counts.n_themes)],
  ["Quotes verified word-for-word", qa.quote_verify_rate != null ? pct(qa.quote_verify_rate) : "-"],
  ["Agreement with the bank's own category", qa.reason_agreement != null ? pct(qa.reason_agreement) : "-"],
])}

<h2 style="${sty.h2}">Emerging now</h2>
${emergingRows.length
    ? rowsToTable(["Theme", "Calls, last 4 weeks", "Expected", "Vs usual", "First seen"], emergingRows)
    : `<p style="${sty.meta}">No theme passed the threshold in this scope.</p>`}

<h2 style="${sty.h2}">What customers contact us about</h2>
${reasonRows.length ? rowsToTable(["Reason", "Calls", "Share"], reasonRows)
    : `<p style="${sty.meta}">Nothing above minimum support in this scope.</p>`}

<h2 style="${sty.h2}">Biggest sources of frustration</h2>
${driverRows.length ? rowsToTable(["Theme", "Calls", "Mean sentiment"], driverRows)
    : `<p style="${sty.meta}">Nothing above minimum support in this scope.</p>`}

<p style="${sty.note}">
Every figure here was recounted from the call ids behind it before it was written, by the same
server-side check the dashboard uses. Mean sentiment runs from -2 to +2.
Written complaints are real, published by the US consumer regulator; call transcripts are synthetic
and labelled as such. Dates are when the complaint was received, which lags the contact itself.
</p>
</body>`;
}

/** Trigger the download. Object URL is revoked on the next tick, once the click has been handled. */
export async function downloadReport(button) {
  const original = button ? button.textContent : null;
  if (button) { button.disabled = true; button.textContent = "Preparing…"; }
  try {
    const html = await buildReportHTML();
    const stamp = new Date().toISOString().slice(0, 10);
    const url = URL.createObjectURL(new Blob([html], { type: "text/html;charset=utf-8" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `kundroster-report-${stamp}.html`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  } catch (err) {
    window.alert(`Could not build the report: ${err.message}`);
  } finally {
    if (button) { button.disabled = false; button.textContent = original; }
  }
}
