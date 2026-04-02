# generative-ui

Design system and guidelines for Claude's built-in generative UI — the `show_widget` tool that renders interactive HTML/SVG widgets inline in claude.ai conversations.

## What it does

Provides the complete Anthropic "Imagine" design system so Claude produces high-quality widgets without needing to call `read_me` first. Covers:

- **Charts** — Chart.js line, bar, area charts with interactive controls
- **Diagrams** — SVG flowcharts, structural diagrams, illustrative diagrams
- **Dashboards** — metric cards, comparison grids, data displays
- **Interactive explainers** — sliders, toggles, live-updating calculations
- **Design tokens** — CSS variables, color palette (light/dark), typography, spacing

## Key design principles

- **Seamless** — widgets blend with the host UI
- **Flat** — no gradients, shadows, or decorative effects
- **Compact** — show the essential inline, explain in text
- **Dark mode mandatory** — all colors work in both light and dark mode via CSS variables

## Triggers

- "show me", "visualize", "draw", "chart", "dashboard"
- "diagram", "flowchart", "widget", "interactive", "mockup"
- "explain how X works" (with visual), "illustrate"
- Any request for visual/interactive output beyond plain text or markdown

## Platform

Works on **Claude.ai** (built-in `show_widget` tool).

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill generative-ui
```

See the [main README](../../README.md) for more installation options.

## Reference files

- `references/design_system.md` — Complete color palette, CSS variables, UI component patterns, metric cards, layout rules
- `references/svg_and_diagrams.md` — SVG viewBox setup, font calibration, pre-built classes, diagram patterns with examples
- `references/chart_js.md` — Chart.js configuration, script load ordering, canvas sizing, legend patterns, dashboard layout
