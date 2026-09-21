// The left rail is the only place a section is chosen.
// Weekly keeps its own show/hide, so this module only puts the page back when you navigate away.

// `asOf` says whether the as-of slider does anything in that view. It is not decoration: the graph
// query ignores as_of entirely - the same call with and without it returns identical rows - and the
// weekly review carries its own week picker, so a second time control beside it only contradicts it.
// A knob that changes nothing is worse than no knob, because it invites you to trust what it says.
// Ask is different and keeps it: as_of is part of the answer's cache identity, so moving it really
// does change the answer.
const VIEWS = {
  navOverview: { view: "viewOverview", title: "Overview", asOf: true,
                 sub: "Every number opens the conversations behind it." },
  navGraph: { view: "viewGraph", title: "Theme graph", asOf: false,
              sub: "A link means conversations that raised both themes." },
  navAsk: { view: "viewAsk", title: "Ask", asOf: true,
            sub: "Every claim is recounted from the calls it cites before it is shown." },
};
const WEEKLY = { title: "The weekly customer review",
                 sub: "One week of contacts, answered as four questions." };

let hooks = {};

function head(title, sub, asOf) {
  document.getElementById("pageTitle").textContent = title;
  document.getElementById("pageSub").textContent = sub;
  document.querySelector(".asof").hidden = !asOf;
}

export function show(id) {
  for (const b of document.querySelectorAll(".rail-nav button")) b.classList.toggle("on", b.id === id);
  const target = VIEWS[id];
  if (!target) {                       // weekly reveals itself; only the page chrome is ours
    head(WEEKLY.title, WEEKLY.sub, false);
    return;
  }
  document.getElementById("weekly").hidden = true;
  document.querySelector("main").hidden = false;
  for (const key of Object.keys(VIEWS)) document.getElementById(VIEWS[key].view).hidden = key !== id;
  head(target.title, target.sub, target.asOf);
  if (hooks[id]) hooks[id]();
}

export function initNav(enterHooks = {}) {
  hooks = enterHooks;
  for (const id of [...Object.keys(VIEWS), "weeklyBtn"]) {
    document.getElementById(id).addEventListener("click", () => show(id));
  }
  // weekly.js already restores main here; this only moves the rail's highlight with it.
  document.getElementById("weeklyClose").addEventListener("click", () => show("navOverview"));
}
