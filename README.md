# Finance Skills

> [!WARNING]
> This project is for educational and informational purposes only. Nothing here constitutes financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.

A collection of agent skills for financial analysis and trading.

## Demo

### options-payoff — Bull Call Spread

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/options-payoff-bull-call-spread-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/options-payoff-bull-call-spread.png">
  <img alt="Options Payoff — Bull Call Spread for MSFT" src="assets/options-payoff-bull-call-spread.png">
</picture>


## Available Skills

### Analysis & Data

| Skill | Description | Platform |
|---|---|---|
| [options-payoff](skills/options-payoff/) | Generate interactive options payoff curve charts with dynamic parameter controls. Supports butterfly, vertical spread, calendar spread, iron condor, straddle, strangle, covered call, and more. | Claude.ai or [generative-ui](skills/generative-ui/) |
| [yfinance-data](skills/yfinance-data/) | Fetch financial and market data using yfinance — stock prices, historical OHLCV, financial statements, options chains, dividends, earnings, analyst recommendations, screener, and more. | All platforms |

### Research & Sentiment

| Skill | Description | Platform |
|---|---|---|
| [telegram-news](skills/telegram-news/) | Read-only Telegram channel reader via [tdl](https://github.com/iyear/tdl) — export messages from financial news channels, monitor crypto/market groups, and aggregate Telegram-based news feeds. One-time QR code login. | Claude Code |
| [twitter](skills/twitter/) | Read-only Twitter/X research via [twitter-cli](https://github.com/jackwener/twitter-cli) — search financial tweets, track analyst commentary, monitor earnings sentiment, and follow market discussions. No API keys needed (uses browser cookies). | All platforms |

### Visualization

| Skill | Description | Platform |
|---|---|---|
| [generative-ui](skills/generative-ui/) | Design system and guidelines for Claude's built-in generative UI (`show_widget`). Render interactive HTML/SVG widgets inline — charts, diagrams, dashboards, interactive explainers, and more. | Claude.ai built-in |

## Setup

### Claude Code (CLI)

**Option A — `npx skills add` (recommended)**

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

## License

MIT
