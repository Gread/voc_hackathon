// Chart.js wrappers. Colours come from the CSS variables so both themes stay consistent.

const charts = new Map();

function cssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

function palette() {
  return [cssVar("--accent", "#b4530a"), cssVar("--neg", "#a8322a"), cssVar("--pos", "#2f6b46"),
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
export function barsChart(canvasId, rows, { horizontal = true, tone = "accent" } = {}) {
  const color = cssVar(`--${tone}`, "#b4530a");
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

export function destroyAll() {
  for (const chart of charts.values()) chart.destroy();
  charts.clear();
}
