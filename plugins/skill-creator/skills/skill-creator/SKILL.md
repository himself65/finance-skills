---
name: skill-creator
description: >
  Create, improve, and evaluate agent skills (SKILL.md plus reference files). Use this
  skill whenever the user wants to build, scaffold, or design a new skill, improve or
  fix an existing skill that isn't working well, score or benchmark a skill's quality
  or run evals on it, or turn a repeated manual workflow into a skill ("I keep doing
  X manually", "can you remember how to do X", "turn this into a skill").
---

# Skill Creator

Create, evaluate, and iterate on high-quality agent skills. This skill covers the whole lifecycle: planning what the skill should do, writing SKILL.md and reference files, scoring quality against a rubric, and iterating until the skill meets production standards.

**Philosophy:** A great skill is precise, not long. Its description routes the right requests to it. Its body gives the model the context it can't get anywhere else — the environment, tool contracts, defaults, domain judgment, and the reasons behind each constraint — and leaves out what a capable model already does on its own. Current Claude models follow instructions closely and literally, so every line gets acted on: an over-scripted or shouting skill produces rigid, over-cautious output, while a clear goal and quality bar let the model plan the work itself. `references/writing-guide.md` covers this in detail.

**Runtime adaptation:** Skills that touch external tools should detect what is installed, authenticated, and reachable at runtime and adapt, rather than assuming a single method. Offer fallback paths where real alternatives exist. See `references/dynamic-calling.md` for the pattern catalog.

---

## Step 1: Understand What the User Wants

Classify the request into one of these modes:

| User Intent | Mode | Jump To |
|---|---|---|
| Create a brand-new skill | **Create** | Step 2 |
| Improve / fix an existing skill | **Improve** | Step 6 |
| Evaluate / score a skill's quality | **Evaluate** | Step 7 |

If ambiguous, ask: "Do you want to create a new skill, improve an existing one, or evaluate one?"

### Gather Requirements (for Create mode)

Before writing anything, answer these questions (ask the user if unclear):

| Question | Why it matters |
|---|---|
| What task does the skill automate? | Defines the core workflow |
| Who is the target user? | Determines complexity and terminology level |
| What tools/APIs/CLIs does it use? | Determines dependencies and platform restrictions |
| What does the user provide as input? | Defines parameters and defaults |
| What should the output look like? | Defines the output contract |
| Does it need API keys or credentials? | Determines `required_environment_variables` |
| Should it work on Claude.ai or only CLI? | Determines platform field and dynamic commands |

---

## Step 2: Plan the Skill Architecture

Before writing SKILL.md, plan the structure. Read `references/architecture-patterns.md` for detailed guidance on each pattern.

### Choose a Structural Pattern

| Pattern | When to use | Shape | Example |
|---|---|---|---|
| **Linear** | Single workflow, no branching | Setup → fetch → analyze → respond | earnings-preview |
| **Router** | Multiple sub-tasks under one umbrella | Setup + routing table + sub-skills | stock-correlation (4 sub-skills), etf-premium |
| **Methodology** | Formal domain framework with real gates | Ordered checks, each able to stop the analysis | sepa-strategy |
| **Widget** | Generates interactive UI output | Extract → compute → render → explain | options-payoff |
| **API Wrapper** | Wraps an external API with many endpoints | Auth + endpoint map + heavy references | fintel-data |

### Plan the Outline

Every skill has three parts:

1. **Setup / detection** — detect available tools, auth state, and runtime environment, and decide which method to use. Skills with no external dependencies can skip this.
2. **The work** — numbered steps where the order genuinely matters (fetch before compute, a gate that can end the analysis), plus the judgment the model has to exercise, stated as goals, criteria, and domain heuristics rather than a script.
3. **Respond to the user** — the output contract: what the answer leads with, what it must contain, which caveats apply, and any verdict scale.

If a skill needs more than about nine steps, split it or use the Router pattern.

### Plan the Detection Flow

Skills that touch external tools should start with a runtime detection flow. Read `references/dynamic-calling.md` for all patterns. The detection flow answers:

| Question | How to detect | Decision |
|---|---|---|
| Is the CLI tool installed? | `command -v tool` | CLI path vs Python fallback |
| Is the user authenticated? | `tool auth status` / `echo $API_KEY` | Skip auth setup vs guide through it |
| Which runtime has the library? | `import lib` in terminal vs execute_code | Route to correct runtime |
| Is a richer tool available? | `gh --version` vs `git --version` | Rich path vs minimal path |
| Is live data reachable? | `curl -s endpoint` | Live data vs cached/default |

The detection output feeds a **decision tree** that the rest of the skill follows — check rather than assume.

### Plan Reference Files

Decide what goes in SKILL.md vs references/:

| In SKILL.md (under ~250 lines) | In references/ |
|---|---|
| Workflow and decision points | Detailed API documentation |
| Routing/decision tables | Code templates (>20 lines) |
| Parameter defaults table | Formulas and edge cases |
| Output contract | Troubleshooting database |
| Quick examples (1-3) | Comprehensive examples (4+) and dated datasets |

---

## Step 3: Write the SKILL.md

Read `references/writing-guide.md` for detailed instructions on writing each section. Read `references/frontmatter-guide.md` for the complete YAML field reference.

### Key Rules

1. **Frontmatter first**: `name` (lowercase-hyphenated, max 64 chars) and `description` (max 1024 chars, no angle brackets) are required. The description is routing text that rides along in every request: say what the skill does, name the categories of requests it serves and the distinctive vocabulary users will use (methods, tools, data types, entities), and point to sibling skills for neighboring requests. Name intent categories instead of listing near-synonymous phrasings.

2. **Detection flow for external dependencies**: use `!`command`` probes with fallback sentinels to detect tools, auth state, and runtime, then route to a method. For Codex and other hosts without command preprocessing, explicitly instruct the agent to run the enclosed commands with its shell tool and use the real output. Offer a second path where a real alternative exists (CLI vs Python library vs built-in tool). See `references/dynamic-calling.md`.

3. **Match specificity to fragility**: give exact commands, flags, and code for fragile operations — installs, auth, CLI syntax, API contracts, calculations that must be right. For judgment work — analysis, interpretation, writing — state the goal, the criteria, and the domain heuristics, and let the model plan. Put a pass/fail gate wherever a failed check really ends the analysis.

4. **Defaults table**: give every parameter the user might omit an explicit default, so the skill never stalls waiting for input.

5. **Output contract in the final step**: what to lead with, what the answer must contain, which caveats apply, and any verdict or grade scale. Pin a section-by-section template only where the format itself matters (scorecards, widgets, checklists). Describe length qualitatively rather than with word or sentence counts, and label examples as illustrative rather than filling them with made-up figures for real companies.

6. **Plain register**: state each constraint once, with its reason. Leave out capitalized MUST/NEVER/CRITICAL, repeated warnings, and instructions current models follow by default ("be thorough", "think step by step", "double-check your answer") — they cause over-triggering and over-checking rather than better work. Keep real policy constraints (read-only, no trade execution, privacy) in plain words.

7. **Keep volatile facts honest**: fetch live data where you can, date-stamp anything that will go stale, and keep dated datasets in `references/`. Verify API names and response shapes against the current library before shipping.

See `references/skill-examples.md` for annotated examples of each pattern.

---

## Step 4: Write Reference Files

Read `references/writing-guide.md` for the full reference file authoring guide.

### Key Rules

1. **Naming**: `lowercase-hyphenated.md`, one file per concept-cluster
2. **Size**: Quick lookup 50-150 lines, deep guide 150-400 lines, catalog 400-900 lines
3. **Structure**: H1 title, H2 sections, code blocks, tables, edge cases section at end
4. **Linking**: Use backtick paths in SKILL.md steps and a `## Reference Files` section at the end

---

## Step 5: Quality Check Before Delivery

Run the skill through the quality rubric in `references/quality-rubric.md`. Score each dimension.

### Quick Checklist

- [ ] Frontmatter has `name` and `description`; the description is under 1024 characters with no angle brackets
- [ ] Description names what the skill does, the categories of intent it serves, and its distinctive vocabulary — not a list of near-synonymous phrasings
- [ ] Description points to sibling skills for neighboring requests, where they exist
- [ ] SKILL.md is under 300 lines (ideally under 250)
- [ ] Every parameter has an explicit default
- [ ] Numbered steps where order matters; judgment work is stated as goals, criteria, and heuristics
- [ ] Gates stop the analysis only where a failed check really ends it
- [ ] Final step states an output contract: what to lead with, required content, caveats, verdict scale
- [ ] No numeric length caps; examples are labeled illustrative
- [ ] Constraints are stated once, in plain words, with their reasons — no capitalized MUST/NEVER, no "think step by step" or "double-check" boilerplate
- [ ] Complex content is in reference files, not inline
- [ ] Reference file pointers use backtick paths
- [ ] External dependencies are detected at runtime with `!`command`` checks and fallbacks (`|| echo "..."`)
- [ ] Separate runtimes treated as separate environments (terminal vs execute_code)
- [ ] Legal/ethical disclaimers included where appropriate
- [ ] No hardcoded ticker lists, tool paths, or undated static data that will go stale
- [ ] API names, fields, and code in the skill were checked against the current library

If any item fails, fix it before delivering to the user.

---

## Step 6: Improve an Existing Skill

When the user asks to improve a skill:

### 6a: Read the Current Skill

Read the SKILL.md and all reference files (on Hermes, `skill_view(name)` loads them).

### 6b: Score It Against the Rubric

Use the quality rubric from `references/quality-rubric.md`. Present the score breakdown to the user (illustrative):

| Dimension | Score | Issue |
|---|---|---|
| Trigger quality | 6/10 | Twenty near-synonym phrasings; misses the ETF use case |
| Defaults coverage | 3/10 | No defaults table |
| Instruction design | 5/10 | Scripted steps for judgment work; capitalized warnings |
| Output contract | 4/10 | Rigid 9-section template with made-up example figures |
| Reference usage | 7/10 | Good split, but missing troubleshooting |

### 6c: Propose Specific Improvements

List concrete changes ranked by impact:

1. [Highest impact] Add a defaults table covering every parameter
2. [High impact] Rewrite the description around intent categories and distinctive vocabulary
3. [Medium impact] Replace the fixed report template with an output contract
4. ...

### 6d: Apply Changes

After user approval, edit the skill files (on Hermes, use `skill_manage(action='patch', ...)` for targeted changes or `skill_manage(action='edit', ...)` for full rewrites).

---

## Step 7: Evaluate a Skill

When the user asks to evaluate or score a skill:

### 7a: Load and Analyze

Read the full SKILL.md and all reference files. Count lines, steps, defaults, and reference files, and note the description's length and the intent categories it covers.

### 7b: Score Against Rubric

Use the comprehensive rubric from `references/quality-rubric.md`. Score each of the 10 dimensions on a 1-10 scale.

### 7c: Present the Scorecard

```
## Skill Quality Scorecard: [skill-name]

| # | Dimension | Score | Notes |
|---|---|---|---|
| 1 | Trigger quality | 8/10 | Covers all four intent categories; one sibling boundary missing |
| 2 | Defaults coverage | 9/10 | All 11 parameters have defaults |
| 3 | Instruction design | 8/10 | Ordered setup and compute; analysis stated as criteria |
| 4 | Reference file strategy | 7/10 | 2 files, could use troubleshooting |
| 5 | Dynamic content | 10/10 | Dep check + live data injection |
| 6 | Output contract | 9/10 | Leads with verdict; required caveats; scale defined |
| 7 | Error handling | 6/10 | Missing data handling unclear |
| 8 | Code/formula quality | 8/10 | Working JS, copy-paste ready |
| 9 | Conciseness & register | 7/10 | 196 lines; two capitalized warnings to restate |
| 10 | Domain accuracy | 9/10 | BS formulas correct, edge cases covered |

**Overall: 81/100** -- Production quality

### Top 3 Improvements
1. ...
2. ...
3. ...
```

### Reference Skills

Skills in this repo that show each pattern well:

| Skill | What it demonstrates |
|---|---|
| sepa-strategy | Methodology pattern: real gates, domain criteria in references, a verdict scale |
| options-payoff | Widget pattern: a default for every field, live data injection, a precise render spec |
| stock-correlation | Router pattern: intent routing table, self-contained sub-skills, metrics computed in code |
| earnings-preview | Output contract: a content checklist with one judgment section, lead-with-the-headline guidance |
| fintel-data | API wrapper: key resolution flow, endpoint map, error semantics |

---

## Step 8: Respond to the User

### For Create mode

Deliver:
1. The complete SKILL.md content
2. All reference files
3. A README.md for the skill directory
4. The quality scorecard (from Step 5)
5. Suggested next steps (test it, iterate, publish)

### For Improve mode

Deliver:
1. Before/after quality scores
2. Summary of changes made
3. Remaining improvement opportunities

### For Evaluate mode

Deliver:
1. The full quality scorecard
2. Comparison to the reference skills
3. Prioritized improvement list

---

## Reference Files

- `references/dynamic-calling.md` -- **Core reference**: Detection flows, decision trees, method fallbacks, runtime awareness, and multi-tool adaptation patterns with annotated examples from production skills
- `references/writing-guide.md` -- How to write each SKILL.md section for current Claude models: descriptions, detection flows, instructions matched to fragility, defaults, output contracts, and reference files
- `references/architecture-patterns.md` -- Linear, Router, Methodology, Widget, and API Wrapper patterns with examples and anti-patterns
- `references/frontmatter-guide.md` -- Complete YAML frontmatter field reference (name, description, platform, env vars, config, credentials)
- `references/quality-rubric.md` -- 10-dimension scoring rubric with 1-10 scales, examples, and score interpretation
- `references/skill-examples.md` -- Annotated excerpts from top skills showing why specific patterns work
