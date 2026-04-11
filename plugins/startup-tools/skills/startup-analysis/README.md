# startup-analysis

Multi-perspective startup analysis skill — evaluate any startup from VC investor, job applicant, and CEO/founder viewpoints.

## What it does

Produces a comprehensive startup analysis by examining the company through three distinct lenses:

- **VC Investor** — Market opportunity, unit economics, team quality, defensibility, investment verdict
- **Job Applicant** — Financial stability, equity value, career growth, culture signals, employment verdict
- **CEO/Founder** — Product-market fit, growth efficiency, competitive position, organizational health, health grade

Each perspective surfaces different insights. A company can be a great investment but a terrible place to work (or vice versa). The skill cross-references findings to highlight where perspectives agree and diverge.

**This skill uses web search** to gather public information about the startup before analysis.

## Triggers

- "analyze this startup", "evaluate [company]", "should I join [company]"
- "is [company] a good investment", "due diligence on [company]"
- "what do you think of [startup]", "research [company] for me"
- "startup assessment", "company analysis", "evaluate this company"
- Any mention of evaluating, analyzing, or assessing a startup from investment, career, or strategic perspectives

## Platform

Works on **Claude Code** and other CLI-based agents (web search required). May work on **Claude.ai** with reduced data gathering capability.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-startup-tools

# Or install just this skill
npx skills add himself65/finance-skills --skill startup-analysis
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/vc-framework.md` — VC due diligence checklist with metrics and benchmarks
- `references/job-applicant-framework.md` — Job seeker evaluation framework with equity analysis
- `references/ceo-framework.md` — CEO self-assessment with operational metrics
