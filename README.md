# Finance Skills

> [!WARNING]
> This project is for educational and informational purposes only. Nothing here constitutes financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard.

**Visit [finance-skills.himself65.com](https://finance-skills.himself65.com/) for documentation, demos, and setup instructions.**

## Quick Start

### Claude Code — All Plugins

```bash
npx plugins add himself65/finance-skills
```

### Claude Code — Individual Plugins

```bash
npx plugins add himself65/finance-skills --plugin finance-market-analysis
npx plugins add himself65/finance-skills --plugin finance-social-readers
npx plugins add himself65/finance-skills --plugin finance-data-providers
npx plugins add himself65/finance-skills --plugin finance-startup-tools
npx plugins add himself65/finance-skills --plugin finance-ui-tools
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

### Market Analysis (`finance-market-analysis`)

Stock analysis, earnings, estimates, correlations, liquidity, ETFs, options payoff, and trading strategies via yfinance.

| Skill | Description |
|---|---|
| [earnings-preview](plugins/market-analysis/skills/earnings-preview/) | Pre-earnings briefing — consensus estimates, beat/miss history, analyst sentiment |
| [earnings-recap](plugins/market-analysis/skills/earnings-recap/) | Post-earnings analysis — actual vs estimated EPS, price reaction, margin trends |
| [estimate-analysis](plugins/market-analysis/skills/estimate-analysis/) | Analyst estimate deep-dive — revision trends, growth projections, historical accuracy |
| [etf-premium](plugins/market-analysis/skills/etf-premium/) | ETF premium/discount vs NAV — market price comparison, peer analysis, category screener |
| [options-payoff](plugins/market-analysis/skills/options-payoff/) | Interactive options payoff charts with dynamic controls |
| [saas-valuation-compression](plugins/market-analysis/skills/saas-valuation-compression/) | SaaS valuation compression analysis — ARR multiples, cause attribution, peer comparisons |
| [sepa-strategy](plugins/market-analysis/skills/sepa-strategy/) | SEPA strategy analysis — Minervini's trend template, VCP patterns, entry points, position sizing |
| [stock-correlation](plugins/market-analysis/skills/stock-correlation/) | Correlation analysis — sector peers, co-movement, pair-trading candidates |
| [stock-liquidity](plugins/market-analysis/skills/stock-liquidity/) | Liquidity analysis — spreads, volume profiles, market impact, Amihud ratio |
| [yfinance-data](plugins/market-analysis/skills/yfinance-data/) | Market data via yfinance — prices, financials, options, dividends, earnings |

### Social Readers (`finance-social-readers`)

Read-only social media and research feeds — Twitter/X, Discord, LinkedIn, Telegram, and Y Combinator.

| Skill | Description |
|---|---|
| [discord-reader](plugins/social-readers/skills/discord-reader/) | Read-only Discord research via [opencli](https://github.com/jackwener/opencli) |
| [linkedin-reader](plugins/social-readers/skills/linkedin-reader/) | Read-only LinkedIn feed & job search via [opencli](https://github.com/jackwener/opencli) |
| [telegram-reader](plugins/social-readers/skills/telegram-reader/) | Read-only Telegram channel reader via [tdl](https://github.com/iyear/tdl) |
| [twitter-reader](plugins/social-readers/skills/twitter-reader/) | Read-only Twitter/X research via [opencli](https://github.com/jackwener/opencli) |
| [yc-reader](plugins/social-readers/skills/yc-reader/) | Y Combinator company data via [yc-oss/api](https://github.com/yc-oss/api) |

### Data Providers (`finance-data-providers`)

External API data — sentiment via Adanos, comprehensive data via Funda AI, and Hormuz Strait monitoring.

| Skill | Description |
|---|---|
| [finance-sentiment](plugins/data-providers/skills/finance-sentiment/) | Stock sentiment research via Adanos Finance API — Reddit, X.com, news, Polymarket |
| [funda-data](plugins/data-providers/skills/funda-data/) | [Funda AI](https://funda.ai) API — real-time quotes, fundamentals, options flow, sentiment, SEC filings, and 60+ endpoints |
| [hormuz-strait](plugins/data-providers/skills/hormuz-strait/) | Strait of Hormuz monitoring — shipping, oil impact, insurance risk, crisis timeline |

### Startup Tools (`finance-startup-tools`)

Multi-perspective startup analysis frameworks for VC investors, job applicants, and founders.

| Skill | Description |
|---|---|
| [startup-analysis](plugins/startup-tools/skills/startup-analysis/) | Multi-perspective startup analysis — VC investor, job applicant, and CEO/founder viewpoints |

### UI Tools (`finance-ui-tools`)

Generative UI design system for rendering interactive HTML/SVG widgets in Claude conversations.

| Skill | Description |
|---|---|
| [generative-ui](plugins/ui-tools/skills/generative-ui/) | Generative UI design system for Claude's `show_widget` |

## License

MIT
