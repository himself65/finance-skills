# Writing SKILL.md and Reference Files

Detailed instructions for authoring each part of a skill. This is the reference companion to Steps 3-4 of the skill-creator workflow.

## Writing the Frontmatter

Write the YAML frontmatter first. See `references/frontmatter-guide.md` for the complete field reference.

```yaml
---
name: skill-name-here
description: >
  [Line 1: What it does — concrete, specific]
  [Line 2-5: Exhaustive trigger list — include BOTH expert terminology AND beginner phrasing]
  [Line 6+: Edge case triggers — "also when user does X", "even if they only say Y"]
---
```

**Description quality rules:**
- Minimum 5 distinct trigger phrases
- Include at least 2 "sideways entry points" (unexpected phrasings that should still trigger)
- Name specific tools, methods, or APIs the skill uses
- Include example ticker symbols or entities if domain-specific

## Writing Step 1: Detection Flow

Every skill that uses external tools MUST start with a detection flow — not just a single dep check, but a multi-dimensional probe that feeds a decision tree. See `references/dynamic-calling.md` for the complete pattern catalog.

### Template: Detection flow with decision tree

```markdown
## Step 1: Detection Flow

**Environment status:**
` ` `
!`(command -v tool_a && tool_a --version) 2>/dev/null || echo "TOOL_A_MISSING"`
` ` `

` ` `
!`(command -v tool_b && tool_b --version) 2>/dev/null || echo "TOOL_B_MISSING"`
` ` `

` ` `
!`echo $API_KEY | head -c 8 && echo "...KEY_SET" || echo "KEY_NOT_SET"`
` ` `

**Decision tree:**
1. If `tool_a` available and `KEY_SET` → **Method 1** (preferred, richest)
2. If `tool_a` available but `KEY_NOT_SET` → guide auth setup, then Method 1
3. If `tool_a` missing but `tool_b` available → **Method 2** (fallback)
4. If neither available → install `tool_a`, then Method 1
```

### Key rules for detection flows

- **Always use fallback sentinels:** `|| echo "SENTINEL"` — never let a check hang or error silently
- **Detect multiple dimensions:** tool existence + auth state + runtime environment
- **Produce a decision tree:** At least 2 distinct method paths, preferably 3+
- **Show partial keys:** `echo $KEY | head -c 8` lets users verify without exposing secrets
- **Treat runtimes as separate:** Terminal and execute_code are different — a shell install doesn't mean execute_code has the package
- **Keep checks fast:** Under 2 seconds — they run synchronously before the skill loads

For pure analysis skills (no external deps), use a "Gather Data" step that still detects data source availability (e.g., "if yfinance available, use it; otherwise accept manual input from user").

## Writing Core Steps (2 through N)

For each step:
1. **Clear heading**: `## Step N: [Verb] [Object]` (e.g., "Compute Correlations", "Identify Stage")
2. **Decision table** if the step involves routing or classification
3. **Pass/fail gate** if applicable ("If condition fails, stop here and tell the user")
4. **Reference pointer** for deep content: "Read `references/X.md` for details."
5. **Defaults table** for any parameters the user might omit

## Writing Parameter Defaults

Every skill MUST have explicit defaults for all parameters. Create a table:

```markdown
| Parameter | Default if not provided | Rationale |
|---|---|---|
| Lookback period | 1y | Balances recency and statistical significance |
| Ticker | SPY | Most liquid, universally recognized |
| Risk per trade | 1% | Standard conservative sizing |
```

## Writing the Final Step: Respond to the User

The last step MUST specify the exact output structure:

```markdown
## Step N: Respond to the User

Present results with these sections:

1. **[Section name]**: [What to include]
2. **[Section name]**: [What to include]
...

### Caveats to include
- [Required disclaimer]
- [Data limitations]
```

Number every output section. Include a verdict/grade system if the skill is evaluative.

---

## Writing Reference Files

### Naming Convention
- `lowercase-hyphenated.md` (never camelCase or underscores)
- Topic-focused: `quantization.md`, `position-sizing.md`
- One file per concept-cluster, not per section

### Reference File Structure

```markdown
# [Topic Title]

[1-3 sentence introduction]

## [First Major Section]

### [Subsection]

[Tables, code blocks, formulas]

## Edge Cases

- [Specific condition] -> [How to handle]
```

### Size Guidelines
- **Quick lookup** (API tables, checklists): 50-150 lines
- **Deep guide** (technique, methodology): 150-400 lines
- **Comprehensive catalog** (visual effects, all endpoints): 400-900 lines

### How SKILL.md Should Reference Them

Use table pointers in the relevant step, not scattered inline links:

```markdown
Read `references/position-sizing.md` for the full formula, examples, and pyramiding rules.
```

Or as a reference section at the end:

```markdown
## Reference Files

- `references/api.md` -- Complete API endpoint reference
- `references/troubleshooting.md` -- Common errors and solutions
```
