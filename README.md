# Finance Skills

A collection of agent skills for financial analysis and trading.

## Demo

### options-payoff — Butterfly Spread

![Options Payoff Demo](skills/options-payoff/options-payoff-demo.png)

## Available Skills

| Skill | Description |
|---|---|
| [options-payoff](skills/options-payoff/) | Generate interactive options payoff curve charts with dynamic parameter controls. Supports butterfly, vertical spread, calendar spread, iron condor, straddle, strangle, covered call, and more. |
| [yfinance-data](skills/yfinance-data/) | Fetch financial and market data using yfinance — stock prices, historical OHLCV, financial statements, options chains, dividends, earnings, analyst recommendations, screener, and more. |

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
