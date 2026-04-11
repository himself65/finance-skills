# skill-creator

Create, evaluate, and iterate on high-quality agent skills with structured guidance, quality scoring, and best-practice enforcement.

## What it does

- **Create** new skills from scratch with step-by-step guidance through architecture planning, SKILL.md writing, reference file creation, and quality validation
- **Evaluate** existing skills against a 10-dimension quality rubric (trigger quality, defaults, step architecture, reference strategy, output template, etc.) with benchmark comparisons
- **Improve** skills by scoring them, proposing ranked improvements, and applying targeted patches

The skill encodes patterns extracted from analyzing 20+ production finance skills and 120+ hermes-agent skills, distilling what separates top-tier skills (sepa-strategy, options-payoff) from mediocre ones.

**Core rule:** Skills must always detect available tools at runtime and adapt with decision trees and fallback paths — never hardcode a single method.

## Triggers

- "create a skill", "make a new skill", "build a skill for", "write a skill that"
- "improve this skill", "optimize this skill", "this skill isn't working well"
- "evaluate this skill", "score this skill", "how good is this skill"
- "run evals on", "benchmark this skill", "test this skill's quality"
- "turn this into a skill", "I keep doing X manually", "can you remember how to do X"

## Platform

Works on **Claude Code** and other CLI-based agents. Also works on **Claude.ai** for evaluation and planning (skill file creation requires CLI).

## Setup

```bash
# As a plugin (recommended)
npx plugins add himself65/finance-skills --plugin finance-skill-creator

# Or install just this skill
npx skills add himself65/finance-skills --skill skill-creator
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/dynamic-calling.md` -- **Core**: Detection flows, decision trees, method fallbacks, runtime awareness, 9 patterns from production skills
- `references/architecture-patterns.md` -- Linear, Router, Methodology, Widget, and API Wrapper patterns with examples and anti-patterns
- `references/frontmatter-guide.md` -- Complete YAML frontmatter field reference (name, description, platform, env vars, config, credentials)
- `references/quality-rubric.md` -- 10-dimension scoring rubric with 1-10 scales, benchmark scores, and score interpretation
- `references/skill-examples.md` -- Annotated excerpts from top skills showing why specific patterns work
- `references/writing-guide.md` -- How to write each SKILL.md section, detection flows, defaults tables, and output templates
