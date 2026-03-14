# Generative UI Design System

Extracted from Claude's actual `visualize:read_me` guidelines (Imagine — Visual Creation Suite).

---

## Color Palette

9 color ramps, each with 7 stops from lightest to darkest. 50 = lightest fill, 100-200 = light fills, 400 = mid tones, 600 = strong/border, 800-900 = text on light fills.

| Class | Ramp | 50 | 100 | 200 | 400 | 600 | 800 | 900 |
|---|---|---|---|---|---|---|---|---|
| `c-purple` | Purple | #EEEDFE | #CECBF6 | #AFA9EC | #7F77DD | #534AB7 | #3C3489 | #26215C |
| `c-teal` | Teal | #E1F5EE | #9FE1CB | #5DCAA5 | #1D9E75 | #0F6E56 | #085041 | #04342C |
| `c-coral` | Coral | #FAECE7 | #F5C4B3 | #F0997B | #D85A30 | #993C1D | #712B13 | #4A1B0C |
| `c-pink` | Pink | #FBEAF0 | #F4C0D1 | #ED93B1 | #D4537E | #993556 | #72243E | #4B1528 |
| `c-gray` | Gray | #F1EFE8 | #D3D1C7 | #B4B2A9 | #888780 | #5F5E5A | #444441 | #2C2C2A |
| `c-blue` | Blue | #E6F1FB | #B5D4F4 | #85B7EB | #378ADD | #185FA5 | #0C447C | #042C53 |
| `c-green` | Green | #EAF3DE | #C0DD97 | #97C459 | #639922 | #3B6D11 | #27500A | #173404 |
| `c-amber` | Amber | #FAEEDA | #FAC775 | #EF9F27 | #BA7517 | #854F0B | #633806 | #412402 |
| `c-red` | Red | #FCEBEB | #F7C1C1 | #F09595 | #E24B4A | #A32D2D | #791F1F | #501313 |

### How to Assign Colors

Color encodes **meaning**, not sequence. Don't cycle through colors like a rainbow.

- Group nodes by **category** — all nodes of the same type share one color
- Use **gray for neutral/structural** nodes (start, end, generic steps)
- Use **2-3 colors per diagram**, not 6+. More = more visual noise
- **Prefer purple, teal, coral, pink** for general categories. Reserve blue, green, amber, red for semantic meaning (info, success, warning, error)

### Text on Colored Backgrounds

Always use the 800 or 900 stop from the same ramp as the fill. Never use black, gray, or `--color-text-primary` on colored fills.

When a box has both a title and a subtitle, use two different stops:
- **Light mode**: 50 fill + 600 stroke + 800 title / 600 subtitle
- **Dark mode**: 800 fill + 200 stroke + 100 title / 200 subtitle

Example: text on Blue 50 (#E6F1FB) must use Blue 800 (#0C447C) or 900 (#042C53), not black.

---

## CSS Variables

**Backgrounds**: `--color-background-primary` (white), `-secondary` (surfaces), `-tertiary` (page bg), `-info`, `-danger`, `-success`, `-warning`

**Text**: `--color-text-primary` (black), `-secondary` (muted), `-tertiary` (hints), `-info`, `-danger`, `-success`, `-warning`

**Borders**: `--color-border-tertiary` (0.15α, default), `-secondary` (0.3α, hover), `-primary` (0.4α), semantic `-info/-danger/-success/-warning`

**Typography**: `--font-sans`, `--font-serif`, `--font-mono`

**Layout**: `--border-radius-md` (8px), `--border-radius-lg` (12px — preferred for most components), `--border-radius-xl` (16px)

All auto-adapt to light/dark mode. For custom colors in HTML, use CSS variables. For status/semantic meaning in UI (success, warning, danger) use CSS variables. For categorical coloring in both diagrams and UI, use the color ramps.

---

## UI Component Patterns

### Aesthetic

Flat, clean, white surfaces. Minimal 0.5px borders. Generous whitespace. No gradients, no shadows (except functional focus rings). Everything should feel native to the host UI.

### Tokens

- Borders: always `0.5px solid var(--color-border-tertiary)` (or `-secondary` for emphasis)
- Corner radius: `var(--border-radius-md)` for most elements, `var(--border-radius-lg)` for cards
- Cards: white bg (`var(--color-background-primary)`), 0.5px border, radius-lg, padding 1rem 1.25rem
- Form elements (input, select, textarea, button, range slider) are pre-styled — write bare tags
- Buttons: transparent bg, 0.5px border-secondary, hover bg-secondary, active scale(0.98). If it triggers `sendPrompt`, append a ↗ arrow
- Spacing: use rem for vertical rhythm (1rem, 1.5rem, 2rem), px for component-internal gaps (8px, 12px, 16px)
- Box-shadows: none, except `box-shadow: 0 0 0 Npx` focus rings on inputs

### Metric Cards

For summary numbers (revenue, count, percentage):

```html
<div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 1rem;">
  <div style="font-size: 13px; color: var(--color-text-secondary);">Label</div>
  <div style="font-size: 24px; font-weight: 500;">$1,234</div>
</div>
```

Use in grids of 2-4 with `gap: 12px`. Distinct from raised cards (which have white bg + border).

### Layout Patterns

- **Editorial** (explanatory content): no card wrapper, prose flows naturally
- **Card** (bounded objects like a contact record, receipt): single raised card wraps the whole thing
- Don't put tables in widgets — output them as markdown in your response text

**Grid overflow**: `grid-template-columns: 1fr` has `min-width: auto` by default. Use `minmax(0, 1fr)` to clamp.

### Interactive Explainer

Sliders, buttons, live state displays, charts. Keep prose explanations in your response text. No card wrapper. Whitespace is the container.

```html
<div style="display: flex; align-items: center; gap: 12px; margin: 0 0 1.5rem;">
  <label style="font-size: 14px; color: var(--color-text-secondary);">Years</label>
  <input type="range" min="1" max="40" value="20" id="years" style="flex: 1;" />
  <span style="font-size: 14px; font-weight: 500; min-width: 24px;" id="years-out">20</span>
</div>
```

### Comparison Grid

Side-by-side card grid. Highlight differences with semantic colors. Use `repeat(auto-fit, minmax(160px, 1fr))` for responsive columns. When one option is recommended, accent its card with `border: 2px solid var(--color-border-info)` (the only exception to the 0.5px rule).

### Data Record

Wrap in a single raised card. Example:

```html
<div style="background: var(--color-background-primary); border-radius: var(--border-radius-lg); border: 0.5px solid var(--color-border-tertiary); padding: 1rem 1.25rem;">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
    <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--color-background-info); display: flex; align-items: center; justify-content: center; font-weight: 500; font-size: 14px; color: var(--color-text-info);">MR</div>
    <div>
      <p style="font-weight: 500; font-size: 15px; margin: 0;">Maya Rodriguez</p>
      <p style="font-size: 13px; color: var(--color-text-secondary); margin: 0;">VP of Engineering</p>
    </div>
  </div>
</div>
```

---

## Complexity Budget (Hard Limits)

- Box subtitles: ≤5 words
- Colors: ≤2 ramps per diagram
- Horizontal tier: ≤4 boxes at full width (~140px each). 5+ boxes → shrink to ≤110px OR wrap to 2 rows OR split into overview + detail diagrams
