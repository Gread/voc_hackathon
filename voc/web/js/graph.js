// The theme graph: themes as spheres, conversations that raised two of them as tubes.
// three.js is fetched on first visit, not at boot — it is 600 kB for one view.

import { api } from "./api.js";
import { clear, el, num } from "./format.js";
import { onChange, queryParams } from "./state.js";
import { openTheme } from "./themecard.js";

const HEIGHT = 560;
const LIMIT = 16;

let three = null;      // the loaded library
let pending = null;    // in-flight load
let scene = null;      // everything we built, or null before the first visit
let stale = true;
let selected = null;
let nearSet = new Set();
let labelsOn = true;
let labelsLinkedOnly = false;
let flagOn = true;

const FLAG_DIST = 620;      // how far in front of the camera the cloth hangs
let symbolImg = null;

/** The official LF symbol, the file lansforsakringar.se itself serves — never traced from a photo. */
function loadSymbol() {
  if (symbolImg) return Promise.resolve(symbolImg);
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => { symbolImg = img; resolve(img); };
    img.onerror = () => resolve(null);          // no flag is better than a broken one
    img.src = "/static/img/lf-symbol.png";
  });
}

/** White field with the symbol centred, drawn at the panel's own aspect so the mark stays square.
 *  Stretching one fixed texture to fill a wide panel would squash the logo, which we will not do. */
function flagTexture(T, w, h) {
  const c = document.createElement("canvas");
  c.height = 640;
  c.width = Math.max(64, Math.round(640 * (w / h)));
  const g = c.getContext("2d");
  g.fillStyle = "#ffffff";
  g.fillRect(0, 0, c.width, c.height);
  if (symbolImg) {
    // Full-bleed puts the mark dead centre, under the densest part of the graph. The field stays
    // at full strength so it still reads as cloth; the mark softens so the data stays on top of it.
    const side = Math.round(Math.min(c.width, c.height) * 0.76);
    g.globalAlpha = 0.55;
    g.drawImage(symbolImg, Math.round((c.width - side) / 2), Math.round((c.height - side) / 2), side, side);
    g.globalAlpha = 1;
  }
  return new T.CanvasTexture(c);
}

function loadThree() {
  if (three) return Promise.resolve(three);
  if (!pending) {
    pending = new Promise((resolve, reject) => {
      const tag = document.createElement("script");
      tag.src = "/static/vendor/three.min.js";
      tag.onload = () => { three = window.THREE; resolve(three); };
      tag.onerror = () => reject(new Error("could not load /static/vendor/three.min.js"));
      document.head.appendChild(tag);
    });
  }
  return pending;
}

/** Colour by how angry the theme reads, on the LFDS scale. */
function colorFor(sentiment) {
  const s = Number(sentiment);
  if (!Number.isFinite(s)) return 0x7a7a7a;
  if (s >= 0) return 0x3e6237;
  if (s <= -1.35) return 0x870315;
  if (s <= -1.2) return 0xe40523;
  return 0xeb5c5c;
}

function radiusFor(nCalls) {
  return 2.6 + Math.sqrt(Math.max(1, nCalls)) / 3;
}

/** Play the weeks over a graph that does not move.
 *
 *  Only radius and glow change. The layout stays exactly where the all-time graph put it, because
 *  a node that drifts while the weeks run cannot be told apart from a node that grew, and the whole
 *  point of playing it is to see which themes swell and when.
 *
 *  A week with no calls for a theme shrinks it to the floor rather than hiding it: an empty week is
 *  information, and a sphere that vanishes reads as a rendering fault.
 */
function playback(nodes, meshes, tubes, T, payload) {
  const row = document.getElementById("graphPlay");
  const weeks = (payload.data || {}).weeks || [];
  if (weeks.length < 2) { row.hidden = true; return null; }

  const at = new Map();                           // theme_id -> Map(week index -> n_calls)
  const wi = new Map(weeks.map((w, i) => [w, i]));
  for (const r of payload.rows || []) {
    if (!at.has(r.theme_id)) at.set(r.theme_id, new Map());
    at.get(r.theme_id).set(wi.get(r.week), r.n_calls);
  }

  // A trailing four-week window, not the single week. Two reasons, and the second is the real one:
  // a theme sees a median of 2 calls in a week, which is mostly noise, and four weeks is exactly the
  // n_recent the emerging scores are computed over. When a sphere lights up for "5 calls where 0.83
  // were expected", it should be showing the same window that number was measured on.
  const WINDOW = 4;
  const win = new Map();                          // theme_id -> array by week index
  const all = [];
  for (const n of nodes) {
    const series = at.get(n.theme_id) || new Map();
    const out = new Array(weeks.length);
    for (let i = 0; i < weeks.length; i++) {
      let s = 0;
      for (let j = Math.max(0, i - WINDOW + 1); j <= i; j++) s += series.get(j) || 0;
      out[i] = s;
      all.push(s);
    }
    win.set(n.theme_id, out);
  }

  // Scale against the 95th percentile, not the maximum: the busiest window is 357 against a p95 of
  // 16, and normalising to that outlier would flatten every ordinary week into the same small dot.
  // Anything above the cap simply pegs at full size.
  all.sort((a, b) => a - b);
  const cap = Math.max(4, all[Math.floor(all.length * 0.95)] || 4);

  // radiusFor is built for all-time counts, where its 2.6 floor is a small part of a radius of 9.
  // At weekly counts that floor is nearly all of it, so a busy week differed from a dead one by 7%
  // of the radius - invisible. This spans the weekly range instead, from a quarter size to nearly
  // double, which is a seven-fold swing you can actually watch.
  const scaleFor = (n) => 0.25 + 1.45 * Math.sqrt(Math.min(n, cap) / cap);

  // Sizing by raw volume barely reorders anything: the 366-call theme is large every week and the
  // 30-call one is small every week, so the picture that moves least is the one you are watching for
  // movement. Against its own normal, every theme sits near the same middling size when it is
  // behaving, and only the ones running hot or cold change - which is the question the view is for,
  // and the same question the orange flags answer. The reference is the theme's median active
  // window, so one quiet spell does not redefine what normal means for it.
  const ref = {};
  for (const n of nodes) {
    const active = win.get(n.theme_id).filter((v) => v > 0).sort((a, b) => a - b);
    ref[n.theme_id] = active.length ? Math.max(1, active[Math.floor(active.length / 2)]) : 1;
  }
  const relativeFor = (n, id) => 0.22 + 0.62 * Math.min(n / ref[id], 3);

  const modeSel = document.getElementById("playMode");
  const flags = (payload.data || {}).flags || {};

  const range = document.getElementById("weekRange");
  const label = document.getElementById("weekLabel");
  const playBtn = document.getElementById("playBtn");
  range.max = String(weeks.length - 1);
  row.hidden = false;

  let timer = null;
  let current = -1;            // -1 is the whole corpus; the mode switch has to know which

  const show = (idx) => {
    current = idx;
    const whole = idx < 0;
    const week = whole ? null : weeks[idx];
    const hot = new Set((flags[week] || []).map((f) => f.theme_id));
    const relative = modeSel.value === "relative";
    let shown = 0;
    for (const n of nodes) {
      const mesh = meshes[n.theme_id];
      if (!mesh) continue;
      const seen = whole ? 0 : win.get(n.theme_id)[idx];
      shown += seen;
      mesh.scale.setScalar(whole ? 1 : (relative ? relativeFor(seen, n.theme_id) : scaleFor(seen)));
      // Orange is the one colour not in the sentiment scale, so a flag cannot be read as a mood.
      mesh.material.emissive = new T.Color(!whole && hot.has(n.theme_id) ? 0xff7a1a : 0x000000);
      mesh.material.emissiveIntensity = 0.9;
    }
    // The links are drawn at all-time weight. Left at that while the spheres shrink they hold the
    // eye and the motion is lost behind them, so they step back for the weeks and return for the whole.
    for (const t of tubes) t.material.opacity = whole ? 0.28 : 0.08;

    label.textContent = whole ? "All time"
      : `${week} · ${num(shown)} in 4 wks${hot.size ? ` · ${hot.size} above baseline` : ""}`;
    label.classList.toggle("hot", !whole && hot.size > 0);
  };

  const stop = () => { window.clearInterval(timer); timer = null; playBtn.textContent = "▶"; };
  playBtn.onclick = () => {
    if (timer) return stop();
    playBtn.textContent = "❚❚";
    timer = window.setInterval(() => {
      const next = (Number(range.value) + 1) % weeks.length;
      range.value = String(next);
      show(next);
    }, 260);
  };
  range.oninput = () => { stop(); show(Number(range.value)); };
  // Redraw in place rather than resetting: switching what size means should not lose your week.
  modeSel.onchange = () => show(current);
  document.getElementById("weekAll").onclick = () => { stop(); show(-1); };

  show(-1);
  return stop;
}

/** Stable pseudo-random from an id, so the same corpus always lays out the same way. */
function seed(id) {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) { h ^= id.charCodeAt(i); h = Math.imul(h, 16777619); }
  return Math.abs(h);
}

/** Force-directed in 3D: repulsion everywhere, springs along the links, run to a standstill.
 *  Deterministic — the starting points come from the ids, never from Math.random. */
function layout(nodes, edges) {
  const pos = {};
  nodes.forEach((n, i) => {
    const h = seed(n.theme_id);
    const a = ((h % 1000) / 1000) * Math.PI * 2;
    const b = Math.acos(2 * (((h >> 10) % 1000) / 1000) - 1);
    const r = 34 + (i % 4) * 5;
    pos[n.theme_id] = [r * Math.sin(b) * Math.cos(a), r * Math.sin(b) * Math.sin(a), r * Math.cos(b)];
  });
  const ids = nodes.map((n) => n.theme_id);
  const strongest = Math.max(1, ...edges.map((e) => e.n_calls));

  for (let step = 0; step < 300; step++) {
    const force = {};
    for (const id of ids) force[id] = [0, 0, 0];

    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = pos[ids[i]], b = pos[ids[j]];
        let dx = a[0] - b[0], dy = a[1] - b[1], dz = a[2] - b[2];
        const d2 = dx * dx + dy * dy + dz * dz || 0.01;
        const d = Math.sqrt(d2);
        const push = 6200 / d2;
        dx /= d; dy /= d; dz /= d;
        force[ids[i]][0] += dx * push; force[ids[i]][1] += dy * push; force[ids[i]][2] += dz * push;
        force[ids[j]][0] -= dx * push; force[ids[j]][1] -= dy * push; force[ids[j]][2] -= dz * push;
      }
    }
    for (const e of edges) {
      const a = pos[e.source], b = pos[e.target];
      if (!a || !b) continue;
      const dx = b[0] - a[0], dy = b[1] - a[1], dz = b[2] - a[2];
      const d = Math.sqrt(dx * dx + dy * dy + dz * dz) || 0.01;
      const rest = 26 + 30 * (1 - e.n_calls / strongest);   // stronger links sit closer
      const pull = (d - rest) * 0.055;
      force[e.source][0] += (dx / d) * pull; force[e.source][1] += (dy / d) * pull; force[e.source][2] += (dz / d) * pull;
      force[e.target][0] -= (dx / d) * pull; force[e.target][1] -= (dy / d) * pull; force[e.target][2] -= (dz / d) * pull;
    }
    const damp = 0.9 * (1 - step / 340);
    for (const id of ids) {
      for (let k = 0; k < 3; k++) {
        pos[id][k] += Math.max(-7, Math.min(7, force[id][k] * damp));
        pos[id][k] *= 0.994;                                  // a weak pull to the middle
      }
    }
  }
  return pos;
}

function sidePanel(node, links) {
  const side = clear(document.getElementById("graphSide"));
  if (!node) { side.appendChild(el("p", { class: "muted", text: "Pick a theme." })); return; }
  side.appendChild(el("h2", { text: node.name, style: "margin:0;font-size:19px;line-height:1.25" }));
  side.appendChild(el("div", { class: "graph-stats" }, [
    el("div", {}, [el("strong", { text: num(node.n_calls) }), el("span", { text: "conversations" })]),
    el("div", {}, [el("strong", { text: String(node.mean_sentiment ?? "—") }), el("span", { text: "mean sentiment" })]),
    el("div", {}, [el("strong", { text: String(node.n_links) }), el("span", { text: "linked themes" })]),
  ]));
  side.appendChild(el("h3", { class: "weekly-sub", text: "Raised in the same conversation as", style: "margin-top:0" }));
  if (!links.length) {
    side.appendChild(el("p", { class: "footnote",
      text: "No other theme in this view shares enough conversations to clear the link threshold." }));
  }
  for (const lk of links) {
    side.appendChild(el("div", { class: "row-head", style: "padding:4px 0" }, [
      el("button", { class: "linkish row-name", text: lk.name, onclick: () => select(lk.theme_id) }),
      el("span", { class: "row-meta", text: num(lk.n_calls) }),
    ]));
  }
  side.appendChild(el("div", { style: "flex-grow:1" }));
  // The card is where the calls, wordings and trend already live; duplicating them here would mean
  // a second place to keep honest.
  side.appendChild(el("button", { class: "ghost", style: "margin-top:14px",
                                  text: `Open the theme card · ${num(node.n_calls)} conversations`,
                                  onclick: () => openTheme(node.theme_id) }));
}

function paint() {
  if (!scene) return;
  const near = new Set();
  for (const e of scene.edges) {
    if (e.source === selected) near.add(e.target);
    if (e.target === selected) near.add(e.source);
  }
  nearSet = near;
  for (const [id, span] of Object.entries(scene.labels || {})) {
    span.classList.toggle("on", id === selected);
    span.classList.toggle("dim", !(id === selected || near.has(id)));
  }
  for (const [id, mesh] of Object.entries(scene.meshes)) {
    const lit = id === selected || near.has(id);
    mesh.material.emissive.setHex(id === selected ? 0x005aa0 : 0x000000);
    mesh.material.emissiveIntensity = id === selected ? 0.55 : 0;
    mesh.material.transparent = !lit;
    mesh.material.opacity = lit ? 1 : 0.34;
  }
  for (const tube of scene.tubes) {
    const on = tube.userData.pair.includes(selected);
    tube.material.color.setHex(on ? 0x005aa0 : 0x9aa7b2);
    tube.material.opacity = on ? 0.95 : 0.28;
  }
  for (const chip of document.querySelectorAll("#graphChips .chip")) {
    chip.classList.toggle("on", chip.dataset.theme === selected);
    chip.style.borderColor = chip.dataset.theme === selected ? "#005aa0" : "";
  }
}

function select(id) {
  if (!scene || !scene.byId[id]) return;
  selected = id;
  const links = scene.edges
    .filter((e) => e.source === id || e.target === id)
    .map((e) => { const other = e.source === id ? e.target : e.source;
                  return { theme_id: other, name: (scene.byId[other] || {}).name || other, n_calls: e.n_calls }; })
    .sort((a, b) => b.n_calls - a.n_calls);
  sidePanel(scene.byId[id], links);
  paint();
}

function teardown() {
  if (!scene) return;
  if (scene.stopPlay) scene.stopPlay();   // else the timer keeps resizing meshes that are gone
  scene.stop();
  scene = null;
}

async function build() {
  const T = await loadThree();
  const stage = document.getElementById("graphStage");
  const canvas = document.getElementById("graphCanvas");
  const payload = await api.graph(queryParams(), { limit: LIMIT });
  const nodes = payload.rows || [];
  const edges = (payload.data || {}).edges || [];
  teardown();

  if (nodes.length < 2) {
    clear(document.getElementById("graphSide")).appendChild(
      el("p", { class: "muted", text: "Not enough themes in this scope to draw a graph." }));
    return;
  }

  const width = Math.max(320, stage.clientWidth);
  const renderer = new T.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(width, HEIGHT, false);
  canvas.style.height = `${HEIGHT}px`;

  const world = new T.Scene();
  const fov = 45;
  const camera = new T.PerspectiveCamera(fov, width / HEIGHT, 1, 3000);
  world.add(new T.AmbientLight(0xffffff, 0.8));
  const key = new T.DirectionalLight(0xffffff, 0.55);
  key.position.set(50, 70, 110);
  world.add(key);
  const rim = new T.DirectionalLight(0xc0e5f8, 0.3);
  rim.position.set(-80, -40, -60);
  world.add(rim);

  const group = new T.Group();
  world.add(group);

  // The cloth is a child of the camera, hanging a fixed distance in front of it and cut to the
  // frustum at that distance. That is what makes it the whole backdrop: it cannot be orbited off
  // screen, and zooming the graph does not shrink it away from the panel edges.
  world.add(camera);
  let flag = null;
  let flagRest = null;
  let flagW = 0;
  let flagH = 0;

  const fitFlag = () => {
    if (!flag) return;
    flagH = 2 * Math.tan((fov / 2) * Math.PI / 180) * FLAG_DIST;
    flagW = flagH * camera.aspect;
    flag.geometry.dispose();
    flag.geometry = new T.PlaneGeometry(flagW, flagH, 56, 38);
    flagRest = flag.geometry.attributes.position.array.slice();
    if (flag.material.map) flag.material.map.dispose();
    flag.material.map = flagTexture(T, flagW, flagH);
    flag.material.needsUpdate = true;
  };

  loadSymbol().then(() => {
    if (!scene || scene.world !== world) return;                 // the view was rebuilt meanwhile
    flag = new T.Mesh(new T.PlaneGeometry(1, 1, 2, 2), new T.MeshStandardMaterial({
      side: T.DoubleSide, roughness: 0.92, metalness: 0,
      transparent: true, opacity: 0.92, depthWrite: false,
    }));
    flag.position.set(0, 0, -FLAG_DIST);
    flag.visible = flagOn;
    camera.add(flag);
    fitFlag();
    scene.flag = flag;
    scene.fitFlag = fitFlag;
  });

  /** Travelling sine waves in normalised cloth coordinates, so the ripple count stays the same
   *  whatever size the panel cuts the flag to. Pinned at the hoist: cloth on a pole, not a sheet. */
  const waveFlag = (t) => {
    if (!flag || !flagRest || !flag.visible || !flagW) return;
    const p = flag.geometry.attributes.position;
    const amp = flagH * 0.055;
    for (let i = 0; i < p.count; i++) {
      const x = flagRest[i * 3];
      const y = flagRest[i * 3 + 1];
      const u = (x + flagW / 2) / flagW;                          // 0 at the pole, 1 at the fly
      const v = (y + flagH / 2) / flagH;
      const slack = u * u;                                        // the far edge moves most
      p.array[i * 3 + 2] = (Math.sin(u * 8.5 + t * 2.1) * amp + Math.sin(v * 5.5 + t * 1.5) * amp * 0.45) * slack;
      p.array[i * 3 + 1] = y + Math.sin(u * 6.5 + t * 1.7) * amp * 0.35 * slack;
    }
    p.needsUpdate = true;
    flag.geometry.computeVertexNormals();
  };

  const pos = layout(nodes, edges);

  // Frame the graph from its own extent: the layout spreads differently with every filter, and a
  // fixed camera distance crops it or strands it in the middle of an empty stage.
  // Frame the body of the graph, not its furthest point: a theme with no links is pushed outwards
  // by repulsion with nothing pulling back, and framing to it shrinks everything else to nothing.
  const spread = nodes.map((n) => Math.hypot(...pos[n.theme_id])).sort((a, b) => a - b);
  const biggest = Math.max(...nodes.map((n) => radiusFor(n.n_calls)));
  const extent = Math.max(20, spread[Math.floor(spread.length * 0.85)] + biggest);
  const narrow = Math.min(1, camera.aspect);         // the narrow side decides what fits
  camera.position.set(0, 0, (extent / Math.tan((fov / 2) * Math.PI / 180) / narrow) * 1.05);

  const meshes = {};
  const byId = {};
  for (const n of nodes) {
    byId[n.theme_id] = n;
    const mesh = new T.Mesh(
      new T.SphereGeometry(radiusFor(n.n_calls), 32, 24),
      new T.MeshStandardMaterial({ color: colorFor(n.mean_sentiment), roughness: 0.42, metalness: 0.05 }));
    mesh.position.fromArray(pos[n.theme_id]);
    mesh.userData.id = n.theme_id;
    group.add(mesh);
    meshes[n.theme_id] = mesh;
  }

  const tubes = [];
  const up = new T.Vector3(0, 1, 0);
  const strongest = Math.max(1, ...edges.map((e) => e.n_calls));
  for (const e of edges) {
    const a = new T.Vector3().fromArray(pos[e.source]);
    const b = new T.Vector3().fromArray(pos[e.target]);
    const along = new T.Vector3().subVectors(b, a);
    const tube = new T.Mesh(
      new T.CylinderGeometry(0.22 + (e.n_calls / strongest) * 1.5, 0.22 + (e.n_calls / strongest) * 1.5,
                             along.length(), 8),
      new T.MeshStandardMaterial({ color: 0x9aa7b2, roughness: 0.6, transparent: true, opacity: 0.28 }));
    tube.position.copy(a).add(b).multiplyScalar(0.5);
    tube.quaternion.setFromUnitVectors(up, along.clone().normalize());
    tube.userData.pair = [e.source, e.target];
    group.add(tube);
    tubes.push(tube);
  }

  const ray = new T.Raycaster();
  const point = new T.Vector2();
  let dragging = false, moved = false, lastX = 0, lastY = 0;

  const down = (ev) => { dragging = true; moved = false; lastX = ev.clientX; lastY = ev.clientY; stage.classList.add("dragging"); };
  const move = (ev) => {
    if (!dragging) return;
    const dx = ev.clientX - lastX, dy = ev.clientY - lastY;
    if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
    group.rotation.y += dx * 0.006;
    group.rotation.x = Math.max(-1.2, Math.min(1.2, group.rotation.x + dy * 0.006));
    lastX = ev.clientX; lastY = ev.clientY;
  };
  const up_ = (ev) => {
    if (!dragging) return;
    dragging = false;
    stage.classList.remove("dragging");
    if (moved) return;
    const box = canvas.getBoundingClientRect();
    point.x = ((ev.clientX - box.left) / box.width) * 2 - 1;
    point.y = -((ev.clientY - box.top) / box.height) * 2 + 1;
    ray.setFromCamera(point, camera);
    const hit = ray.intersectObjects(Object.values(meshes), false)[0];
    if (hit) select(hit.object.userData.id);
  };
  const wheel = (ev) => {
    ev.preventDefault();
    camera.position.z = Math.max(80, Math.min(420, camera.position.z + ev.deltaY * 0.22));
  };

  canvas.addEventListener("pointerdown", down);
  window.addEventListener("pointermove", move);
  window.addEventListener("pointerup", up_);
  canvas.addEventListener("wheel", wheel, { passive: false });

  const resize = () => {
    const w = Math.max(320, stage.clientWidth);
    renderer.setSize(w, HEIGHT, false);
    camera.aspect = w / HEIGHT;
    camera.updateProjectionMatrix();
    fitFlag();                    // the backdrop is cut to the frustum, so it is re-cut here
  };
  window.addEventListener("resize", resize);

  // One span per sphere, projected onto the canvas each frame.
  const layer = clear(document.getElementById("graphLabels"));
  const labels = {};
  for (const n of nodes) {
    const span = el("span", { class: "graph-label", text: n.name, title: n.name });
    layer.appendChild(span);
    labels[n.theme_id] = span;
  }

  const probe = new T.Vector3();
  const halfFov = Math.tan((fov / 2) * Math.PI / 180);
  const placeLabels = () => {
    if (!labelsOn) { layer.hidden = true; return; }
    layer.hidden = false;
    const w = canvas.clientWidth || width;
    for (const n of nodes) {
      const span = labels[n.theme_id];
      const shown = !labelsLinkedOnly || n.theme_id === selected || nearSet.has(n.theme_id);
      if (!shown) { span.style.display = "none"; continue; }
      meshes[n.theme_id].getWorldPosition(probe);
      const dist = camera.position.distanceTo(probe);
      probe.project(camera);
      if (probe.z > 1) { span.style.display = "none"; continue; }   // behind the camera
      // The sphere's on-screen radius, so the label sits just under it however far away it is.
      const px = radiusFor(n.n_calls) * (HEIGHT / 2) / (halfFov * Math.max(1, dist));
      // A sphere this small is a dot; its name would be clutter over the graph, not a label on it.
      if (px < 4 && n.theme_id !== selected) { span.style.display = "none"; continue; }
      span.style.display = "";
      span.style.left = `${(probe.x * 0.5 + 0.5) * w}px`;
      span.style.top = `${(-probe.y * 0.5 + 0.5) * HEIGHT + px + 3}px`;
      span.style.zIndex = String(Math.max(0, 900 - Math.round(dist)));
    }
  };

  let frame = 0;
  let clock = 0;
  const tick = () => {
    clock += 1 / 60;
    if (!dragging) group.rotation.y += 0.0015;
    waveFlag(clock);
    renderer.render(world, camera);
    placeLabels();
    frame = window.requestAnimationFrame(tick);
  };

  scene = {
    meshes, tubes, byId, edges, resize, labels, placeLabels, world, flag: null,
    stop: () => {
      window.cancelAnimationFrame(frame);
      canvas.removeEventListener("pointerdown", down);
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up_);
      canvas.removeEventListener("wheel", wheel);
      window.removeEventListener("resize", resize);
      renderer.dispose();
    },
  };
  tick();                       // started after `scene` exists: the flag checks it on arrival

  const chips = clear(document.getElementById("graphChips"));
  for (const n of nodes) {
    const chip = el("button", { class: "chip", type: "button", text: n.name,
                                onclick: () => select(n.theme_id) });
    chip.dataset.theme = n.theme_id;
    chips.appendChild(chip);
  }
  select(nodes[0].theme_id);

  // Fetched after the scene is up so the graph draws immediately and playback arrives when ready.
  try {
    scene.stopPlay = playback(nodes, meshes, tubes, T,
                              await api.graphWeeks(queryParams(), { limit: LIMIT }));
  } catch {
    document.getElementById("graphPlay").hidden = true;   // no playback is fine; a broken graph is not
  }
}

export function initGraph() {
  const on = document.getElementById("labelsOn");
  const linked = document.getElementById("labelsLinkedOnly");
  labelsOn = on.checked;
  labelsLinkedOnly = linked.checked;
  on.addEventListener("change", () => {
    labelsOn = on.checked;
    linked.disabled = !labelsOn;
    if (scene) scene.placeLabels();
  });
  linked.addEventListener("change", () => {
    labelsLinkedOnly = linked.checked;
    if (scene) scene.placeLabels();
  });

  const flag = document.getElementById("flagOn");
  flagOn = flag.checked;
  flag.addEventListener("change", () => {
    flagOn = flag.checked;
    if (scene && scene.flag) scene.flag.visible = flagOn;
  });

  onChange((reason) => {
    if (reason === "asof") return;          // the graph is not an as-of view
    stale = true;
    if (!document.getElementById("viewGraph").hidden) showGraph();
  });
}

export async function showGraph() {
  const side = document.getElementById("graphSide");
  if (!stale && scene) { scene.resize(); return; }
  stale = false;
  clear(side).appendChild(el("p", { class: "muted", text: "building the graph…" }));
  try {
    await build();
  } catch (err) {
    stale = true;
    clear(side).appendChild(el("p", { class: "muted", text: `could not draw the graph: ${err.message}` }));
  }
}
