# Finance Skills

> [!WARNING]
> This project is for educational and informational purposes only. Nothing here constitutes financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.

A collection of agent skills for financial analysis and trading, following the [Agent Skills](https://agentskills.io) open standard.

**Visit [skills.himself65.com](https://skills.himself65.com/) for documentation, demos, and setup instructions.**

---

<div align="center">

</a>



</div>

---

## Quick Start

### Plugin Groups (Claude Code, Codex, Cursor, and More)

```bash
npx plugins add himself65/finance-skills
```

The installer prompts you to select one or more plugin groups. To install every group non-interactively:

```bash
npx plugins add himself65/finance-skills --yes
```

### Individual Skills

```bash
npx skills add himself65/finance-skills --skill yfinance-data
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
| [company-valuation](plugins/market-analysis/skills/company-valuation/) | DCF + relative + SOTP triangulation — implied share price, WACC × g sensitivity, Bull/Base/Bear scenarios |
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

Read-only social media and research feeds — Twitter/X, Discord, LinkedIn, Telegram, Y Combinator, and a generic opencli fallback for 100+ other sources.

| Skill | Description |
|---|---|
| [discord-reader](plugins/social-readers/skills/discord-reader/) | Read-only Discord research via [opencli](https://github.com/jackwener/opencli) |
| [linkedin-reader](plugins/social-readers/skills/linkedin-reader/) | Read-only LinkedIn feed & job search via [opencli](https://github.com/jackwener/opencli) |
| [opencli-reader](plugins/social-readers/skills/opencli-reader/) | Generic read-only fallback for 100+ [opencli](https://github.com/jackwener/opencli) adapters — Yahoo Finance, Bloomberg, Reuters, Eastmoney, Xueqiu, Reddit, HackerNews, Substack, arXiv, and more |
| [telegram-reader](plugins/social-readers/skills/telegram-reader/) | Read-only Telegram channel reader via [tdl](https://github.com/iyear/tdl) |
| [twitter-reader](plugins/social-readers/skills/twitter-reader/) | Read-only Twitter/X research via [opencli](https://github.com/jackwener/opencli) |
| [yc-reader](plugins/social-readers/skills/yc-reader/) | Y Combinator company data via [yc-oss/api](https://github.com/yc-oss/api) |

### Data Providers (`finance-data-providers`)


| Skill | Description |
|---|---|
| [finance-sentiment](plugins/data-providers/skills/finance-sentiment/) | Stock sentiment research via Adanos Finance API — Reddit, X.com, news, Polymarket |
| [fintel-data](plugins/data-providers/skills/fintel-data/) | [Fintel](https://fintel.io) — short interest, borrow rates, short volume, fails-to-deliver, 13F institutional ownership, insider transactions, analyst targets, calendars — via REST API or official MCP server |
| [hormuz-strait](plugins/data-providers/skills/hormuz-strait/) | Strait of Hormuz monitoring — shipping, oil impact, insurance risk, crisis timeline |
| [tradingview-mcp](plugins/data-providers/skills/tradingview-mcp/) | Headless TradingView data via a bundled [tradingview-mcp](https://github.com/atilaahmettaner/tradingview-mcp) server — TA readouts, multi-timeframe alignment, exchange scans, futures overview/movers, extended hours, options chain (no greeks), backtests. No app, no login |
| [tradingview-reader](plugins/data-providers/skills/tradingview-reader/) | Read-only TradingView desktop reader — quotes, full options chains with greeks/IV, expiries, watchlists, alerts, chart state, screenshots — via [opencli](https://github.com/jackwener/opencli) + CDP |
| [hyperliquid-reader](plugins/data-providers/skills/hyperliquid-reader/) | Read-only [Hyperliquid](https://app.hyperliquid.xyz) market-data reader — perp/spot markets, mids, funding (incl. cross-venue arb screen), order book, and candles — via [opencli](https://github.com/jackwener/opencli) + public info API |

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

### Skill Creator (`finance-skill-creator`)

Create, evaluate, and iterate on high-quality agent skills with structured guidance, quality scoring, and best-practice enforcement.

| Skill | Description |
|---|---|
| [skill-creator](plugins/skill-creator/skills/skill-creator/) | Create new skills, evaluate existing ones against a 10-dimension rubric, and improve skill quality |

## License

MIT
