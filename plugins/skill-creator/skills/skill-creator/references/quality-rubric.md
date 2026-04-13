# Skill Quality Rubric

Score each dimension on a 1-10 scale. A production-quality skill should score 70+ overall. The best skills in this repo score 80-90.

## Dimension 1: Trigger Quality (Description Field)

How well does the description field capture the full range of user requests that should activate this skill?

| Score | Criteria |
|---|---|
| 1-3 | Generic description ("analyze stocks"), few trigger phrases, no sideways entries |
| 4-5 | Decent coverage of main use case, 3-5 trigger phrases, expert-only terminology |
| 6-7 | Good coverage, 6-10 trigger phrases, mix of expert and beginner phrasing |
| 8-9 | Excellent, 10+ triggers, sideways entries, example entities, covers edge cases |
| 10 | Exhaustive — hard to imagine a valid request that wouldn't trigger this skill |

**Benchmark:** sepa-strategy scores 9/10 (15+ triggers including "should I buy this stock")

## Dimension 2: Defaults Coverage

Does every parameter have an explicit default so the skill never stalls waiting for input?

| Score | Criteria |
|---|---|
| 1-3 | No defaults table, skill frequently asks user for missing info |
| 4-5 | Some defaults mentioned in prose, incomplete coverage |
| 6-7 | Defaults table exists, covers main parameters, missing a few edge cases |
| 8-9 | Comprehensive defaults table with rationale column, covers all parameters |
| 10 | Every conceivable parameter has a default, skill always produces output |

**Benchmark:** options-payoff scores 9/10 (11 parameters with defaults, rationale for each)

## Dimension 3: Step Architecture

Are steps numbered, well-bounded, and sequenced logically with clear exit gates?

| Score | Criteria |
|---|---|
| 1-3 | No numbered steps, wall-of-text instructions, no exit gates |
| 4-5 | Some structure but inconsistent, steps blend together, missing gates |
| 6-7 | Numbered steps (## Step N), each has a clear purpose, some exit gates |
| 8-9 | 5-9 well-defined steps, each with pass/fail criteria, clear exit gates |
| 10 | Perfect step architecture — every step has a deliverable, gate, and transition |

**Benchmark:** sepa-strategy scores 9/10 (9 steps, each with explicit pass/fail, "stop here" gates)

## Dimension 4: Reference File Strategy

Is complexity properly deferred to reference files? Is SKILL.md lean?

| Score | Criteria |
|---|---|
| 1-3 | Everything inline, SKILL.md is 500+ lines, no reference files |
| 4-5 | Some references exist but SKILL.md still bloated, or references are trivial |
| 6-7 | Good split — SKILL.md under 300 lines, 1-3 reference files for deep content |
| 8-9 | Clean architecture — SKILL.md under 250 lines, 3-7 reference files covering all depth |
| 10 | Perfect split — SKILL.md is pure workflow, all detail in well-organized references |

**Benchmark:** sepa-strategy scores 9/10 (250 lines, 7 reference files totaling ~29KB)

## Dimension 5: Dynamic Calling & Runtime Adaptation

Does the skill detect available tools at runtime and adapt its behavior with multiple method paths?

| Score | Criteria |
|---|---|
| 1-3 | No detection, hardcodes a single tool/library, fails if not installed |
| 4-5 | Has a dependency check but no decision tree or fallback path |
| 6-7 | Detection flow with fallback messages; single method path after detection |
| 8-9 | Full detection flow → decision tree → 2+ method paths; auth detection; graceful fallbacks |
| 10 | Multi-dimensional detection (tools + auth + runtime + live data), decision tree with 3+ paths, inline fallbacks at every usage point, frontmatter conditional activation |

**Benchmark:** github-auth scores 10/10 (detects gh vs git, auth state, credential helper; 3 distinct method paths). options-payoff scores 8/10 (dep check + live SPX price injection with fallback). duckduckgo-search scores 9/10 (CLI vs Python vs built-in, runtime awareness, `fallback_for_toolsets`).

**Note:** Skills that are pure analysis (no external deps) can score 7+ by having a well-structured "Gather Data" step with data source alternatives (e.g., yfinance vs manual input).

## Dimension 6: Output Template

Does the final step specify the exact output structure?

| Score | Criteria |
|---|---|
| 1-3 | "Summarize the results" — no structure specified |
| 4-5 | Lists what to include but no numbering or format |
| 6-7 | Numbered output sections, some format guidance |
| 8-9 | Fully specified template: numbered sections, what data in each, verdict system |
| 10 | Template so precise that two runs of the skill produce identically structured output |

**Benchmark:** sepa-strategy scores 9/10 (8 numbered sections + verdict + disclaimer)

## Dimension 7: Error Handling & Missing Data

How does the skill handle missing data, failed API calls, or partial input?

| Score | Criteria |
|---|---|
| 1-3 | No mention of error cases, skill will break on missing data |
| 4-5 | Some error handling but gaps — certain failures cause silent wrong results |
| 6-7 | Handles main error cases, has "if unavailable" notes |
| 8-9 | Comprehensive: missing data noted and flagged, fallback approaches, user prompts |
| 10 | Graceful degradation at every step — always produces useful output even with partial data |

**Benchmark:** sepa-strategy scores 8/10 ("proceed with what you have, flag RS as significant gap")

## Dimension 8: Code / Formula Quality

Are code templates and formulas correct, complete, and copy-paste ready?

| Score | Criteria |
|---|---|
| 1-3 | No code provided, or pseudocode that won't run |
| 4-5 | Code snippets exist but incomplete — missing imports, variable names differ |
| 6-7 | Working code that needs minor adaptation |
| 8-9 | Copy-paste ready code with proper imports, error handling, and comments |
| 10 | Production-quality code templates in reference files + skeleton in SKILL.md |

**Benchmark:** stock-correlation scores 8/10 (full Python functions with imports, dropna, edge cases)

**Note:** Not all skills need code. For pure analysis skills, score based on formula clarity and table quality.

## Dimension 9: SKILL.md Conciseness

Is the main SKILL.md file appropriately sized?

| Score | Criteria |
|---|---|
| 1-3 | Over 500 lines — too much inline, needs reference extraction |
| 4-5 | 300-500 lines — functional but could be leaner |
| 6-7 | 200-300 lines — good, most deep content in references |
| 8-9 | 150-250 lines — clean, focused on workflow |
| 10 | Under 200 lines with comprehensive reference files — maximum token efficiency |

**Benchmark:** options-payoff scores 8/10 (196 lines, 2 reference files handle the depth)

## Dimension 10: Domain Accuracy

Is the skill's domain knowledge correct and trustworthy?

| Score | Criteria |
|---|---|
| 1-3 | Factual errors, wrong formulas, misleading guidance |
| 4-5 | Mostly correct but some imprecise statements or outdated info |
| 6-7 | Accurate for main use cases, some edge cases not covered |
| 8-9 | Highly accurate, edge cases documented, disclaimers appropriate |
| 10 | Expert-level accuracy — could be used as a reference by domain practitioners |

**Benchmark:** options-payoff scores 9/10 (Black-Scholes correct, edge cases documented, disclaimer present)

---

## Scoring Summary Table

Copy this template when scoring a skill:

```
| # | Dimension | Score | Notes |
|---|---|---|---|
| 1 | Trigger quality | /10 | |
| 2 | Defaults coverage | /10 | |
| 3 | Step architecture | /10 | |
| 4 | Reference file strategy | /10 | |
| 5 | Dynamic content | /10 | |
| 6 | Output template | /10 | |
| 7 | Error handling | /10 | |
| 8 | Code/formula quality | /10 | |
| 9 | SKILL.md conciseness | /10 | |
| 10 | Domain accuracy | /10 | |
| **Total** | | **/100** | |
```

## Score Interpretation

| Range | Quality | Action |
|---|---|---|
| 90-100 | Exceptional | Ship as-is, use as template for new skills |
| 80-89 | Production | Ready to use, minor polish opportunities |
| 70-79 | Good | Functional, 2-3 targeted improvements recommended |
| 60-69 | Needs work | Usable but will frustrate users, prioritize fixes |
| Below 60 | Draft | Not ready for use, needs structural rework |
