// The weekly customer review: four questions about one week, each answered from the same
// queries the dashboard runs. Every count is a link to the calls behind it.
import { api } from "./api.js";
import { openCall, openCallList } from "./calldrawer.js";
import { clear, el, label, num, pctOf, plural } from "./format.js";
import { openTheme } from "./themecard.js";

const QUESTIONS = [
  ["changed", "What changed in customer contacts this week?",
   "Top reasons, new issues and changes in share of calls."],
  ["drove_feeling", "Which experiences drove frustration or satisfaction?",
   "Specific moments and recurring causes in customers' own words."],
  ["needs_attention", "Which issues need attention first?",
   "Growing pain points, call volumes and reported customer impact."],
  ["supporting", "What do the supporting calls actually say?",
   "Exact excerpts, distinct call counts and limits of the evidence."],
];

let weeks = [];
let current = null;

const arrow = (d) => (d === "up" ? "▲" : d === "down" ? "▼" : d === "flat" ? "→" : "");
const moveClass = (d) => (d === "up" ? "up" : d === "down" ? "down" : "flat");

function movement(delta, suffix = " pts") {
  if (!delta || delta.direction === "unknown" || delta.points === null) {
    return el("span", { class: "move flat", text: "no prior week" });
  }
  const sign = delta.points > 0 ? "+" : "";
  return el("span", { class: `move ${moveClass(delta.direction)}`,
                      text: `${arrow(delta.direction)} ${sign}${delta.points}${suffix}` });
}

function quoteLine(q) {
  return el("p", { class: "quote" }, [
    el("button", { class: "linkish", text: `"${q.quote}"`,
                   onclick: () => openCall(q.call_id, q.quote) }),
  ]);
}

/** Section 1: volume and mix. */
function sectionChanged(d) {
  const out = el("div", {});
  out.appendChild(el("div", { class: "weekly-stats" }, [
    stat(num(d.n_calls), "contacts this week"),
    stat(num(d.n_calls_previous_week), "the week before"),
    stat(String(d.four_week_average), "four-week average"),
    stat(String(d.n_new_this_week), "themes new this week"),
  ]));
  const versus = el("p", { class: "footnote" }, [
    document.createTextNode("Against the four-week average: "), movement(d.vs_four_week_average, ""),
  ]);
  out.appendChild(versus);

  for (const r of d.reasons || []) {
    out.appendChild(el("div", { class: "row" }, [
      el("div", { class: "row-head" }, [
        el("span", { class: "row-name", text: r.label }),
        el("span", { class: "row-meta" }, [
          document.createTextNode(`${num(r.n_calls)} · ${pctOf(r.share_pct)}  `),
          movement(r.vs_previous_week),
        ]),
      ]),
      r.top_specific?.length ? el("p", { class: "quote", text: r.top_specific[0] }) : null,
    ]));
  }
  if (d.new_this_week?.length) {
    out.appendChild(el("h3", { class: "weekly-sub", text: "New to this week" }));
    for (const t of d.new_this_week) {
      out.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [
          el("button", { class: "linkish row-name", text: t.name, onclick: () => openTheme(t.theme_id) }),
          el("span", { class: "row-meta", text: plural(t.n_calls, "call") }),
        ]),
      ]));
    }
  }
  return out;
}

/** Section 2: what drove frustration and satisfaction. */
function sectionFeeling(d) {
  const out = el("div", {});
  for (const [key, title] of [["negative", "Frustration"], ["positive", "Satisfaction"]]) {
    const rows = d[key] || [];
    out.appendChild(el("h3", { class: "weekly-sub", text: title }));
    if (!rows.length && key === "positive" && (d.positive_moments || []).length) {
      for (const m of d.positive_moments) {
        out.appendChild(el("div", { class: "row" }, [
          el("div", { class: "row-head" }, [
            el("span", { class: "row-name", text: label(m.category) }),
            el("span", { class: "row-meta", text: plural(m.n_calls, "call") }),
          ]),
          (m.quotes || [])[0] ? quoteLine(m.quotes[0]) : null,
        ]));
      }
      continue;
    }
    if (!rows.length) {
      out.appendChild(el("p", { class: "muted", text: "nothing above minimum support this week" }));
      continue;
    }
    for (const r of rows) {
      out.appendChild(el("div", { class: "row" }, [
        el("div", { class: "row-head" }, [
          r.theme_id
            ? el("button", { class: "linkish row-name", text: r.name, onclick: () => openTheme(r.theme_id) })
            : el("span", { class: "row-name", text: r.name }),
          el("span", { class: "row-meta", text: `${plural(r.n_calls, "call")} · mean ${r.mean_sentiment}` }),
        ]),
        r.triggers?.length ? el("p", { class: "trigger", text: r.triggers[0] }) : null,
        (r.quotes || [])[0] ? quoteLine(r.quotes[0]) : null,
      ]));
    }
  }
  return out;
}

/** Section 3: what to act on first. */
function sectionAttention(d) {
  const out = el("div", {});
  if (!d.rows?.length) {
    out.appendChild(el("p", { class: "muted",
      text: `Nothing cleared the threshold this week. ${num(d.n_tested)} themes were testable.` }));
  }
  for (const r of d.rows || []) {
    const asks = (r.customer_asks || []).map((a) => `${label(a.value)} ${pctOf(a.share_pct)}`).join(" · ");
    out.appendChild(el("div", { class: "row" }, [
      el("div", { class: "row-head" }, [
        el("button", { class: "linkish row-name", text: r.name, onclick: () => openTheme(r.theme_id) }),
        el("span", { class: "pill " + (r.status || ""), text: (r.status || "").toUpperCase() }),
      ]),
      el("p", { class: "footnote",
        text: `${num(r.n_recent)} in the last four weeks against ${Number(r.expected_recent).toFixed(1)} expected`
              + ` · z ${Number(r.z).toFixed(1)}`
              + (r.robust_8w ? " · robust at 8 weeks" : "")
              + (r.first_seen_week ? ` · first seen ${r.first_seen_week}` : "") }),
      r.root_cause ? el("p", { class: "trigger", text: r.root_cause }) : null,
      asks ? el("p", { class: "footnote", text: `What they asked for: ${asks}` }) : null,
    ]));
  }
  if (d.expected_false_positives !== undefined && d.expected_false_positives !== null) {
    out.appendChild(el("p", { class: "footnote",
      text: `${Number(d.expected_false_positives).toFixed(2)} of ${num(d.n_tested)} themes tested would`
            + ` pass this threshold by chance.` }));
  }
  return out;
}

/** Section 4: the words themselves, and what they cannot bear. */
function sectionSupporting(d) {
  const out = el("div", {});
  for (const g of d.groups || []) {
    out.appendChild(el("div", { class: "row" }, [
      el("div", { class: "row-head" }, [
        el("button", { class: "linkish row-name", text: g.name, onclick: () => openTheme(g.theme_id) }),
        el("span", { class: "row-meta",
          text: `${plural(g.n_distinct_calls, "distinct call")}${g.window && g.window.includes("..") ? ` · ${g.window}` : ""}` }),
      ]),
      ...(g.quotes || []).map(quoteLine),
    ]));
  }
  if (d.limits?.length) {
    out.appendChild(el("h3", { class: "weekly-sub", text: "What this evidence cannot bear" }));
    const list = el("ul", { class: "limits" });
    for (const l of d.limits) list.appendChild(el("li", { text: l }));
    out.appendChild(list);
  }
  return out;
}

const RENDER = { changed: sectionChanged, drove_feeling: sectionFeeling,
                 needs_attention: sectionAttention, supporting: sectionSupporting };

function stat(value, caption) {
  return el("div", { class: "weekly-stat" }, [
    el("strong", { text: value }), el("span", { text: caption }),
  ]);
}

async function render(week) {
  const body = document.getElementById("weeklyBody");
  clear(body).appendChild(el("p", { class: "muted", text: "reading the week…" }));
  let payload;
  try {
    payload = await api.weekly(week);
  } catch (err) {
    clear(body).appendChild(el("p", { class: "muted", text: `could not load: ${err.message}` }));
    return;
  }
  current = payload.week;
  document.getElementById("weeklyRange").textContent =
    `${payload.week} · ${payload.week_start} to ${payload.week_end}`;
  const pick = document.getElementById("weekPick");
  if (pick.value !== current) pick.value = current;

  const out = clear(body);
  for (const [key, question, blurb] of QUESTIONS) {
    const section = payload.sections[key];
    out.appendChild(el("article", { class: "weekly-section" }, [
      el("h2", { text: question }),
      el("p", { class: "muted", text: blurb }),
      section ? RENDER[key](section) : el("p", { class: "muted", text: "unavailable" }),
    ]));
  }
}

function step(delta) {
  const i = weeks.indexOf(current);
  if (i < 0) return;
  const next = weeks[i + delta];
  if (next) render(next);
}

export async function initWeekly(defaultWeek) {
  const panel = document.getElementById("weekly");
  const pick = document.getElementById("weekPick");
  document.getElementById("weeklyBtn").addEventListener("click", async () => {
    panel.hidden = false;
    document.querySelector("main").hidden = true;
    if (!weeks.length) {
      weeks = (await api.weeks()).weeks || [];
      clear(pick);
      for (const w of weeks) pick.appendChild(el("option", { value: w, text: w }));
    }
    render(current || defaultWeek || weeks[weeks.length - 1]);
  });
  document.getElementById("weeklyClose").addEventListener("click", () => {
    panel.hidden = true;
    document.querySelector("main").hidden = false;
  });
  pick.addEventListener("change", () => render(pick.value));
  document.getElementById("weekPrev").addEventListener("click", () => step(-1));
  document.getElementById("weekNext").addEventListener("click", () => step(1));
}
