# SVG Setup and Diagram Patterns

Extracted from Claude's actual `visualize:read_me` guidelines.

---

## SVG Setup

**ViewBox**: `<svg width="100%" viewBox="0 0 680 H">` — 680px wide, flexible height. Set H to fit content tightly (last element's bottom edge + 40px padding). Safe area: x=40 to x=640, y=40 to y=(H-40). Background transparent.

**The 680 in viewBox is load-bearing — do not change it.** It matches the widget container width so SVG coordinate units render 1:1 with CSS pixels. If your diagram content is naturally narrow, keep viewBox width at 680 and center the content — do not shrink the viewBox.

**Do not wrap the SVG in a container `<div>` with a background color** — the widget host provides the card container and background. Output the raw `<svg>` element directly.

### ViewBox Safety Checklist

Before finalizing any SVG, verify:
1. Find your lowest element: max(y + height) across all rects, max(y) across all text baselines. Set viewBox height = that value + 40px buffer
2. Find your rightmost element: max(x + width) across all rects. All content must stay within x=0 to x=680
3. For text with `text-anchor="end"`, the text extends LEFT from x. If x=118 and text is 200px wide, it starts at x=-82 — outside the viewBox
4. Never use negative x or y coordinates. The viewBox starts at 0,0
5. For every pair of boxes in the same row, check that left box's (x + width) < right box's x by at least 20px

### Font Size Calibration

| Text | Chars | Weight | Size | Rendered Width |
|---|---|---|---|---|
| Authentication Service | 22 | 500 | 14px | 167px |
| Background Job Processor | 24 | 500 | 14px | 201px |
| Detects and validates incoming tokens | 37 | 400 | 14px | 279px |
| forwards request to | 19 | 400 | 12px | 123px |

Before placing text in a box: does (text width + 2×padding) fit the container? Box width formula: `rect_width = max(title_chars × 8, subtitle_chars × 7) + 24`.

SVG `<text>` never auto-wraps. Every line break needs an explicit `<tspan x="..." dy="1.2em">`.

### Pre-built Classes

Already loaded in SVG widget context:

- `class="t"` = sans 14px primary text
- `class="ts"` = sans 12px secondary text
- `class="th"` = sans 14px medium (500) heading text
- `class="box"` = neutral rect (bg-secondary fill, border stroke)
- `class="node"` = clickable group with hover effect (cursor pointer, slight dim on hover)
- `class="arr"` = arrow line (1.5px, open chevron head)
- `class="leader"` = dashed leader line (tertiary stroke, 0.5px, dashed)
- `class="c-{ramp}"` = colored node. Apply to `<g>` or shape element (rect/circle/ellipse), NOT to paths. Sets fill+stroke on shapes, auto-adjusts child text classes, dark mode automatic
- Short aliases: `var(--p)`, `var(--s)`, `var(--t)`, `var(--bg2)`, `var(--b)`

**`c-{ramp}` nesting**: These classes use direct-child selectors. Nest a `<g>` inside a `<g class="c-blue">` and inner shapes become grandchildren — they lose the fill and render BLACK. Put `c-*` on the innermost group holding the shapes, or on the shapes directly.

### Arrow Marker (always include)

```svg
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

Use `marker-end="url(#arrow)"` on lines. The head uses `context-stroke` — inherits the color of whichever line it sits on.

### Style Rules

- Every `<text>` element must carry one of: `t`, `ts`, `th`
- Use only two font sizes: 14px (node labels) and 12px (subtitles, descriptions, arrow labels)
- No decorative step numbers or oversized headings
- No icons or illustrations inside boxes — text only
- Sentence case on all labels
- Stroke width: 0.5px for diagram borders and edges
- Connector paths need `fill="none"` (SVG defaults to `fill: black`)
- `rx="4"` for subtle corners, `rx="8"` max for emphasized rounding
- One SVG per tool call — never leave an abandoned or partial SVG

---

## Diagram Types

### Flowchart

For sequential processes, cause-and-effect, decision trees.

**Planning**: Size boxes to fit text generously. At 14px, each character is ~8px wide. A label like "Load Balancer" (13 chars) needs at least 140px wide rect.

**Spacing**: 60px minimum between boxes, 24px padding inside boxes, 12px between text and edges. Leave 10px gap between arrowheads and box edges. Two-line boxes need at least 56px height with 22px between lines.

**Vertical text placement**: Every `<text>` inside a box needs `dominant-baseline="central"`, with y set to the center of its slot. Formula: for text centered in a rect at (x, y, w, h), use `<text x={x+w/2} y={y+h/2} text-anchor="middle" dominant-baseline="central">`.

**Layout**: Prefer single-direction flows. Max 4-5 nodes per diagram. The widget is narrow (~680px).

**Single-line node** (44px tall):
```svg
<g class="node c-blue" onclick="sendPrompt('Tell me more about T-cells')">
  <rect x="100" y="20" width="180" height="44" rx="8" stroke-width="0.5"/>
  <text class="th" x="190" y="42" text-anchor="middle" dominant-baseline="central">T-cells</text>
</g>
```

**Two-line node** (56px tall):
```svg
<g class="node c-blue" onclick="sendPrompt('Tell me more about dendritic cells')">
  <rect x="100" y="20" width="200" height="56" rx="8" stroke-width="0.5"/>
  <text class="th" x="200" y="38" text-anchor="middle" dominant-baseline="central">Dendritic cells</text>
  <text class="ts" x="200" y="56" text-anchor="middle" dominant-baseline="central">Detect foreign antigens</text>
</g>
```

**Connector** (no label):
```svg
<line x1="200" y1="76" x2="200" y2="120" class="arr" marker-end="url(#arrow)"/>
```

**Arrows**: Must not cross any other box or label. If the direct path crosses something, route around with an L-bend: `<path d="M x1 y1 L x1 ymid L x2 ymid L x2 y2"/>`.

**Cycles**: Don't draw as rings. Build a stepper in HTML instead: one panel per stage, dots showing position (● ○ ○), Next wraps from last stage to first.

**Over budget prompts**: If user lists 6+ components, decompose into a stripped overview + one diagram per interesting sub-flow, each with 3-4 nodes.

### Structural Diagram

For concepts where physical or logical containment matters.

**Container rules**:
- Outermost: large rounded rect, rx=20-24, lightest fill (50 stop), 0.5px stroke (600 stop). Label at top-left, 14px bold
- Inner regions: medium rounded rects, rx=8-12, next shade fill (100-200 stop). Different color ramp if semantically different
- 20px minimum padding inside every container
- Max 2-3 nesting levels

**Example** (horizontal layout with two inner regions):
```svg
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
<g class="c-green">
  <rect x="120" y="30" width="560" height="260" rx="20" stroke-width="0.5"/>
  <text class="th" x="400" y="62" text-anchor="middle">Library branch</text>
  <text class="ts" x="400" y="80" text-anchor="middle">Main floor</text>
</g>
<g class="c-teal">
  <rect x="150" y="100" width="220" height="160" rx="12" stroke-width="0.5"/>
  <text class="th" x="260" y="130" text-anchor="middle">Circulation desk</text>
  <text class="ts" x="260" y="148" text-anchor="middle">Checkouts, returns</text>
</g>
<g class="c-amber">
  <rect x="450" y="100" width="210" height="160" rx="12" stroke-width="0.5"/>
  <text class="th" x="555" y="130" text-anchor="middle">Reading room</text>
  <text class="ts" x="555" y="148" text-anchor="middle">Seating, reference</text>
</g>
<text class="ts" x="410" y="175" text-anchor="middle">Books</text>
<line x1="370" y1="185" x2="448" y2="185" class="arr" marker-end="url(#arrow)"/>
```

**Color in structural diagrams**: Nested regions need distinct ramps. Same class on parent and child gives identical fills and flattens the hierarchy. Pick a related ramp for inner structures and a contrasting ramp for functionally different regions.

**Database schemas / ERDs**: Use mermaid.js, not SVG.

### Illustrative Diagram

For building *intuition*. Draw the mechanism, not a diagram *about* the mechanism.

**Two flavors**:
- **Physical subjects**: simplified cross-sections, cutaways, schematics (a water heater is a tank with a burner)
- **Abstract subjects**: spatial metaphors (a transformer is stacked slabs with attention threads, a hash function is a funnel scattering into buckets)

**What changes from flowchart rules**:
- Shapes are freeform: `<path>`, `<ellipse>`, `<circle>`, `<polygon>`, curved lines
- Layout follows the subject's geometry, not a grid
- Color encodes intensity, not category (warm = active/high-weight, cool = dormant)
- Layering and overlap are encouraged for shapes (but never let a stroke cross text)
- Small shape-based indicators are allowed (triangles for flames, circles for bubbles)
- One gradient per diagram is permitted — only for continuous physical properties
- CSS `@keyframes` animation permitted (only `transform` and `opacity`, wrap in `@media (prefers-reduced-motion: no-preference)`)

**Prefer interactive over static**: if the real-world system has a control, give the diagram that control. Use `show_widget` with inline SVG + HTML controls.

**Label placement**: Place labels outside the drawn object with thin leader lines (0.5px dashed). Reserve at least 140px of horizontal margin on the label side.

**Composition approach**:
1. Main object's silhouette — largest shape, centered
2. Internal structure: chambers, pipes, membranes
3. External connections: pipes, arrows, input/output labels
4. State indicators last: color fills, small animated elements
5. Leave generous whitespace around the object for labels

### Routing Decisions

| User says | Type | What to draw |
|---|---|---|
| "how do LLMs work" | Illustrative | Token row, stacked layers, attention threads |
| "transformer architecture" | Structural | Labelled boxes: embedding, attention, FFN |
| "how does attention work" | Illustrative | One query token, fan of lines to every key |
| "what are the training steps" | Flowchart | Forward → loss → backward → update |
| "explain the Krebs cycle" | HTML stepper | Click through stages. Never a ring |
| "draw the database schema" | mermaid.js | `erDiagram` syntax |

The illustrative route is the default for "how does X work" — don't default to a flowchart because it feels safer.

---

## Art and Illustration

For "draw me a sunset" / "create a geometric pattern":

- Fill the canvas — art should feel rich, not sparse
- Bold colors: mix `--color-text-*` categories for variety
- Art is the one place custom `<style>` color blocks are fine — freestyle colors
- Layer overlapping opaque shapes for depth
- Organic forms with `<path>` curves, `<ellipse>`, `<circle>`
- Texture via repetition (parallel lines, dots, hatching) not raster effects
- Geometric patterns with `<g transform="rotate()">` for radial symmetry
