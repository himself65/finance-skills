# crypto-narrative

Crypto / AI / macro **narrative intelligence** via the signaldaemon API.

## What it does

Returns derived signals a price feed or per-asset sentiment score can't compute:

- **Cross-source convergence** (`strength`) — how many independent, trust-weighted
  sources are converging on the same story right now (a narrative, not one headline)
- **Capital divergence** — narrative vs. price as two signed axes: `direction`
  (absolute move) and `vs_market` (relative to the market baseline)
- **Momentum** — is the narrative accelerating (`members_24h`)
- **Clean feed** — de-noised, source-attributed crypto/AI/macro news for a topic

Useful when a user wants:

- "What's the crypto narrative right now?"
- "Is the ETH narrative matched by price, or just hype?"
- "Which crypto/AI/macro stories are converging across sources?"
- "What's the market regime?"
- "Clean crypto news on restaking before I act"

**This skill is read-only.** It fetches narrative context only and places no trades.
Treat divergence as context/risk-framing, not a proven trading edge.

## Triggers

- "what's the crypto narrative today"
- "is the BTC/ETH narrative matched by price"
- "which crypto stories are converging"
- "narrative vs price"
- "crypto market regime"
- "is this narrative funded or just hype"
- "clean crypto news on {topic}"
- "AI agents crypto narrative"

## Prerequisites

- `SIGNALDAEMON_API_KEY` in the environment (free demo: `curl -X POST https://api.signaldaemon.com/v1/request-key`, no signup)
- `curl` available in the shell

## Platform

**Claude Code** — requires outbound HTTP / shell. (Also usable over remote MCP:
`https://api.signaldaemon.com/mcp`, header `x-api-key`.)

## Setup

```bash
# As a plugin (recommended — installs all data-provider skills)
npx plugins add himself65/finance-skills --plugin finance-data-providers

# Or install just this skill
npx skills add himself65/finance-skills --skill crypto-narrative
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/api_reference.md` — endpoints, field meanings, and the divergence schema

---

Data source: [signaldaemon](https://signaldaemon.com) (crypto/AI/macro narrative &
signal intelligence). The skill is framed around the user problem; signaldaemon is the
underlying API. No secrets in this skill — the key lives in your environment.
