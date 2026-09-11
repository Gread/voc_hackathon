// Filters and as-of week live in the URL so any view can be shared or reloaded.

const LIST_KEYS = ["product", "segment", "region_group", "channel", "region", "company"];
const SCALAR_KEYS = ["date_from", "date_to", "as_of"];
const listeners = new Set();

export const state = { filters: {}, asOf: null, dev: false };

export function readURL() {
  const params = new URLSearchParams(window.location.search);
  const filters = {};
  for (const key of LIST_KEYS) {
    const raw = params.get(key);
    if (raw) filters[key] = raw.split(",").filter(Boolean);
  }
  for (const key of SCALAR_KEYS.slice(0, 2)) {
    if (params.get(key)) filters[key] = params.get(key);
  }
  state.filters = filters;
  state.asOf = params.get("as_of") || null;
  state.dev = params.get("dev") === "1";
  document.body.classList.toggle("dev", state.dev);
  return state;
}

export function writeURL(replace = false) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(state.filters)) {
    if (Array.isArray(value) ? value.length : value) params.set(key, Array.isArray(value) ? value.join(",") : value);
  }
  if (state.asOf) params.set("as_of", state.asOf);
  if (state.dev) params.set("dev", "1");
  const url = `${window.location.pathname}${params.toString() ? "?" + params : ""}`;
  if (replace) window.history.replaceState({}, "", url);
  else window.history.pushState({}, "", url);
}

/** Query parameters for the API: the filters plus the as-of week. */
export function queryParams() {
  const out = { ...state.filters };
  if (state.asOf) out.as_of = state.asOf;
  return out;
}

export function setFilter(key, value) {
  if (Array.isArray(value) ? !value.length : !value) delete state.filters[key];
  else state.filters[key] = value;
  writeURL();
  emit("filters");
}

export function clearFilters() {
  state.filters = {};
  writeURL();
  emit("filters");
}

export function setAsOf(week) {
  state.asOf = week || null;
  writeURL(true);
  emit("asof");
}

export function onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); }

export function emit(reason) { for (const fn of listeners) fn(reason); }

export function describeFilters() {
  const parts = Object.entries(state.filters).map(([k, v]) =>
    `${k.replace(/_/g, " ")}: ${Array.isArray(v) ? v.join(", ") : v}`);
  return parts.length ? parts.join(" · ") : "all calls";
}

window.addEventListener("popstate", () => { readURL(); emit("popstate"); });
