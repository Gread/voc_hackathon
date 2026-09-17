// Thin fetch layer. Every call carries the current filters and as-of week.

async function getJSON(path, params = {}) {
  const url = new URL(path, window.location.origin);
  for (const [key, value] of Object.entries(params)) {
    if (value === null || value === undefined || value === "") continue;
    if (Array.isArray(value)) { if (value.length) url.searchParams.set(key, value.join(",")); }
    else url.searchParams.set(key, String(value));
  }
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch { /* not JSON */ }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

export const api = {
  meta: () => getJSON("/api/meta"),
  overview: (f) => getJSON("/api/overview", f),
  reasons: (f) => getJSON("/api/reasons", { ...f, compare: 1 }),
  themes: (f, opts = {}) => getJSON("/api/themes", { ...f, ...opts }),
  theme: (id, f) => getJSON(`/api/themes/${encodeURIComponent(id)}`, f),
  trend: (ids, grain, f) => getJSON("/api/trend", { ...f, ids: ids.join(","), grain }),
  emerging: (f, opts = {}) => getJSON("/api/emerging", { ...f, ...opts }),
  drivers: (f, opts = {}) => getJSON("/api/drivers", { ...f, ...opts }),
  breakdown: (f, opts = {}) => getJSON("/api/breakdown", { ...f, ...opts }),
  quotes: (f, opts = {}) => getJSON("/api/quotes", { ...f, ...opts }),
  search: (q, f) => getJSON("/api/search", { ...f, q }),
  call: (id) => getJSON(`/api/calls/${encodeURIComponent(id)}`),
  resultRows: (resultId, qhash) => getJSON(`/api/results/${encodeURIComponent(resultId)}/rows` + (qhash ? `?qhash=${encodeURIComponent(qhash)}` : "")),
  questions: () => getJSON("/api/questions"),
  weekly: (week) => getJSON("/api/weekly", week ? { week } : {}),
  weeks: () => getJSON("/api/weeks"),
  answer: (qhash) => getJSON(`/api/answers/${encodeURIComponent(qhash)}`),
};

// POST + ReadableStream: EventSource cannot send a body.
export async function askStream(body, onEvent, signal) {
  const res = await fetch("/api/ask", {
    method: "POST", signal,
    headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify(body),
  });
  if (!res.ok || !res.body) throw new Error(`ask failed: ${res.status}`);
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let split;
    while ((split = buffer.indexOf("\n\n")) >= 0) {
      const block = buffer.slice(0, split);
      buffer = buffer.slice(split + 2);
      let name = "";
      const data = [];
      for (const line of block.split("\n")) {
        if (line.startsWith("event: ")) name = line.slice(7).trim();
        else if (line.startsWith("data: ")) data.push(line.slice(6));
      }
      if (!name) continue;
      let payload = {};
      try { payload = data.length ? JSON.parse(data.join("\n")) : {}; } catch { payload = { raw: data.join("\n") }; }
      onEvent(name, payload);
    }
  }
}
