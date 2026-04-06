# Finance Skills

> [!WARNING]
> This project is for educational and informational purposes only. Nothing here constitutes financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard.

**Visit [finance-skills.himself65.com](https://finance-skills.himself65.com/) for documentation, demos, and setup instructions.**

## Quick Start

### Claude Code — Plugin (recommended)

```bash
npx plugins add himself65/finance-skills
```

### Claude Code — Individual Skills

```bash
npx skills add himself65/finance-skills
```

### Other Agents

```bash
npx skills add himself65/finance-skills -a <agent-name>
```

## Available Skills

### Analysis & Data

| Skill | Description | Platform |
|---|---|---|
| [earnings-preview](skills/earnings-preview/) | Pre-earnings briefing — consensus estimates, beat/miss history, analyst sentiment | All |
| [earnings-recap](skills/earnings-recap/) | Post-earnings analysis — actual vs estimated EPS, price reaction, margin trends | All |
| [estimate-analysis](skills/estimate-analysis/) | Analyst estimate deep-dive — revision trends, growth projections, historical accuracy | All |
| [options-payoff](skills/options-payoff/) | Interactive options payoff charts with dynamic controls | Claude.ai |
| [saas-valuation-compression](skills/saas-valuation-compression/) | SaaS valuation compression analysis — ARR multiples, cause attribution, peer comparisons | All |
| [startup-analysis](skills/startup-analysis/) | Multi-perspective startup analysis — VC investor, job applicant, and CEO/founder viewpoints | Claude Code |
| [stock-correlation](skills/stock-correlation/) | Correlation analysis — sector peers, co-movement, pair-trading candidates | All |
| [stock-liquidity](skills/stock-liquidity/) | Liquidity analysis — spreads, volume profiles, market impact, Amihud ratio | All |
| [yfinance-data](skills/yfinance-data/) | Market data via yfinance — prices, financials, options, dividends, earnings | All |

### Paid Data Providers

| Skill | Description | Platform |
|---|---|---|
| [funda-data](skills/funda-data/) | [Funda AI](https://funda.ai) API — real-time quotes, fundamentals, options flow, sentiment, SEC filings, and 60+ endpoints | Claude Code |
| [finance-sentiment](skills/finance-sentiment/) | Stock sentiment research via Adanos Finance API — Reddit, X.com, news, Polymarket | Claude Code |

### Geopolitical & Macro Risk

| Skill | Description | Platform |
|---|---|---|
| [hormuz-strait](skills/hormuz-strait/) | Strait of Hormuz monitoring — shipping, oil impact, insurance risk, crisis timeline | All |

### Research & Sentiment

| Skill | Description | Platform |
|---|---|---|
| [discord-reader](skills/discord-reader/) | Read-only Discord research via [opencli](https://github.com/jackwener/opencli) | Claude Code |
| [linkedin-reader](skills/linkedin-reader/) | Read-only LinkedIn feed & job search via [opencli](https://github.com/jackwener/opencli) | Claude Code |
| [telegram-reader](skills/telegram-reader/) | Read-only Telegram channel reader via [tdl](https://github.com/iyear/tdl) | Claude Code |
| [twitter-reader](skills/twitter-reader/) | Read-only Twitter/X research via [opencli](https://github.com/jackwener/opencli) | Claude Code |
| [yc-reader](skills/yc-reader/) | Y Combinator company data via [yc-oss/api](https://github.com/yc-oss/api) | Claude Code |

### Visualization

| Skill | Description | Platform |
|---|---|---|
| [generative-ui](skills/generative-ui/) | Generative UI design system for Claude's `show_widget` | Claude.ai |

## License

MIT
