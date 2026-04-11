# options-payoff

Generate interactive options payoff curve charts with dynamic parameter controls.

## What it does

This skill renders a fully interactive HTML widget showing:

- **Expiry payoff curve** (dashed gray line) — intrinsic value at expiration
- **Theoretical value curve** (solid colored line) — Black-Scholes price at current DTE/IV
- Dynamic sliders for all key parameters (strikes, premium, IV, DTE, spot price)
- Real-time stats: max profit, max loss, breakevens, current P&L at spot

## Supported strategies

| Strategy | Legs |
|---|---|
| Butterfly | Buy K1, Sell 2×K2, Buy K3 |
| Vertical spread | Buy K1, Sell K2 (same expiry) |
| Calendar spread | Buy far-expiry K, Sell near-expiry K |
| Iron condor | Sell K2/K3, Buy K1/K4 wings |
| Straddle | Buy Call K + Buy Put K |
| Strangle | Buy OTM Call + Buy OTM Put |
| Covered call | Long 100 shares + Sell Call K |
| Naked put | Sell Put K |
| Ratio spread | Buy 1×K1, Sell N×K2 |

For unlisted strategies, the skill uses `custom` mode — decomposing into individual legs and summing their P&Ls.

## Triggers

- Describing an options strategy (e.g., "show me a bull call spread")
- Uploading a screenshot from a broker (IBKR, TastyTrade, Robinhood, etc.)
- Mentioning strike prices, premiums, or expiry dates
- Asking to "show me the payoff", "draw the P&L curve", or "what does this trade look like"

## Platform

Works on **Claude.ai** (via the built-in `show_widget` tool) or with the [generative-ui](../../../ui-tools/skills/generative-ui/) skill on Claude Code.

## Setup

```bash
# As a plugin (recommended — installs all skills)
npx plugins add himself65/finance-skills --plugin finance-market-analysis

# Or install just this skill
npx skills add himself65/finance-skills --skill options-payoff
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/strategies.md` — Detailed payoff formulas and edge cases for each strategy type
- `references/bs_code.md` — Copy-paste ready Black-Scholes JS implementation with normCDF
