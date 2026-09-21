// Chart.js wrappers. Colours come from the CSS variables so both themes stay consistent.

const charts = new Map();

function cssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

function palette() {
  // --accent was never a defined token (styles.css only has --brand), so every trend line's first
  // series silently fell back to this hardcoded orange instead of the bank's own brand colour.
  return [cssVar("--brand", "#005aa0"), cssVar("--neg", "#a8322a"), cssVar("--pos", "#2f6b46"),
          "#6b6ba8", "#a87f2f", "#3f7f8a"];
}

function baseOptions() {
  const ink = cssVar("--ink-soft", "#5b5850");
  const line = cssVar("--line", "#e4e1da");
  return {
    responsive: true, maintainAspectRatio: false, animation: { duration: 220 },
    interaction: { mode: "index", intersect: false },
    plugins: {
      legend: { labels: { color: ink, boxWidth: 10, font: { size: 11 } } },
      tooltip: { backgroundColor: cssVar("--panel", "#fff"), titleColor: cssVar("--ink", "#000"),
                 bodyColor: ink, borderColor: line, borderWidth: 1 },
    },
    scales: {
      x: { ticks: { color: ink, font: { size: 10 }, maxRotation: 0, autoSkipPadding: 12 }, grid: { color: line } },
      y: { ticks: { color: ink, font: { size: 10 } }, grid: { color: line }, beginAtZero: true },
    },
  };
}

function render(canvasId, config) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof window.Chart === "undefined") return null;
  charts.get(canvasId)?.destroy();
  const chart = new window.Chart(canvas.getContext("2d"), config);
  charts.set(canvasId, chart);
  return chart;
}

/** series: [{label, points: [{period, share, n_calls}]}] */
export function trendChart(canvasId, series, { asOf = null, valueKey = "share" } = {}) {
  const colors = palette();
  const periods = [...new Set(series.flatMap((s) => s.points.map((p) => p.period)))].sort();
  const datasets = series.map((s, i) => {
    const byPeriod = new Map(s.points.map((p) => [p.period, p]));
    return {
      label: s.label,
      data: periods.map((p) => {
        const point = byPeriod.get(p);
        if (!point) return null;
        const v = point[valueKey];
        return valueKey === "share" ? Number(((v <= 1 ? v * 100 : v) || 0).toFixed(2)) : v;
      }),
      borderColor: colors[i % colors.length],
      backgroundColor: colors[i % colors.length] + "22",
      borderWidth: 2, pointRadius: 2, tension: 0.25, spanGaps: true, fill: false,
    };
  });
  return render(canvasId, {
    type: "line",
    data: { labels: periods, datasets },
    options: {
      ...baseOptions(),
      plugins: {
        ...baseOptions().plugins,
        tooltip: {
          ...baseOptions().plugins.tooltip,
          callbacks: {
            label: (ctx) => {
              const s = series[ctx.datasetIndex];
              const point = s?.points.find((p) => p.period === ctx.label);
              const value = valueKey === "share" ? `${ctx.formattedValue}%` : ctx.formattedValue;
              return `${s?.label}: ${value}` + (point?.n_calls !== undefined ? ` (${point.n_calls} calls)` : "");
            },
          },
        },
      },
      scales: {
        ...baseOptions().scales,
        y: { ...baseOptions().scales.y,
             title: { display: true, text: valueKey === "share" ? "share of calls (%)" : "calls",
                      color: cssVar("--muted", "#888"), font: { size: 10 } } },
      },
    },
  });
}

/** rows: [{label, value, n}] */
export function barsChart(canvasId, rows, { horizontal = true, tone = "brand" } = {}) {
  const color = cssVar(`--${tone}`, "#005aa0");
  return render(canvasId, {
    type: "bar",
    data: {
      labels: rows.map((r) => r.label),
      datasets: [{ label: "calls", data: rows.map((r) => r.value), backgroundColor: color + "cc",
                   borderColor: color, borderWidth: 1, borderRadius: 3 }],
    },
    options: {
      ...baseOptions(), indexAxis: horizontal ? "y" : "x",
      plugins: { ...baseOptions().plugins, legend: { display: false } },
    },
  });
}

/** Composition of contact reasons as a doughnut: the one question here that is genuinely
 *  parts-of-a-whole ("what is the mix?"), which a ranked bar list answers less directly.
 *
 *  Ranking still belongs to the bars - angles are hard to compare - so this sits beside them
 *  rather than replacing them. Long tails are collapsed into one "Other" slice, because a
 *  doughnut with fifteen slivers reads as decoration.
 *
 *  Monochrome blue ramp rather than a rainbow: the categories have no inherent colour meaning,
 *  and a ramp keeps it on brand and readable for anyone who can't separate hues.
 */
const RAMPS = {
  brand: ["#00315c", "#00427a", "#005aa0", "#3d87bd", "#7fb3d9", "#b6d7ee"],
  neg: ["#5c0210", "#870315", "#b8041c", "#e40523", "#ef5b6b", "#f7a3ac"],
  pos: ["#1f3b1b", "#2d4a27", "#3e6237", "#5a8450", "#86ad7c", "#b7d0b0"],
};

export function donutChart(canvasId, rows, { top = 6, ramp = "brand" } = {}) {
  const RAMP = RAMPS[ramp] || RAMPS.brand;
  const sorted = [...rows].sort((a, b) => (b.value || 0) - (a.value || 0));
  const head = sorted.slice(0, top);
  const tail = sorted.slice(top);
  const tailTotal = tail.reduce((sum, r) => sum + (Number(r.value) || 0), 0);
  const labels = head.map((r) => r.label);
  const values = head.map((r) => Number(r.value) || 0);
  if (tailTotal > 0) { labels.push(`Other (${tail.length})`); values.push(tailTotal); }
  const colors = labels.map((_, i) => (tailTotal > 0 && i === labels.length - 1
    ? cssVar("--neutral", "#7a7a7a") : RAMP[i % RAMP.length]));
  const total = values.reduce((a, b) => a + b, 0) || 1;

  return render(canvasId, {
    type: "doughnut",
    data: { labels, datasets: [{ data: values, backgroundColor: colors, borderColor: cssVar("--panel", "#fff"), borderWidth: 2 }] },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: "58%",
      animation: { duration: 500 },
      plugins: {
        legend: {
          position: "right",
          labels: {
            color: cssVar("--ink", "#292929"), boxWidth: 12, padding: 10, font: { size: 12 },
            // Theme names are whole sentences ("claim denied on your records, my evidence never
            // looked at"), which the legend clips mid-word in a half-width panel. Shorten here
            // only - the slice keeps its full name, so the tooltip still reads in full.
            generateLabels(chart) {
              const base = window.Chart.overrides.doughnut.plugins.legend.labels.generateLabels(chart);
              return base.map((item) => ({
                ...item,
                text: item.text.length > 30 ? `${item.text.slice(0, 29).trimEnd()}…` : item.text,
              }));
            },
          },
        },
        tooltip: {
          backgroundColor: cssVar("--panel", "#fff"), titleColor: cssVar("--ink", "#000"),
          bodyColor: cssVar("--ink-soft", "#666"), borderColor: cssVar("--line", "#d6d6d6"), borderWidth: 1,
          callbacks: {
            label: (ctx) => `${ctx.label}: ${ctx.parsed.toLocaleString("en-US")} calls `
              + `(${((ctx.parsed / total) * 100).toFixed(1)}%)`,
          },
        },
      },
    },
  });
}

/** A theme's own trajectory as an inline SVG sparkline, for the Emerging panel.
 *
 *  It replaces a bar that couldn't say anything: that bar was scaled against the largest row, so
 *  when every emerging theme sat at 5 calls, every bar rendered full width. A line shows the shape
 *  the emerging score is actually reacting to - flat for months, then a climb - which is the one
 *  thing a reader needs to see without being taught the statistics.
 *
 *  Inline SVG rather than Chart.js: there are one of these per row, they carry no axes or
 *  interaction, and an <svg> costs no canvas, no instance to destroy, and stays crisp when zoomed.
 */
export function sparkline(points, { weeks = 26, recent = 4, width = 900, height = 64 } = {}) {
  const tail = points.slice(-weeks);
  const values = tail.map((p) => Number(p.n_calls) || 0);
  const max = Math.max(1, ...values);
  const stepX = tail.length > 1 ? width / (tail.length - 1) : width;
  const pad = 4;
  const y = (v) => pad + (height - pad * 2) * (1 - v / max);
  const xy = values.map((v, i) => [i * stepX, y(v)]);
  const path = xy.map(([x, yy], i) => `${i ? "L" : "M"}${x.toFixed(1)},${yy.toFixed(1)}`).join(" ");
  const splitAt = Math.max(0, xy.length - recent - 1);
  const recentPath = xy.slice(splitAt).map(([x, yy], i) => `${i ? "L" : "M"}${x.toFixed(1)},${yy.toFixed(1)}`).join(" ");
  const area = `${path} L${width},${height} L0,${height} Z`;
  const last = xy[xy.length - 1] || [0, height];
  const firstWeek = tail[0]?.period ?? "";
  const lastWeek = tail[tail.length - 1]?.period ?? "";
  const peak = Math.max(...values);

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("width", String(width));
  svg.setAttribute("height", String(height));
  svg.setAttribute("class", "sparkline");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label",
    `Weekly calls from ${firstWeek} to ${lastWeek}, peaking at ${peak}. The last ${recent} weeks are highlighted.`);
  svg.innerHTML =
    `<path d="${area}" fill="var(--brand-soft)"></path>` +
    `<path class="spark-line" d="${path}" fill="none" stroke="var(--neutral)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"></path>` +
    `<path class="spark-recent" d="${recentPath}" fill="none" stroke="var(--neg)" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"></path>` +
    `<circle class="spark-dot" cx="${last[0].toFixed(1)}" cy="${last[1].toFixed(1)}" r="4.5" fill="var(--neg)"></circle>`;
  return svg;
}

/** The same pivot trendChart() does internally, exposed so a text table can show exactly what the
 *  canvas draws - Chart.js renders to a bitmap, invisible to assistive tech and with no fallback
 *  content of its own, so the table is the honest alternative rather than a decorative extra. */
export function seriesToTable(series, valueKey = "share") {
  const periods = [...new Set(series.flatMap((s) => s.points.map((p) => p.period)))].sort();
  const columns = ["Period", ...series.map((s) => s.label)];
  const rows = periods.map((p) => [p, ...series.map((s) => {
    const point = s.points.find((pt) => pt.period === p);
    if (!point) return "-";
    const v = point[valueKey];
    return valueKey === "share" ? `${((v <= 1 ? v * 100 : v) || 0).toFixed(1)}%` : String(v ?? "-");
  })]);
  return { columns, rows };
}

export function destroyAll() {
  for (const chart of charts.values()) chart.destroy();
  charts.clear();
}
