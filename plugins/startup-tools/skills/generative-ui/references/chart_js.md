# Chart.js Reference

Extracted from Claude's actual `visualize:read_me` guidelines.

---

## Basic Setup

```html
<div style="position: relative; width: 100%; height: 300px;">
  <canvas id="myChart"></canvas>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js" onload="initChart()"></script>
<script>
  function initChart() {
    new Chart(document.getElementById('myChart'), {
      type: 'bar',
      data: { labels: ['Q1','Q2','Q3','Q4'], datasets: [{ label: 'Revenue', data: [12,19,8,15] }] },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }
  if (window.Chart) initChart();
</script>
```

---

## Rules

### Canvas Sizing
- Set height ONLY on the wrapper div, never on the canvas element itself
- Use `position: relative` on the wrapper
- Use `responsive: true, maintainAspectRatio: false` in Chart.js options
- Never set CSS height directly on canvas — causes wrong dimensions, especially for horizontal bar charts
- For horizontal bar charts: wrapper div height = at least `(number_of_bars × 40) + 80` pixels

### Script Load Ordering
- Load UMD build via `<script src="https://cdnjs.cloudflare.com/ajax/libs/...">` — sets `window.Chart` global
- Follow with plain `<script>` (no `type="module"`)
- CDN scripts may not be loaded when the next `<script>` runs (especially during streaming)
- **Always use `onload="initChart()"` on the CDN script tag**
- Define your chart init in a named function
- Add `if (window.Chart) initChart();` as fallback at end of inline script
- This guarantees charts render regardless of load order

### Canvas and CSS Variables
- Canvas cannot resolve CSS variables. Use hardcoded hex or Chart.js defaults
- Multiple charts: use unique IDs (`myChart1`, `myChart2`). Each gets its own canvas+div pair

### Scale Padding
- For bubble and scatter charts: bubble radii extend past center points, so points near axis boundaries get clipped
- Pad the scale range — set `scales.y.min` and `scales.y.max` ~10% beyond data range
- Or use `layout: { padding: 20 }` as a blunt fallback

### X-Axis Labels
- Chart.js auto-skips x-axis labels when they'd overlap
- For ≤12 categories where all labels must be visible (waterfall, monthly), set `scales.x.ticks: { autoSkip: false, maxRotation: 45 }`

---

## Number Formatting

Negative values are `-$5M` not `$-5M` — sign before currency symbol.

Use a formatter:
```js
(v) => (v < 0 ? '-' : '') + '$' + Math.abs(v) + 'M'
```

---

## Legends

Always disable Chart.js default and build custom HTML:

```js
plugins: { legend: { display: false } }
```

```html
<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 8px; font-size: 12px; color: var(--color-text-secondary);">
  <span style="display: flex; align-items: center; gap: 4px;">
    <span style="width: 10px; height: 10px; border-radius: 2px; background: #3266ad;"></span>Chrome 65%
  </span>
  <span style="display: flex; align-items: center; gap: 4px;">
    <span style="width: 10px; height: 10px; border-radius: 2px; background: #73726c;"></span>Safari 18%
  </span>
</div>
```

Include the value/percentage in each label when the data is categorical (pie, donut, single-series bar). Position the legend above the chart (`margin-bottom`) or below (`margin-top`) — not inside the canvas.

---

## Dashboard Layout

Wrap summary numbers in metric cards above the chart:

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 1rem;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 1rem;">
    <div style="font-size: 13px; color: var(--color-text-secondary);">Revenue</div>
    <div style="font-size: 24px; font-weight: 500;">$2.4M</div>
  </div>
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 1rem;">
    <div style="font-size: 13px; color: var(--color-text-secondary);">Growth</div>
    <div style="font-size: 24px; font-weight: 500; color: var(--color-text-success);">+12%</div>
  </div>
</div>

<div style="position: relative; width: 100%; height: 300px;">
  <canvas id="revenueChart"></canvas>
</div>
```

Chart canvas flows below without a card wrapper. Use `sendPrompt()` for drill-down: `sendPrompt('Break down Q4 by region')`.

---

## ERD / Database Schemas (mermaid.js)

Use mermaid.js `erDiagram`, not Chart.js or SVG:

```html
<style>
#erd svg.erDiagram .row-rect-odd path,
#erd svg.erDiagram .row-rect-odd rect,
#erd svg.erDiagram .row-rect-even path,
#erd svg.erDiagram .row-rect-even rect { stroke: none !important; }
</style>
<div id="erd"></div>
<script type="module">
import mermaid from 'https://esm.sh/mermaid@11/dist/mermaid.esm.min.mjs';
const dark = matchMedia('(prefers-color-scheme: dark)').matches;
await document.fonts.ready;
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    darkMode: dark,
    fontSize: '13px',
    lineColor: dark ? '#9c9a92' : '#73726c',
    textColor: dark ? '#c2c0b6' : '#3d3d3a',
  },
});
const { svg } = await mermaid.render('erd-svg', `erDiagram
  USERS ||--o{ POSTS : writes
  POSTS ||--o{ COMMENTS : has`);
document.getElementById('erd').innerHTML = svg;
</script>
```
