# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard. Skills are installable into Claude Code, Claude.ai, and other supported agents (Codex, Gemini CLI, GitHub Copilot, etc.).

## Repository structure

This repo is both a Claude Code plugin and an Agent Skills repository.

```
.claude-plugin/
  plugin.json             # Claude Code plugin manifest
  marketplace.json        # Plugin marketplace definition
skills/
  <skill-name>/
    SKILL.md              # Skill definition (frontmatter + body instructions)
    README.md             # Skill documentation for GitHub
    references/           # Supporting reference files (markdown)
.agents/                  # Auto-generated mirror for agent distribution (do not edit directly)
.github/workflows/
  release-skills.yml      # Zips each skill and publishes as GitHub release on push to main
```

## How skills work

Each skill is a self-contained directory under `skills/`. The `SKILL.md` file is what Claude reads at runtime — it tells the model when to activate, what steps to follow, and where to find reference details.

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

1. Create `skills/<skill-name>/` directory
2. Write `SKILL.md` with YAML frontmatter (`name`, `description`) and step-by-step instructions
3. Add reference files under `references/` for detailed API docs, code templates, or formulas that would bloat the main instructions
4. Add a `README.md` for the skill's GitHub page (description, triggers, platform, setup, reference file list)
5. Update the root `README.md` to list the new skill in the appropriate category table
6. The skill will be auto-zipped and released on merge to main via GitHub Actions

### Platform considerations

Skills that require shell access, network calls, or external binaries (e.g., twitter-cli, pip install) only work on **CLI-based agents** like Claude Code. They do **not** work on Claude.ai, which runs in a sandboxed environment that restricts network access and binaries.

Skills that only use Claude's built-in tools (e.g., `show_widget` for generative-ui) work on **Claude.ai**.

### Instruction style guidelines

- Organize as numbered steps (## Step 1, Step 2, etc.)
- Use tables to map user intents to actions/methods
- Include defaults for missing parameters so the skill works with partial input
- Put lengthy code templates and API references in `references/` files, not inline
- End with a "Respond to the User" step describing how to present results

## CI/CD

- **Release workflow** (`.github/workflows/release-skills.yml`): On push to `main`, zips each `skills/*/` directory and publishes them as a GitHub release tagged `latest`. These zips are what users upload to Claude.ai.

## Important constraints

- **No trade execution.** All brokerage-related skills must be read-only. Never allow AI to execute trades.
- This is a documentation/reference repository — no build system, no package.json, no tests. Quality comes from clear, accurate skill instructions.
