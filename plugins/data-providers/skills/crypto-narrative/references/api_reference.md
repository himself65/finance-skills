# Crypto Narrative API Reference

This skill uses the signaldaemon API for read-only crypto/AI/macro narrative &
signal intelligence.

Human docs: https://signaldaemon.com/api · Agent-readable: https://signaldaemon.com/api.md
How to read the signals: https://signaldaemon.com/signals

## Authentication

Send the API key as:

```bash
-H "x-api-key: $SIGNALDAEMON_API_KEY"
```

Get a free demo key (no signup): `POST https://api.signaldaemon.com/v1/request-key`.

## Endpoints

### Ranked narratives + market snapshot

```text
POST https://api.signaldaemon.com/v1/narratives
body: {"limit": 8}    (max 12)
```

Each narrative:
- `name`, `gist`, `category`, `rank`
- `strength` — cross-source convergence score (trust-weighted independent-source agreement)
- `momentum.members_24h` — new corroborating sources in last 24h (acceleration)
- `divergence` — see schema below
- `sources`, `representative_items` (cited articles)

Top-level `market_snapshot`: `market_regime` (crash/range/bull), `market_7d`,
`fear_greed`, `btc`/`eth`/`sol`. Read every divergence relative to `market_regime`.

### Clean feed for a topic

```text
POST https://api.signaldaemon.com/v1/feed
body: {"query": "restaking", "category": null, "limit": 8}
```

Returns a de-noised, source-attributed feed. `coverage: "thin"` means partial — say so.

### Pre-trade gate (vet a candidate trade)

```text
POST https://api.signaldaemon.com/v1/vet
body: {"symbol": "ETH", "side": "long", "horizon": null, "source": null}
```

Returns `{verdict, confidence, narrative, reason, evidence}` where `verdict` ∈
`support` · `caution` · `contradict` · `no_signal`. Read-only; vets the narrative
dimension only (not a buy/sell call) and abstains (`no_signal`) when there is no
single-asset narrative coverage for `symbol`.

### Quota self-check (free, no increment)

```text
GET https://api.signaldaemon.com/v1/quota
```

## Divergence schema (two signed axes — never infer one from the other)

```json
{
  "code": "narrative_price_aligned",
  "direction": "down",          // absolute 7d move: up | down
  "vs_market": "outperform",    // relative to market_7d: outperform | underperform
  "asset": "ETH",
  "price_change_7d": -12.65,
  "rel_flow": 4.1
}
```

- `code` ∈ `narrative_price_aligned` · `narrative_no_flow` · `neutral` · `no_asset`
- In a crash an asset can be `direction=down` AND `vs_market=outperform` (fell slower
  than the market = relative strength, NOT a bullish move). Report both axes.
- `no_asset` = no single tradeable asset; report the story, do not invent a ticker.
- Treat divergence as context, not a proven trading edge.

## MCP (alternative to REST)

Remote MCP, Streamable HTTP: `https://api.signaldaemon.com/mcp`, header `x-api-key`.
Tools (read-only): `get_market_narratives(limit)`, `get_clean_feed(query, category, limit)`,
`vet_trade(symbol, side)`.

## Errors

- `401` missing/invalid key → mint one at `/v1/request-key`
- `429` quota or rate limit → check `/v1/quota`
- Raw `urllib` clients: set a `User-Agent` (default bot UAs are firewalled by the CDN).
