// Formatting and safe DOM helpers. Nothing from the API is ever inserted as raw HTML.

export function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

export function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = String(value);
    else if (key === "html") node.innerHTML = value;            // only for strings we built ourselves
    else if (key.startsWith("on") && typeof value === "function") node.addEventListener(key.slice(2), value);
    else if (key === "dataset") Object.assign(node.dataset, value);
    else node.setAttribute(key, String(value));
  }
  for (const child of [].concat(children)) {
    if (child === null || child === undefined || child === false) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

export function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
  return node;
}

export const num = (v) => (v === null || v === undefined || Number.isNaN(Number(v))
  ? "-" : Number(v).toLocaleString("en-US"));

/** A fraction (0.031) rendered as a percentage. Never pass a value that is already a percentage:
 *  0.4 meaning "0.4 per cent" is indistinguishable from 0.4 meaning "40 per cent". */
export function pct(v, digits = 1) {
  if (v === null || v === undefined || Number.isNaN(Number(v))) return "-";
  return `${(Number(v) * 100).toFixed(digits)}%`;
}

/** A value that is already a percentage (3.1 -> "3.1%"). */
export function pctOf(v, digits = 1) {
  if (v === null || v === undefined || Number.isNaN(Number(v))) return "-";
  return `${Number(v).toFixed(digits)}%`;
}

export const signed = (v, digits = 1) =>
  v === null || v === undefined ? "" : `${Number(v) > 0 ? "+" : ""}${Number(v).toFixed(digits)}`;

export function label(code) {
  return String(code ?? "").replace(/_/g, " ").replace(/^\w/, (c) => c.toUpperCase());
}

export const shortDate = (iso) => (iso ? String(iso).slice(0, 10) : "");

/** A hard character slice cuts mid-word; this backs up to the last space before the limit. */
export function truncate(text, max = 160) {
  const s = String(text ?? "");
  if (s.length <= max) return s;
  const cut = s.slice(0, max);
  const lastSpace = cut.lastIndexOf(" ");
  return `${lastSpace > max * 0.6 ? cut.slice(0, lastSpace) : cut}…`;
}

// Minimal, safe markdown: paragraphs, **bold**, *italic*, `code`, - lists, and [c1] claim markers.
export function markdown(text) {
  const inline = (s) => esc(s)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[(c\d+)\]/g, '<span class="marker">[$1]</span>');
  const out = [];
  let list = null;
  for (const raw of String(text ?? "").split("\n")) {
    const line = raw.trim();
    if (!line) { if (list) { out.push(`<ul>${list.join("")}</ul>`); list = null; } continue; }
    if (/^[-*]\s+/.test(line)) { (list ??= []).push(`<li>${inline(line.replace(/^[-*]\s+/, ""))}</li>`); continue; }
    if (list) { out.push(`<ul>${list.join("")}</ul>`); list = null; }
    out.push(`<p>${inline(line)}</p>`);
  }
  if (list) out.push(`<ul>${list.join("")}</ul>`);
  return out.join("");
}

export function bar(fraction, tone = "") {
  const width = Math.max(0, Math.min(100, Number(fraction) * 100 || 0));
  return el("div", { class: `bar ${tone}` }, [el("span", { style: `width:${width.toFixed(1)}%` })]);
}

export function badge(confidence) {
  if (!confidence) return el("span", { class: "badge", text: "no support" });
  return el("span", { class: `badge ${esc(confidence.tier || "")}`, text: confidence.badge || confidence.tier || "" });
}

export function statusPill(status) {
  return el("span", { class: `pill ${esc(status || "stable")}`, text: status || "stable" });
}

/** A canvas chart has no text content at all - nothing for a screen reader, nothing to copy. This
 *  appends a toggle and a real, initially-collapsed table with the chart's own numbers as its text
 *  alternative. Removes any table+toggle it previously attached to the same wrap first, so a
 *  re-render doesn't accumulate copies. */
export function attachChartTable(wrap, columns, rows) {
  wrap.querySelector(".chart-table-toggle")?.remove();
  wrap.querySelector(".chart-table")?.remove();
  const table = el("table", { class: "chart-table" }, [
    el("thead", {}, [el("tr", {}, columns.map((c) => el("th", { text: c })))]),
    el("tbody", {}, rows.map((r) => el("tr", {}, r.map((v, i) =>
      el(i === 0 ? "th" : "td", i === 0 ? { text: String(v), scope: "row" } : { text: String(v) }))))),
  ]);
  table.hidden = true;
  const btn = el("button", { type: "button", class: "ghost chart-table-toggle",
                             text: "View as table", "aria-expanded": "false" });
  btn.addEventListener("click", () => {
    table.hidden = !table.hidden;
    btn.textContent = table.hidden ? "View as table" : "Hide table";
    btn.setAttribute("aria-expanded", String(!table.hidden));
  });
  wrap.appendChild(btn);
  wrap.appendChild(table);
}

/** "1 product", "3 products" - the theme card headline is the demo's most-read line. */
export function plural(n, singular, pluralForm = null) {
  const count = Number(n) || 0;
  return `${num(count)} ${count === 1 ? singular : (pluralForm ?? singular + "s")}`;
}
