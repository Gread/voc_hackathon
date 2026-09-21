// Theme card: the "same problem, different words" exhibit, with breakdowns and merge history.

import { api } from "./api.js";
import { openCall, openCallList } from "./calldrawer.js";
import { closeOverlay, openOverlay } from "./dialog.js";
import { clear, el, label, num, pct, plural, shortDate, statusPill } from "./format.js";
import { queryParams } from "./state.js";
import { trendChart } from "./charts.js";

const modal = () => document.getElementById("modal");
const body = () => document.getElementById("modalBody");

export function closeModal() { closeOverlay(modal()); }

export function initThemeCard() {
  document.getElementById("modalClose").addEventListener("click", closeModal);
  modal().addEventListener("click", (e) => { if (e.target === modal()) closeModal(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });
}

function breakdownTabs(container, themeId) {
  const dims = [["product", "Product"], ["segment", "Segment"], ["region_group", "Region"]];
  const tabs = el("span", { class: "tabs" });
  const target = el("div");
  const load = async (dim) => {
    clear(target).appendChild(el("p", { class: "muted", text: "loading…" }));
    let payload;
    try {
      payload = await api.breakdown(queryParams(), { entity_type: "theme", entity_id: themeId, by: dim });
    } catch (err) {
      clear(target).appendChild(el("p", { class: "muted", text: err.message }));
      return;
    }
    const rows = payload.rows || [];
    const maxLift = Math.max(1, ...rows.filter((r) => !r.suppressed).map((r) => Number(r.lift) || 0));
    clear(target);
    if (!rows.length) { target.appendChild(el("p", { class: "muted", text: "no rows" })); return; }
    for (const row of rows) {
      if (row.suppressed) {
        target.appendChild(el("div", { class: "row" }, [
          el("div", { class: "row-head" }, [
            el("span", { class: "row-name suppressed", text: label(row.value) }),
            el("span", { class: "row-meta suppressed", text: "below minimum support" }),
          ]),
        ]));
        continue;
      }
      target.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [
          el("span", { class: "row-name", text: label(row.value) }),
          el("span", { class: "row-meta", text: `${num(row.n_calls)} of ${num(row.n_slice)} · ${pct(row.share)} · ${Number(row.lift || 0).toFixed(2)}x` }),
        ]),
        el("div", { class: "bar" }, [el("span", { style: `width:${Math.min(100, (Number(row.lift) || 0) / maxLift * 100)}%` })]),
      ]));
    }
  };
  for (const [dim, name] of dims) {
    const btn = el("button", { class: "tab", text: name, type: "button", "aria-pressed": "false", onclick: () => {
      for (const t of tabs.children) { t.classList.remove("active"); t.setAttribute("aria-pressed", "false"); }
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      load(dim);
    } });
    tabs.appendChild(btn);
  }
  tabs.firstChild.classList.add("active");
  tabs.firstChild.setAttribute("aria-pressed", "true");
  container.appendChild(tabs);
  container.appendChild(target);
  load("product");
}

export async function openTheme(themeId) {
  const node = modal();
  openOverlay(node, body());
  clear(body()).appendChild(el("p", { class: "muted", text: "loading theme…" }));
  let payload;
  try {
    payload = await api.theme(themeId, queryParams());
  } catch (err) {
    clear(body()).appendChild(el("p", { class: "muted", text: `could not load theme: ${err.message}` }));
    return;
  }
  const d = payload.data || {};
  const out = clear(body());

  out.appendChild(el("h2", { text: d.name || themeId }));
  out.appendChild(el("p", { text: d.problem_statement || "" }));
  if (d.root_cause) out.appendChild(el("p", { class: "muted", text: `Root cause as customers describe it: ${d.root_cause}` }));

  const head = el("p", { class: "row-meta" }, [
    el("strong", { text: plural(d.n_calls, "call") }), document.createTextNode(" · "),
    el("strong", { text: plural(d.n_wordings, "wording") }), document.createTextNode(" · "),
    el("strong", { text: plural(d.n_products, "product") }),
    d.status ? document.createTextNode(" · ") : null, d.status ? statusPill(d.status) : null,
  ]);
  out.appendChild(head);
  if (payload.result_id) {
    out.appendChild(el("button", { class: "linkish", text: "show the calls behind this theme",
                                   onclick: () => openCallList(payload.result_id, d.name || themeId) }));
  }
  if (d.grouping_quality === "weak") {
    out.appendChild(el("p", { class: "footnote", text: "Grouping quality: weak - these statements were less stable when re-assigned." }));
  }

  if ((d.weekly_series || []).length) {
    out.appendChild(el("h3", { text: "Week by week" }));
    const canvas = el("canvas", { id: "themeTrendChart", height: "120" });
    out.appendChild(el("div", { style: "height:160px" }, [canvas]));
    setTimeout(() => trendChart("themeTrendChart",
      [{ label: d.name || themeId, points: d.weekly_series.map((p) => ({ period: p.period, share: p.share, n_calls: p.n_calls })) }],
      { valueKey: "n_calls" }), 0);
  }

  out.appendChild(el("h3", { text: `The same problem in ${plural(d.n_wordings, "different wording")}` }));
  const wordings = d.wordings || [];
  if (!wordings.length) out.appendChild(el("p", { class: "muted", text: "no member statements" }));
  for (const w of wordings) {
    out.appendChild(el("div", { class: "wording" }, [
      el("button", { class: "linkish", text: w.issue_statement, onclick: () => openCall(w.call_id) }),
      el("span", { class: "row-meta", text: ` — ${shortDate(w.date)} · ${label(w.product)}` }),
    ]));
  }

  if ((d.top_specific_drivers || []).length) {
    out.appendChild(el("h3", { text: "What specifically triggers it" }));
    for (const t of d.top_specific_drivers) {
      out.appendChild(el("div", { class: "row" }, [
        el("span", { text: t.text }), el("span", { class: "row-meta", text: ` ${plural(t.n, "call")}` }),
      ]));
    }
  }

  out.appendChild(el("h3", { text: "Who it affects" }));
  breakdownTabs(out, themeId);

  if ((d.merge_history || []).length) {
    out.appendChild(el("h3", { text: "Merge history" }));
    for (const m of d.merge_history) {
      out.appendChild(el("p", { class: "footnote",
        text: `absorbed ${m.from_theme} — ${m.reason || "same cause, different wording"} (judged by ${m.judged_by || "?"})` }));
    }
  }
}
