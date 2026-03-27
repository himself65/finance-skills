# Finance Skills

> [!WARNING]
> This project is for educational and informational purposes only. Nothing here constitutes financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.

A collection of agent skills for financial analysis and trading.

See [DEMOS.md](DEMOS.md) for screenshots and examples.

### Paid API (subscription required)

| Skill | Description | Platform |
|---|---|---|
| [unusual-whales](skills/unusual-whales/) | Query the [Unusual Whales API](https://unusualwhales.com/public-api) for options flow, dark pool trades, congressional trading, institutional holdings, Greek exposure, volatility, screener, and 100+ endpoints. [Purchase API key](https://unusualwhales.com/pricing?product=api). | Claude Code |

## Setup

### Claude Code Plugin (recommended)

This repo is a [Claude Code plugin](https://code.claude.com/docs/en/plugins). Install it directly:

**Option A — Plugin marketplace**

Add the marketplace and install:

```bash
# Add the marketplace
/plugin marketplace add himself65/finance-skills

# Install the plugin
/plugin install finance-skills@finance-skills
```

**Option B — Local plugin (for development)**

```bash
claude --plugin-dir ./path/to/finance-skills
```

Once installed, skills are namespaced under `finance-skills:` (e.g., `/finance-skills:options-payoff`).

### Claude Code (Agent Skills)

**Option A — `npx skills add`**

```bash
npx skills add himself65/finance-skills
```

Install a specific skill:

```bash
npx skills add himself65/finance-skills --skill options-payoff
```

Install globally (available across all projects):

```bash
npx skills add himself65/finance-skills --skill options-payoff -g
```

**Option B — Manual installation**

Clone the repo and symlink (or copy) the skill into your Claude Code skills directory:

```bash
# Personal (all projects)
cp -r skills/options-payoff ~/.claude/skills/options-payoff

# Project-local (this project only)
cp -r skills/options-payoff .claude/skills/options-payoff
```

### Claude.ai (Web / Desktop App)

1. Go to **Settings > Capabilities** and enable **Code execution and file creation**
2. Download the zip for the skill you want from the [latest release](https://github.com/himself65/finance-skills/releases/latest) (e.g., `options-payoff.zip`)
3. In Claude, go to **Customize > Skills**
4. Click the **+** button and select **Upload a skill**
5. Select the zip file — the skill will appear in your skills list

Repeat steps 2–5 for each skill you want to install.

### Other Agents

The skills in this repo follow the [Agent Skills](https://agentskills.io) open standard. You can install them to any supported agent (Codex, Gemini CLI, GitHub Copilot, etc.) using:

```bash
npx skills add himself65/finance-skills -a <agent-name>
```

## Available Skills

### Analysis & Data

| Skill | Description | Platform |
|---|---|---|
| [options-payoff](skills/options-payoff/) | Generate interactive options payoff curve charts with dynamic parameter controls. Supports butterfly, vertical spread, calendar spread, iron condor, straddle, strangle, covered call, and more. | Claude.ai or [generative-ui](skills/generative-ui/) |
| [stock-correlation](skills/stock-correlation/) | Analyze stock correlations to find related companies, sector peers, and pair-trading candidates. Routes to sub-skills: co-movement discovery, return correlation, sector clustering, and realized correlation. | All platforms |
| [yfinance-data](skills/yfinance-data/) | Fetch financial and market data using yfinance — stock prices, historical OHLCV, financial statements, options chains, dividends, earnings, analyst recommendations, screener, and more. | All platforms |

### Geopolitical & Macro Risk

| Skill | Description | Platform |
|---|---|---|
| [hormuz-strait](skills/hormuz-strait/) | Real-time Strait of Hormuz monitoring — shipping transits, oil price impact, stranded vessels, insurance risk, diplomatic status, global trade impact, and crisis timeline via the Hormuz Strait Monitor API. | All platforms |

### Research & Sentiment

| Skill | Description | Platform |
|---|---|---|
| [discord-reader](skills/discord-reader/) | Read-only Discord research via [opencli](https://github.com/jackwener/opencli) — read trading server messages, search discussions, monitor crypto/market groups, and track sentiment in financial communities. Connects to Discord Desktop via CDP (no token needed). | Claude Code |
| [telegram-reader](skills/telegram-reader/) | Read-only Telegram channel reader via [tdl](https://github.com/iyear/tdl) — export messages from financial news channels, monitor crypto/market groups, and aggregate Telegram-based news feeds. One-time QR code login. | Claude Code |
| [twitter-reader](skills/twitter-reader/) | Read-only Twitter/X research via [opencli](https://github.com/jackwener/opencli) — search financial tweets, track analyst commentary, monitor earnings sentiment, and follow market discussions. No API keys needed (reuses Chrome browser session). | Claude Code |

### Visualization

| Skill | Description | Platform |
|---|---|---|
| [generative-ui](skills/generative-ui/) | Design system and guidelines for Claude's built-in generative UI (`show_widget`). Render interactive HTML/SVG widgets inline — charts, diagrams, dashboards, interactive explainers, and more. | Claude.ai built-in |

## License

MIT
