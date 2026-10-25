# AGENTS.md

This file provides guidance to coding agents (Claude Code, OpenAI Codex, and any other tool that reads `AGENTS.md`) when working with code in this repository. `CLAUDE.md` is a one-line `@AGENTS.md` import so Claude Code loads the same file — edit this one, never that stub.

## Project overview

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard. Skills are installable into Claude Code, Claude.ai, and other supported agents (Codex, Gemini CLI, GitHub Copilot, etc.).

## Repository structure

This repo is three things at once:
1. A **Claude Code and OpenAI Codex plugin marketplace** (`.claude-plugin/marketplace.json`, generated `.agents/plugins/marketplace.json`, and `plugins/`)
2. An **Agent Skills** repository (the `SKILL.md` files inside `plugins/<group>/skills/`)
3. An **opencli plugin monorepo** (`opencli-plugin.json` at root + `opencli-plugins/`) — Node code for adapters that some skills depend on

Skills are organized into plugin groups by usage; opencli plugins are separate Node packages.

```
AGENTS.md                 # Agent instructions (this file); CLAUDE.md is an `@AGENTS.md` stub
.claude-plugin/
  marketplace.json        # Marketplace definition — lists all 6 plugins
plugins/
  market-analysis/        # Stock analysis, earnings, correlations, options via yfinance
    plugin.json           # Portable Agent Plugins manifest + extensions.com.openai
    .codex-plugin/        # Generated compatibility manifest; do not edit directly
    skills/
      <skill-name>/
        SKILL.md
        README.md
        references/
  social-readers/         # Social media research feeds (Twitter, Discord, LinkedIn, Telegram, YC)
    plugin.json
    skills/...
  data-providers/         # External API data (Adanos, Fintel, Hormuz Strait, TradingView, Hyperliquid)
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
.agents/plugins/          # Generated Codex marketplace (do not edit directly)
scripts/                  # Stdlib Python metadata generation, packaging, tests, Codex smoke
.github/workflows/
  release-skills.yml      # Zips each skill and publishes as GitHub release on tag
  skill-lint.yml          # Lints all SKILL.md files
  plugin-packages.yml     # Checks generated metadata and tests/builds release packages
```

## How skills work

Each skill is a self-contained directory under `plugins/<group>/skills/`. The `SKILL.md` file is what Claude reads at runtime — it tells the model when to activate, what steps to follow, and where to find reference details.

### SKILL.md format

```markdown
---
name: skill-name
description: >
  Multi-line description that doubles as the trigger definition.
  Name the categories of requests that should activate this skill and the
  distinctive vocabulary users will use.
---

# Skill Title

Numbered ## Step N sections where order matters; goals, criteria, and domain
heuristics for judgment work. Tables, code blocks, and formulas as needed.

## Reference Files

- `references/foo.md` — description
```

**Required frontmatter fields:** `name`, `description`

The `description` field controls when the skill activates and rides along in every session, so treat it as routing text: say what the skill does, name every category of request it serves with the distinctive vocabulary (methods, tools, data types, example tickers), and point to sibling skills for neighboring requests. Name categories rather than listing near-synonymous phrasings, and keep behavioral instructions in the body.

### Reference files

Markdown documents in `references/` containing detailed API references, code templates, formulas, or schema docs. The SKILL.md instructions tell the model to read specific reference files when needed, keeping the main instructions concise.

## Creating a new skill

1. Choose the appropriate plugin group (`market-analysis`, `social-readers`, `data-providers`, or `startup-tools`)
2. Create `plugins/<group>/skills/<skill-name>/` directory
3. Write `SKILL.md` with YAML frontmatter (`name`, `description`) and instructions that follow the style guidelines below
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
- Only Claude Code runs these before the skill loads — Claude.ai ignores them, and Codex does not preprocess them. So every skill with probes starts with the line "If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation." Keep that line when you add probes to a skill.

### Instruction style guidelines

Skills are read by current Claude models, which follow instructions closely and literally and plan multi-step work on their own. Write for that reader:

- Use numbered steps (## Step 1, Step 2, etc.) where order matters — setup, data fetch, computation, gates. For judgment work (analysis, interpretation, writing), state the goal, the criteria, and the domain heuristics rather than scripting it.
- Give exact commands and code for fragile operations (installs, auth, CLI flags, API calls, formulas), and put arithmetic in code rather than asking the model to estimate it.
- Use tables to map user intents to actions/methods
- Include defaults for missing parameters so the skill works with partial input
- State each constraint once, in plain words, with its reason. Skip capitalized MUST/NEVER/CRITICAL, repeated warnings, and instructions the model follows by default ("be thorough", "think step by step", "double-check").
- End with a "Respond to the User" step that states an output contract — what to lead with, what must be covered, required caveats, any verdict scale — rather than a fill-in template. Describe length qualitatively, and label examples as illustrative instead of filling them with invented figures for real companies.
- Put lengthy code templates, API references, and dated datasets in `references/` files, not inline, and date-stamp anything that will go stale.
- Keep maintainer notes and change history in the skill's `README.md`, not in `SKILL.md`.
- When you touch a skill, verify its API names and response shapes against the current library version.

## Plugin system

This repo ships as a Claude Code and OpenAI Codex plugin marketplace containing 6 plugins:

| Plugin | Description |
|---|---|
| `finance-market-analysis` | Stock analysis, earnings, correlations, options via yfinance |
| `finance-social-readers` | Social media research feeds (Twitter, Discord, LinkedIn, Telegram, YC) |
| `finance-data-providers` | External API data (Adanos, Fintel, Hormuz Strait, TradingView MCP + desktop reader, Hyperliquid) |
| `finance-startup-tools` | Startup analysis frameworks |
| `finance-ui-tools` | Generative UI design system for Claude widgets |
| `finance-skill-creator` | Skill authoring, evaluation, and improvement |

- `.claude-plugin/marketplace.json` — marketplace listing with all 6 plugin entries.
- `.agents/plugins/marketplace.json` — generated native Codex marketplace, built from the plugin inventory and manifests. **Do not edit directly** — use `npm run plugins:sync`. Register with `codex plugin marketplace add himself65/finance-skills`, then install a group with `codex plugin add finance-market-analysis@finance-skills`.
- `plugins/<group>/.codex-plugin/plugin.json` and `plugins/data-providers/mcp.json` — generated Codex compatibility and portable MCP metadata. Run `npm run plugins:sync` after editing source manifests or `.mcp.json`; CI checks for drift. See `docs/codex.md` for installation and release details.
- `plugins/<group>/plugin.json` — per-plugin manifest (name, version, keywords). Skills under `plugins/<group>/skills/` with SKILL.md frontmatter are auto-discovered by the plugin loader.
- `plugins/<group>/.mcp.json` — optional bundled MCP servers, started automatically when the plugin is enabled. Tools are namespaced `mcp__plugin_<plugin-name>_<server-name>__<tool>`. Currently: `data-providers/.mcp.json` runs [tradingview-mcp](https://github.com/atilaahmettaner/tradingview-mcp) via `uvx`, pinned to an upstream commit SHA (bump the SHA deliberately and re-verify `tools/list` — upstream reuses version numbers, so PyPI lags git).

Users run `npx plugins add himself65/finance-skills` and select one or more plugin groups interactively; `--yes` installs every discovered group. The current `plugins` CLI has no `--plugin` flag. Individual skills can be installed via `npx skills add himself65/finance-skills --skill <name>`.

When a skill is invoked as a plugin, it is namespaced as `<plugin-name>:<skill-name>` (e.g., `/finance-market-analysis:options-payoff`). Codex uses the same name (`finance-market-analysis:options-payoff`); mention it with `$`, or ask in plain language and the description triggers it.

## CI/CD

- **Release workflow** (`.github/workflows/release-skills.yml`): On tag push (`v*`), validates the tag against manifest versions and publishes individual skill ZIPs, six plugin ZIPs, a local marketplace ZIP, and SHA-256 checksums. `pnpm bump` synchronizes generated Codex files before committing/tagging. Prereleases do not replace the latest stable release.
- **Plugin package checks** (`.github/workflows/plugin-packages.yml`): Runs `python3 scripts/package_plugins.py check`, packaging regression tests, and the release build. `npm run plugins:smoke` additionally checks the built archive through a locally installed Codex loader.
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
