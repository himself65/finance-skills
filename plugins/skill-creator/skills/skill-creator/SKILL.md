---
name: skill-creator
description: >
  Create new skills, modify and improve existing skills, and measure skill performance.
  Use when users want to create a skill from scratch, update or optimize an existing skill,
  run evals to test a skill, benchmark skill performance with variance analysis, or iterate
  on skill quality. Triggers: "create a skill", "make a new skill", "build a skill for",
  "write a skill that", "skill for doing X", "I want a skill to", "new skill", "design a skill",
  "scaffold a skill", "improve this skill", "optimize this skill", "this skill isn't working well",
  "evaluate this skill", "score this skill", "how good is this skill", "run evals on",
  "benchmark this skill", "test this skill's quality", "skill quality", "skill performance".
  Also triggers when a user describes a repeatable workflow they want to automate, says
  "I keep doing X manually", "can you remember how to do X", or "turn this into a skill".
---

# Skill Creator

Create, evaluate, and iterate on high-quality agent skills. This skill guides the entire lifecycle: planning what the skill should do, writing SKILL.md and reference files, scoring quality against a rubric, and iterating until the skill meets production standards.

**Philosophy:** A great skill is not a long skill. It is a *precise* skill: exhaustive triggers, explicit defaults, clear steps with exit gates, deferred complexity via reference files, and a structured output template.

**Core rule — always dynamic, never static:** Skills MUST detect what tools, libraries, and auth are available at runtime and adapt their behavior accordingly. Never hardcode a single method. Always provide a detection flow with a decision tree and fallback paths. See `references/dynamic-calling.md` for the complete pattern catalog.

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
| What should the output look like? | Defines the response template |
| Does it need API keys or credentials? | Determines `required_environment_variables` |
| Should it work on Claude.ai or only CLI? | Determines platform field and dynamic commands |

---

## Step 2: Plan the Skill Architecture

Before writing SKILL.md, plan the structure. Read `references/architecture-patterns.md` for detailed guidance on each pattern.

### Choose a Structural Pattern

| Pattern | When to use | Steps | Example |
|---|---|---|---|
| **Linear** | Single workflow, no branching | 5-7 | earnings-preview, etf-premium |
| **Router** | Multiple sub-tasks under one umbrella | 3 + sub-skills | stock-correlation (4 sub-skills) |
| **Methodology** | Complex domain framework with sequential gates | 7-9 | sepa-strategy (9-step trading methodology) |
| **Widget** | Generates interactive UI output | 4-5 | options-payoff (extract + compute + render) |
| **API Wrapper** | Wraps an external API with many endpoints | 3-5 + heavy references | funda-data (5 steps, 8 reference files) |

### Plan the Step Outline

Write out the step names before writing content. Every skill should have:

1. **Detection flow** (Step 1) -- dynamically detect available tools, auth state, and runtime environment; build a decision tree for which method to use
2. **Core methodology** (Steps 2-N) -- the actual work, with pass/fail gates; each step that calls an external tool should have method alternatives based on what Step 1 detected
3. **Respond to user** (Final step) -- structured output template

Target **5-9 steps** total. More than 9 means the skill should be split or use a router pattern.

### Plan the Detection Flow

Every skill that touches external tools MUST start with a runtime detection flow. Read `references/dynamic-calling.md` for all patterns. The detection flow answers:

| Question | How to detect | Decision |
|---|---|---|
| Is the CLI tool installed? | `command -v tool` | CLI path vs Python fallback |
| Is the user authenticated? | `tool auth status` / `echo $API_KEY` | Skip auth setup vs guide through it |
| Which runtime has the library? | `import lib` in terminal vs execute_code | Route to correct runtime |
| Is a richer tool available? | `gh --version` vs `git --version` | Rich path vs minimal path |
| Is live data reachable? | `curl -s endpoint` | Live data vs cached/default |

The detection output feeds into a **decision tree** that the rest of the skill follows. Never assume — always check.

### Plan Reference Files

Decide what goes in SKILL.md vs references/:

| In SKILL.md (under ~250 lines) | In references/ |
|---|---|
| Step-by-step workflow | Detailed API documentation |
| Routing/decision tables | Code templates (>20 lines) |
| Parameter defaults table | Formulas and edge cases |
| Output format template | Troubleshooting database |
| Quick examples (1-3) | Comprehensive examples (4+) |

---

## Step 3: Write the SKILL.md

Read `references/writing-guide.md` for detailed instructions on writing each section. Read `references/frontmatter-guide.md` for the complete YAML field reference.

### Key Rules

1. **Frontmatter first**: `name` (lowercase-hyphenated, max 64 chars) and `description` (exhaustive trigger list, max 1024 chars) are required. Description needs 5+ triggers including sideways entry points.

2. **Step 1 = detection flow**: Use `!`command`` with fallbacks to detect available tools, auth state, and runtime. Build a decision tree with multiple method paths (e.g., CLI preferred, Python fallback, built-in tools last resort). Never hardcode a single tool — always detect and adapt. See `references/dynamic-calling.md`.

3. **Core steps with method alternatives**: Each step that calls an external tool should offer at least 2 paths based on what Step 1 detected. Use pattern: "If `TOOL_A` detected → Method 1, otherwise → Method 2." Each step gets `## Step N: [Verb] [Object]`, a decision table if routing, a pass/fail gate if evaluative, and a reference pointer for deep content.

4. **Defaults table**: Every parameter MUST have an explicit default. No skill should ever stall waiting for input.

5. **Final step = output template**: Number every output section. Specify exactly what data goes in each. Include a verdict/grade system if evaluative.

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

- [ ] Frontmatter has `name` and `description` (both required)
- [ ] Description has 5+ distinct trigger phrases
- [ ] Description includes sideways entry points
- [ ] SKILL.md is under 300 lines (ideally under 250)
- [ ] Every parameter has an explicit default
- [ ] Steps are numbered (## Step N: ...)
- [ ] Each step has a clear exit condition or deliverable
- [ ] Final step specifies exact output structure with numbered sections
- [ ] Complex content is in reference files, not inline
- [ ] Reference file pointers use backtick paths
- [ ] Step 1 has a detection flow with `!`command`` checks and fallbacks (`|| echo "..."`)
- [ ] Detection flow produces a decision tree with 2+ method paths
- [ ] Core steps adapt behavior based on detection results (not hardcoded to one tool)
- [ ] Separate runtimes treated as separate environments (terminal vs execute_code)
- [ ] Legal/ethical disclaimers included where appropriate
- [ ] No hardcoded ticker lists, tool paths, or static data that will go stale

If any item fails, fix it before delivering to the user.

---

## Step 6: Improve an Existing Skill

When the user asks to improve a skill:

### 6a: Read the Current Skill

Load the skill with `skill_view(name)` or read the SKILL.md directly. Also read all reference files.

### 6b: Score It Against the Rubric

Use the quality rubric from `references/quality-rubric.md`. Present the score breakdown to the user:

| Dimension | Score | Issue |
|---|---|---|
| Trigger quality | 6/10 | Missing beginner phrasing |
| Defaults coverage | 3/10 | No defaults table |
| Step structure | 8/10 | Good, but Step 3 lacks exit gate |
| Output template | 4/10 | Vague "summarize results" |
| Reference usage | 7/10 | Good split, but missing troubleshooting |

### 6c: Propose Specific Improvements

List concrete changes ranked by impact:

1. [Highest impact] Add defaults table with 8+ parameters
2. [High impact] Rewrite description with 10+ trigger phrases
3. [Medium impact] Add structured output template to final step
4. ...

### 6d: Apply Changes

After user approval, edit the skill. Use `skill_manage(action='patch', ...)` for targeted changes or `skill_manage(action='edit', ...)` for full rewrites.

---

## Step 7: Evaluate a Skill

When the user asks to evaluate or score a skill:

### 7a: Load and Analyze

Read the full SKILL.md and all reference files. Count lines, steps, triggers, defaults, reference files.

### 7b: Score Against Rubric

Use the comprehensive rubric from `references/quality-rubric.md`. Score each of the 10 dimensions on a 1-10 scale.

### 7c: Present the Scorecard

```
## Skill Quality Scorecard: [skill-name]

| # | Dimension | Score | Notes |
|---|---|---|---|
| 1 | Trigger quality | 8/10 | 12 triggers, includes sideways entries |
| 2 | Defaults coverage | 9/10 | All 11 parameters have defaults |
| 3 | Step architecture | 8/10 | 5 clear steps with gates |
| 4 | Reference file strategy | 7/10 | 2 files, could use troubleshooting |
| 5 | Dynamic content | 10/10 | Dep check + live data injection |
| 6 | Output template | 9/10 | 5 numbered sections + verdict |
| 7 | Error handling | 6/10 | Missing data handling unclear |
| 8 | Code/formula quality | 8/10 | Working JS, copy-paste ready |
| 9 | SKILL.md conciseness | 7/10 | 196 lines, well within target |
| 10 | Domain accuracy | 9/10 | BS formulas correct, edge cases covered |

**Overall: 81/100** -- Production quality

### Top 3 Improvements
1. ...
2. ...
3. ...
```

### Benchmark Reference

For context, here are scores for known high-quality skills in this repo:

| Skill | Score | Why |
|---|---|---|
| sepa-strategy | ~90/100 | 9 steps, 7 refs, exhaustive triggers, structured verdict |
| options-payoff | ~85/100 | Strong defaults, working code, live data, clean output |
| stock-correlation | ~80/100 | Router pattern, 4 sub-skills, good defaults |

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
2. Comparison to benchmark skills
3. Prioritized improvement list

---

## Reference Files

- `references/dynamic-calling.md` -- **Core reference**: Detection flows, decision trees, method fallbacks, runtime awareness, and multi-tool adaptation patterns with annotated examples from production skills
- `references/writing-guide.md` -- Detailed instructions for writing SKILL.md sections, environment checks, defaults tables, output templates, and reference files
- `references/architecture-patterns.md` -- Linear, Router, Methodology, Widget, and API Wrapper patterns with examples and anti-patterns
- `references/frontmatter-guide.md` -- Complete YAML frontmatter field reference (name, description, platform, env vars, config, credentials)
- `references/quality-rubric.md` -- 10-dimension scoring rubric with 1-10 scales, benchmark scores, and score interpretation
- `references/skill-examples.md` -- Annotated excerpts from top skills showing why specific patterns work
