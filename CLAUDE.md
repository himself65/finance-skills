# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard. Skills are installable into Claude Code, Claude.ai, and other supported agents (Codex, Gemini CLI, GitHub Copilot, etc.).

## Repository structure

This repo is three things at once:
1. A **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json` + `plugins/`)
2. An **Agent Skills** repository (the `SKILL.md` files inside `plugins/<group>/skills/`)
3. An **opencli plugin monorepo** (`opencli-plugin.json` at root + `opencli-plugins/`) — Node code for adapters that some skills depend on

Skills are organized into plugin groups by usage; opencli plugins are separate Node packages.

```
.claude-plugin/
  marketplace.json        # Marketplace definition — lists all 6 plugins
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
    plugin.json
    .mcp.json             # Bundled MCP servers (tradingview — headless TradingView scanner, pinned to a git SHA)
    skills/...
  startup-tools/          # Startup analysis
    plugin.json
    skills/...
  ui-tools/               # Generative UI design system
    plugin.json
    skills/...
  skill-creator/          # Skill authoring, evaluation, and improvement
    plugin.json
    skills/...
opencli-plugin.json       # Top-level opencli MONOREPO manifest — declares sub-plugins
opencli-plugins/          # Source for opencli adapters (Node code, has tests)
  tradingview/            # TradingView desktop reader (drives the tradingview-reader skill)
    opencli-plugin.json   # Per-plugin manifest
    package.json          # Node package (type: module)
    *.js                  # one file per command (registers via cli({...}))
    lib/                  # shared helpers
    tests/                # node:test units
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

This repo ships as a Claude Code plugin marketplace containing 6 plugins:

| Plugin | Description |
|---|---|
| `finance-market-analysis` | Stock analysis, earnings, correlations, options via yfinance |
| `finance-social-readers` | Social media research feeds (Twitter, Discord, LinkedIn, Telegram, YC) |
| `finance-startup-tools` | Startup analysis frameworks |
| `finance-ui-tools` | Generative UI design system for Claude widgets |
| `finance-skill-creator` | Skill authoring, evaluation, and improvement |

- `.claude-plugin/marketplace.json` — marketplace listing with all 6 plugin entries.
- `plugins/<group>/plugin.json` — per-plugin manifest (name, version, keywords). Skills under `plugins/<group>/skills/` with SKILL.md frontmatter are auto-discovered by the plugin loader.
- `plugins/<group>/.mcp.json` — optional bundled MCP servers, started automatically when the plugin is enabled. Tools are namespaced `mcp__plugin_<plugin-name>_<server-name>__<tool>`. Currently: `data-providers/.mcp.json` runs [tradingview-mcp](https://github.com/atilaahmettaner/tradingview-mcp) via `uvx`, pinned to an upstream commit SHA (bump the SHA deliberately and re-verify `tools/list` — upstream reuses version numbers, so PyPI lags git).
- `.agents/` — auto-generated mirror for agent distribution. **Do not edit directly** — this is produced from `plugins/` content.

Users run `npx plugins add himself65/finance-skills` and select one or more plugin groups interactively; `--yes` installs every discovered group. The current `plugins` CLI has no `--plugin` flag. Individual skills can be installed via `npx skills add himself65/finance-skills --skill <name>`.

When a skill is invoked as a plugin, it is namespaced as `<plugin-name>:<skill-name>` (e.g., `/finance-market-analysis:options-payoff`).

## CI/CD

- **Release workflow** (`.github/workflows/release-skills.yml`): On tag push (`v*`), zips each skill from `plugins/*/skills/*/` and publishes them as a GitHub release. These zips can be uploaded to Claude.ai for web/desktop users.
- **Lint workflow** (`.github/workflows/skill-lint.yml`): Lints all `SKILL.md` files across all plugin groups. The linter caps `description` at 1024 chars and rejects angle brackets (`<` / `>`).
- **opencli plugin tests** (`.github/workflows/opencli-plugin-test.yml`): Walks `opencli-plugins/*/` and runs `npm test` for each plugin that has a `package.json` and `tests/*.test.js`. Pure-JS unit tests only — wire-level integration (CDP attach, scanner endpoints) is out of scope and must be PoC-verified against a real desktop app.

## opencli plugins

Some skills (currently `tradingview-reader`) require a custom opencli adapter that is **not** part of opencli's built-in registry. Those adapters live under `opencli-plugins/` as a Node monorepo, declared by the top-level `opencli-plugin.json`.

### Layout

- `opencli-plugin.json` (repo root) — opencli's monorepo manifest. Maps each sub-plugin name to its directory.
- `opencli-plugins/<name>/` — one directory per adapter. Each contains:
  - `opencli-plugin.json` — per-plugin manifest (name, version, opencli compatibility range)
  - `package.json` — Node package, `"type": "module"`, peer dep on `@jackwener/opencli`
  - `<command>.js` files at the top level — each registers itself via `cli({ site, name, ... })` from `@jackwener/opencli/registry`
  - `lib/` — shared helpers (decoders, parsers)
  - `tests/` — `node:test` units; run with `npm test` from inside the plugin directory

### Install path for users

```bash
opencli plugin install github:himself65/finance-skills/<sub-plugin-name>
```

The third path segment selects the sub-plugin. A bare `github:himself65/finance-skills` install would pick up every enabled sub-plugin from the monorepo.

### Authoring a new opencli plugin

1. Create `opencli-plugins/<name>/` with `opencli-plugin.json`, `package.json`, and at least one command file.
2. Each command file imports `cli, Strategy` from `@jackwener/opencli/registry` and calls `cli({...})` at module top level.
3. For desktop-app adapters (CDP attach), use `Strategy.UI` + `browser: true` + `domain: '<host>'`. For pure HTTP, use `Strategy.PUBLIC` + `browser: false`.
4. Add the new sub-plugin to the top-level `opencli-plugin.json` `plugins` map.
5. Tests for pure helpers belong in `tests/` and should pass with `npm test`.
6. The skill that drives the plugin lives under `plugins/<group>/skills/<name>/` and must reference the install command exactly as shown above.

## Important constraints

- **No trade execution.** All brokerage-related skills must be read-only. Never allow AI to execute trades.
- This is primarily a documentation/reference repository — most of the codebase is `SKILL.md` files with no build step. The exception is `opencli-plugins/`, which is real Node code with tests; quality there comes from passing tests and PoC verification, not just clear instructions.
