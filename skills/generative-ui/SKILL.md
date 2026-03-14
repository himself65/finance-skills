---
name: generative-ui
description: >
  Render interactive HTML/SVG widgets inline using Claude's generative UI system (show_widget tool).
  Use this skill whenever the user asks to visualize data, create an interactive chart, build a dashboard,
  render a diagram, draw a flowchart, show a mockup, create an interactive explainer, or produce any
  visual content beyond plain text or markdown. Triggers include: "show me", "visualize", "draw",
  "chart", "dashboard", "diagram", "flowchart", "widget", "interactive", "mockup", "illustrate",
  "explain how X works" (with visual), or any request for visual/interactive output. Also triggers
  when the user wants to display financial data visually, create comparison grids, or build tools
  with sliders, toggles, or live-updating displays.
---

# Generative UI Skill

Create rich visual content — SVG diagrams/illustrations and HTML interactive widgets — rendered inline via `visualize:show_widget`. The best output feels like a natural extension of the chat.

---

## Step 1: Call `visualize:read_me` First

Before your first `show_widget` call, invoke `visualize:read_me` with the relevant modules. Do NOT mention this call to the user — it is an internal setup step.

```json
{ "modules": ["chart", "interactive"] }
```

Available modules:

| Module | Use For |
|---|---|
| `diagram` | SVG flowcharts, structural diagrams, illustrative diagrams |
| `mockup` | UI mockups, forms, cards, dashboards |
| `interactive` | Interactive explainers with controls |
| `chart` | Charts and data analysis (includes Chart.js) |
| `art` | Illustration and generative art |

Pick the closest fit. The module includes all relevant design guidance.

---

## Step 2: Pick the Right Visual Type

Route on the **verb**, not the noun. Same subject, different visual depending on what was asked:

| User says | Type | Tool |
|---|---|---|
| "how does X work" | Illustrative diagram | `show_widget` (SVG) |
| "X architecture" | Structural diagram | `show_widget` (SVG) |
| "what are the steps" | Flowchart | `show_widget` (SVG) |
| "explain compound interest" | Interactive explainer | `show_widget` (HTML) |
| "compare these options" | Comparison grid | `show_widget` (HTML) |
| "show revenue chart" | Chart.js chart | `show_widget` (HTML) |
| "create a contact card" | Data record | `show_widget` (HTML) |
| "draw a sunset" | Art/illustration | `show_widget` (SVG) |

---

## Step 3: Build the Widget

### Structure (strict order)

```
<style>  →  HTML content  →  <script>
```

Output streams token-by-token. Styles must exist before the elements they target, and scripts must run after the DOM is ready.

### Philosophy

- **Seamless**: Users shouldn't notice where the host UI ends and your widget begins
- **Flat**: No gradients, mesh backgrounds, noise textures, or decorative effects. Clean flat surfaces
- **Compact**: Show the essential inline. Explain the rest in text
- **Text goes in your response, visuals go in the tool** — all explanatory text, descriptions, and summaries must be written as normal response text OUTSIDE the tool call. The tool output should contain ONLY the visual element

### Core Rules

- No `<!-- comments -->` or `/* comments */` (waste tokens, break streaming)
- No font-size below 11px
- No emoji — use CSS shapes or SVG paths
- No gradients, drop shadows, blur, glow, or neon effects
- No dark/colored backgrounds on outer containers (transparent only — host provides the bg)
- **Typography**: two weights only: 400 regular, 500 medium. Never use 600 or 700. Headings: h1=22px, h2=18px, h3=16px — all font-weight 500. Body text=16px, weight 400, line-height 1.7
- **Sentence case** always. Never Title Case, never ALL CAPS
- No mid-sentence bolding — entity names go in `code style` not **bold**
- No `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>` — just content fragments
- No `position: fixed` — use normal-flow layouts
- No tabs, carousels, or `display: none` sections during streaming
- No nested scrolling — auto-fit height
- Corners: `border-radius: var(--border-radius-lg)` for cards, `var(--border-radius-md)` for elements
- No rounded corners on single-sided borders (border-left, border-top)
- **Round every displayed number** — use `Math.round()`, `.toFixed(n)`, or `Intl.NumberFormat`

### CDN Allowlist (CSP-enforced)

External resources may ONLY load from:
- `cdnjs.cloudflare.com`
- `cdn.jsdelivr.net`
- `unpkg.com`
- `esm.sh`

All other origins are blocked — the request silently fails.

### CSS Variables

**Backgrounds**: `--color-background-primary` (white), `-secondary` (surfaces), `-tertiary` (page bg), `-info`, `-danger`, `-success`, `-warning`
**Text**: `--color-text-primary` (black), `-secondary` (muted), `-tertiary` (hints), `-info`, `-danger`, `-success`, `-warning`
**Borders**: `--color-border-tertiary` (0.15α, default), `-secondary` (0.3α, hover), `-primary` (0.4α), semantic `-info/-danger/-success/-warning`
**Typography**: `--font-sans`, `--font-serif`, `--font-mono`
**Layout**: `--border-radius-md` (8px), `--border-radius-lg` (12px), `--border-radius-xl` (16px)

All auto-adapt to light/dark mode.

**Dark mode is mandatory** — every color must work in both modes:
- In HTML: always use CSS variables for text. Never hardcode colors like `color: #333`
- In SVG: use pre-built color classes (`c-blue`, `c-teal`, etc.) — they handle light/dark automatically
- Mental test: if the background were near-black, would every text element still be readable?

### `sendPrompt(text)`

A global function that sends a message to chat as if the user typed it. Use it when the user's next step benefits from Claude thinking. Handle filtering, sorting, toggling, and calculations in JS instead.

---

## Step 4: Call `show_widget`

```json
{
  "i_have_seen_read_me": true,
  "title": "snake_case_widget_name",
  "widget_code": "<style>...</style>\n<div>...</div>\n<script>...</script>"
}
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `i_have_seen_read_me` | boolean | Yes | Must be `true` — confirms you called `read_me` first |
| `title` | string | Yes | Snake_case identifier for the widget (used as window title) |
| `widget_code` | string | Yes | HTML or SVG code. For SVG: raw `<svg>` element. For HTML: content fragment |
| `width` | number | No | Window width in pixels. Default: 800 |
| `height` | number | No | Window height in pixels. Default: 600 |

For SVG output: start `widget_code` with `<svg` — it will be auto-detected.

---

## Step 5: Chart.js Template

For charts, use `onload` callback pattern to handle script load ordering:

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 1rem;">
    <div style="font-size: 13px; color: var(--color-text-secondary);">Label</div>
    <div style="font-size: 24px; font-weight: 500;" id="stat1">—</div>
  </div>
</div>

<div style="position: relative; width: 100%; height: 300px; margin-top: 1rem;">
  <canvas id="myChart"></canvas>
</div>

<div style="display: flex; align-items: center; gap: 12px; margin-top: 1rem;">
  <label style="font-size: 14px; color: var(--color-text-secondary);">Parameter</label>
  <input type="range" min="0" max="100" value="50" id="param" step="1" style="flex: 1;" />
  <span style="font-size: 14px; font-weight: 500; min-width: 32px;" id="param-out">50</span>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js" onload="initChart()"></script>
<script>
function initChart() {
  const slider = document.getElementById('param');
  const out = document.getElementById('param-out');
  let chart = null;

  function update() {
    const val = parseFloat(slider.value);
    out.textContent = val;
    document.getElementById('stat1').textContent = val.toFixed(1);

    const labels = [], data = [];
    for (let x = 0; x <= 100; x++) {
      labels.push(x);
      data.push(x * val / 100);
    }

    if (chart) chart.destroy();
    chart = new Chart(document.getElementById('myChart'), {
      type: 'line',
      data: { labels, datasets: [{ data, borderColor: '#7F77DD', borderWidth: 2, pointRadius: 0, fill: false }] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } } }
      }
    });
  }

  slider.addEventListener('input', update);
  update();
}
if (window.Chart) initChart();
</script>
```

**Chart.js rules:**
- Canvas cannot resolve CSS variables — use hardcoded hex
- Set height ONLY on the wrapper div, never on canvas itself
- Always `responsive: true, maintainAspectRatio: false`
- Always disable default legend, build custom HTML legends
- Number formatting: `-$5M` not `$-5M` (negative sign before currency symbol)
- Use `onload="initChart()"` on CDN script tag + `if (window.Chart) initChart();` as fallback

---

## Step 6: SVG Diagram Template

For flowcharts and diagrams, use SVG with pre-built classes:

```svg
<svg width="100%" viewBox="0 0 680 H">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>

  <!-- Single-line node (44px tall) -->
  <g class="node c-blue" onclick="sendPrompt('Tell me more about this')">
    <rect x="250" y="40" width="180" height="44" rx="8" stroke-width="0.5"/>
    <text class="th" x="340" y="62" text-anchor="middle" dominant-baseline="central">Step one</text>
  </g>

  <!-- Connector arrow -->
  <line x1="340" y1="84" x2="340" y2="120" class="arr" marker-end="url(#arrow)"/>

  <!-- Two-line node (56px tall) -->
  <g class="node c-teal" onclick="sendPrompt('Explain this step')">
    <rect x="230" y="120" width="220" height="56" rx="8" stroke-width="0.5"/>
    <text class="th" x="340" y="140" text-anchor="middle" dominant-baseline="central">Step two</text>
    <text class="ts" x="340" y="158" text-anchor="middle" dominant-baseline="central">Processes the input</text>
  </g>
</svg>
```

**SVG rules:**
- ViewBox always 680px wide (`viewBox="0 0 680 H"`). Set H to fit content + 40px padding
- Safe area: x=40 to x=640, y=40 to y=(H-40)
- Pre-built classes: `t` (14px), `ts` (12px secondary), `th` (14px medium 500), `box`, `node`, `arr`, `c-{color}`
- Every `<text>` element must carry a class (`t`, `ts`, or `th`)
- Use `dominant-baseline="central"` for vertical text centering in boxes
- Connector paths need `fill="none"` (SVG defaults to `fill: black`)
- Stroke width: 0.5px for borders and edges
- Make all nodes clickable: `onclick="sendPrompt('...')"`

---

## Step 7: Interactive Explainer Template

For interactive explainers (sliders, live calculations, inline SVG):

```html
<div style="display: flex; align-items: center; gap: 12px; margin: 0 0 1.5rem;">
  <label style="font-size: 14px; color: var(--color-text-secondary);">Years</label>
  <input type="range" min="1" max="40" value="20" id="years" style="flex: 1;" />
  <span style="font-size: 14px; font-weight: 500; min-width: 24px;" id="years-out">20</span>
</div>

<div style="display: flex; align-items: baseline; gap: 8px; margin: 0 0 1.5rem;">
  <span style="font-size: 14px; color: var(--color-text-secondary);">$1,000 →</span>
  <span style="font-size: 24px; font-weight: 500;" id="result">$3,870</span>
</div>

<div style="margin: 2rem 0; position: relative; height: 240px;">
  <canvas id="chart"></canvas>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js" onload="initChart()"></script>
<script>
function initChart() {
  // slider logic, chart rendering, sendPrompt() for follow-ups
}
if (window.Chart) initChart();
</script>
```

Use `sendPrompt()` to let users ask follow-ups: `sendPrompt('What if I increase the rate to 10%?')`

---

## Step 8: Respond to the User

After rendering the widget, briefly explain:
1. What the widget shows
2. How to interact with it (which controls do what)
3. One key insight from the data

Keep it concise — the widget speaks for itself.

---

## Reference Files

- `references/design_system.md` — Complete color palette (9 ramps × 7 stops), CSS variables, UI component patterns, metric cards, layout rules
- `references/svg_and_diagrams.md` — SVG viewBox setup, font calibration, pre-built classes, flowchart/structural/illustrative diagram patterns with examples
- `references/chart_js.md` — Chart.js configuration, script load ordering, canvas sizing, legend patterns, dashboard layout

Read the relevant reference file when you need specific design tokens, SVG coordinate math, or Chart.js configuration details.
