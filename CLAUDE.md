# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard. Skills are installable into Claude Code, Claude.ai, and other supported agents (Codex, Gemini CLI, GitHub Copilot, etc.).

## Repository structure

This repo is both a Claude Code plugin marketplace and an Agent Skills repository. Skills are organized into plugin groups by usage.

```
.claude-plugin/
  marketplace.json        # Marketplace definition — lists all 4 plugins
plugins/
  market-analysis/        # Stock analysis, earnings, correlations, options via yfinance
    plugin.json           # Plugin manifest for this group
    skills/
      <skill-name>/
        SKILL.md
        README.md
        references/
  social-readers/         # Social media research feeds (Twitter, Discord, LinkedIn, Telegram, YC)
    plugin.json
    skills/...
  data-providers/         # External API data (Adanos, Funda AI, Hormuz Strait)
    plugin.json
    skills/...
  startup-tools/          # Startup analysis + generative UI
    plugin.json
    skills/...
workspaces/               # Development workspaces (not distributed)
.agents/                  # Auto-generated mirror for agent distribution (do not edit directly)
.github/workflows/
  release-skills.yml      # Zips each skill and publishes as GitHub release on tag
  skill-lint.yml          # Lints all SKILL.md files
```

## How skills work

Each skill is a self-contained directory under `plugins/<group>/skills/`. The `SKILL.md` file is what Claude reads at runtime — it tells the model when to activate, what steps to follow, and where to find reference details.

### SKILL.md format

```markdown
---
name: skill-name
description: >
  Multi-line description that doubles as the trigger definition.
  Include specific phrases, keywords, and scenarios that should activate this skill.
---

# Skill Title

Step-by-step instructions organized as ## Step N sections.
Tables, code blocks, and formulas as needed.

## Reference Files

- `references/foo.md` — description
```

**Required frontmatter fields:** `name`, `description`

The `description` field is critical — it controls when the skill activates. Write it as a comprehensive trigger list, not a summary.

### Reference files

Markdown documents in `references/` containing detailed API references, code templates, formulas, or schema docs. The SKILL.md instructions tell the model to read specific reference files when needed, keeping the main instructions concise.

## Creating a new skill

1. Choose the appropriate plugin group (`market-analysis`, `social-readers`, `data-providers`, or `startup-tools`)
2. Create `plugins/<group>/skills/<skill-name>/` directory
3. Write `SKILL.md` with YAML frontmatter (`name`, `description`) and step-by-step instructions
4. Add reference files under `references/` for detailed API docs, code templates, or formulas that would bloat the main instructions
5. Add a `README.md` for the skill's GitHub page (description, triggers, platform, setup, reference file list)
6. Update the root `README.md` to list the new skill in the appropriate plugin group table
7. The skill will be auto-zipped and released on tag push via GitHub Actions

### Platform considerations

Skills that require shell access, network calls, or external binaries (e.g., twitter-cli, pip install) only work on **CLI-based agents** like Claude Code. They do **not** work on Claude.ai, which runs in a sandboxed environment that restricts network access and binaries.

Skills that only use Claude's built-in tools (e.g., `show_widget` for generative-ui) work on **Claude.ai**.

### Dynamic content with `!`command``

Skills can embed shell commands that Claude Code executes at skill invocation time, injecting the output inline. Use this for runtime environment checks (tool installation status, auth state, live data). Syntax: wrap in a fenced code block with `` !`command` ``.

Example — checking if a CLI tool is installed and authenticated:
```
!`(command -v mytool && mytool status 2>&1 | head -5 && echo "AUTH_OK" || echo "AUTH_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

Guidelines:
- Use for environment/auth checks so the model skips install/auth steps when unnecessary
- Use for injecting live data (e.g., current stock prices) to replace hardcoded values
- Keep commands fast (< 2s) — they run synchronously before the skill loads
- Always include fallback output (e.g., `|| echo "UNAVAILABLE"`) so the skill degrades gracefully
- Only works on CLI-based agents (Claude Code) — Claude.ai ignores these

### Instruction style guidelines

- Organize as numbered steps (## Step 1, Step 2, etc.)
- Use tables to map user intents to actions/methods
- Include defaults for missing parameters so the skill works with partial input
- Put lengthy code templates and API references in `references/` files, not inline
- End with a "Respond to the User" step describing how to present results

## Plugin system

This repo ships as a Claude Code plugin marketplace containing 4 plugins:

| Plugin | Description |
|---|---|
| `finance-market-analysis` | Stock analysis, earnings, correlations, options via yfinance |
| `finance-social-readers` | Social media research feeds (Twitter, Discord, LinkedIn, Telegram, YC) |
| `finance-data-providers` | External API data (Adanos, Funda AI, Hormuz Strait) |
| `finance-startup-tools` | Startup analysis + generative UI design system |

- `.claude-plugin/marketplace.json` — marketplace listing with all 4 plugin entries.
- `plugins/<group>/plugin.json` — per-plugin manifest (name, version, keywords). Skills under `plugins/<group>/skills/` with SKILL.md frontmatter are auto-discovered by the plugin loader.
- `.agents/` — auto-generated mirror for agent distribution. **Do not edit directly** — this is produced from `plugins/` content.

Users install all plugins via `npx plugins add himself65/finance-skills`. Individual plugins can be installed via `npx plugins add himself65/finance-skills --plugin <plugin-name>`. Individual skills can be installed via `npx skills add himself65/finance-skills --skill <name>`.

When a skill is invoked as a plugin, it is namespaced as `<plugin-name>:<skill-name>` (e.g., `/finance-market-analysis:options-payoff`).

## CI/CD

- **Release workflow** (`.github/workflows/release-skills.yml`): On tag push (`v*`), zips each skill from `plugins/*/skills/*/` and publishes them as a GitHub release. These zips can be uploaded to Claude.ai for web/desktop users.
- **Lint workflow** (`.github/workflows/skill-lint.yml`): Lints all `SKILL.md` files across all plugin groups.

## Important constraints

- **No trade execution.** All brokerage-related skills must be read-only. Never allow AI to execute trades.
- This is a documentation/reference repository — no build system, no tests. Quality comes from clear, accurate skill instructions.
