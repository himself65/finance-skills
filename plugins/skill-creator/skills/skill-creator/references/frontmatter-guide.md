# SKILL.md Frontmatter Reference

Complete field reference for the YAML frontmatter block that starts every SKILL.md file.

## Required Fields

### `name`
- **Type:** string
- **Max length:** 64 characters
- **Pattern:** `^[a-z0-9][a-z0-9._-]*$` (lowercase alphanumeric, hyphens, dots, underscores)
- **Purpose:** Unique identifier used in slash commands, file paths, and skill references

```yaml
name: my-skill-name
```

### `description`
- **Type:** string (multi-line with `>` recommended)
- **Max length:** 1024 characters
- **Purpose:** Controls when the skill activates. This is the most important field for skill quality.

```yaml
description: >
  [What it does] Analyze stocks using the SEPA methodology.
  [Expert triggers] SEPA, Minervini, VCP, trend template, Stage 2, pivot point.
  [Beginner triggers] "should I buy this stock", "is this a good setup".
  [Context triggers] When user shares a chart, mentions swing trading criteria.
```

**Writing a high-quality description:**

1. Start with a concrete action verb: "Analyze", "Generate", "Fetch", "Evaluate" (not "Use" or "Handle")
2. Name specific tools/APIs: "via yfinance", "using the Funda AI API"
3. List 5+ explicit trigger phrases in quotes
4. Include 2+ sideways entry points (unexpected phrasings)
5. End with context triggers ("also when the user...")

**Common mistakes:**
- Too short: "Analyze stocks" — won't trigger on specific requests
- Too generic: "Financial analysis tool" — triggers on everything, useful for nothing
- Missing beginner terms: Only expert jargon excludes most users

## Optional Fields

### `version`
Semantic version for the skill. Useful for tracking changes.
```yaml
version: 1.0.0
```

### `author`
Creator name or handle.
```yaml
author: himself65
```

### `license`
License identifier.
```yaml
license: MIT
```

### `platforms`
Restrict to specific operating systems. Omit to load on all platforms (default).
```yaml
platforms: [macos, linux]   # Valid values: macos, linux, windows
```

### `required_environment_variables`
Declare API keys or tokens the skill needs. These are secrets stored in `~/.hermes/.env`.

```yaml
required_environment_variables:
  - name: FUNDA_API_KEY
    prompt: "Funda AI API key"
    help: "Get one at https://funda.ai/dashboard"
    required_for: "API access"
```

Fields per entry:
- `name` (required) — environment variable name
- `prompt` (optional) — text shown when asking the user
- `help` (optional) — URL or help text for obtaining the value
- `required_for` (optional) — which feature needs this variable

### `required_credential_files`
Declare file-based credentials (OAuth tokens, certificates).

```yaml
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
```

### `metadata.hermes`
Hermes-specific metadata for discovery, activation, and configuration.

```yaml
metadata:
  hermes:
    tags: [Finance, Market Analysis, Options]
    related_skills: [yfinance-data, earnings-preview]
    category: market-analysis
```

### Conditional Activation

Control when the skill appears in the system prompt:

```yaml
metadata:
  hermes:
    requires_toolsets: [web]              # Hide if web toolset NOT active
    requires_tools: [web_search]          # Hide if web_search NOT available
    fallback_for_toolsets: [browser]      # Hide if browser IS active
    fallback_for_tools: [browser_navigate] # Hide if browser_navigate IS available
```

| Field | Logic |
|---|---|
| `requires_toolsets` | Hidden when ANY listed toolset is unavailable |
| `requires_tools` | Hidden when ANY listed tool is unavailable |
| `fallback_for_toolsets` | Hidden when ANY listed toolset IS available |
| `fallback_for_tools` | Hidden when ANY listed tool IS available |

### Config Settings

Non-secret settings stored in `config.yaml`:

```yaml
metadata:
  hermes:
    config:
      - key: wiki.path
        description: Path to knowledge base directory
        default: "~/wiki"
        prompt: "Wiki directory path"
```

## Complete Frontmatter Example

```yaml
---
name: sepa-strategy
description: >
  Analyze stocks using Mark Minervini's SEPA methodology.
  Triggers: SEPA, Minervini, VCP, trend template, Stage 2, pivot point,
  superperformance, bullish stacking, breakout volume, cup-with-handle,
  "should I buy this stock", "is this a good setup", growth stock screening.
version: 1.0.0
author: himself65
license: MIT
metadata:
  hermes:
    tags: [Finance, Trading, Technical Analysis]
    related_skills: [yfinance-data, stock-correlation]
---
```

## Size Constraints Summary

| Field | Limit |
|---|---|
| `name` | 64 characters |
| `description` | 1024 characters |
| SKILL.md total content | 100,000 characters |
| Supporting files | 1 MiB each |
| Category name | 64 characters, single directory level |
