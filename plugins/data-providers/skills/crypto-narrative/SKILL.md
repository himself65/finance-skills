---
name: crypto-narrative
description: >
  Crypto / AI / macro narrative intelligence via the signaldaemon API —
  cross-source narrative convergence (how many independent, trust-weighted
  sources agree on a story now) and capital divergence (narrative vs. price, as
  two signed axes: absolute direction and relative-to-market). Use when the user
  asks what the crypto narrative is right now, which crypto/AI/macro stories are
  gaining traction, whether a narrative is matched by capital or just hype, what
  is converging across sources, the market regime, or for a clean de-noised
  crypto news feed before trading or research. Triggers: "what's the crypto
  narrative today", "is the ETH narrative matched by price", "which crypto
  stories are converging", "narrative vs price on BTC", "crypto market regime",
  "is this narrative funded or just hype", "clean crypto news on restaking", "AI
  agents crypto narrative". READ-ONLY: fetches narrative context only, no trades.
---

# Crypto Narrative

Read-only crypto/AI/macro **narrative intelligence** via the signaldaemon API: it
returns which stories are *converging* across independent sources and whether
capital is confirming them. It is the narrative layer a price feed or a per-asset
sentiment score can't compute. Not price data, not order execution; news-derived,
roughly 20-minute cadence.

## Step 1: Get a key

A free demo key needs no signup:

```bash
SIGNALDAEMON_API_KEY=$(curl -s -X POST https://api.signaldaemon.com/v1/request-key | python3 -c "import sys,json;print(json.load(sys.stdin)['key'])")
```

Demo keys allow 200 narrative calls/day and 5 feed calls/day. A free account key
(500/day, no expiry) is available at https://signaldaemon.com/console. Pass the key
as the `x-api-key` header.

## Step 2: Pull the day's narratives

```bash
curl -s https://api.signaldaemon.com/v1/narratives \
  -H "x-api-key: $SIGNALDAEMON_API_KEY" -H "content-type: application/json" -d '{"limit":8}'
```

Returns ranked narratives plus a top-level `market_snapshot`.

## Step 3: Frame with the regime first

Read `market_snapshot.market_regime` (crash / range / bull) and `market_7d`. Every
divergence reading below is relative to this regime.

## Step 4: Read each narrative

For each: `name` + `gist`; `strength` (cross-source convergence — independent
trust-weighted sources agreeing now; higher = more corroborated, harder to fake than
one loud headline); `momentum.members_24h` (is it accelerating); and `divergence`.

## Step 5: Read divergence as two independent signed axes

Never infer one axis from the other:

- `direction` is up or down — the asset's absolute 7-day move.
- `vs_market` is outperform or underperform — the move relative to `market_7d`.
- `narrative_no_flow` = strong story, capital not following (loud but unfunded).
- `narrative_price_aligned` = story matched by capital.
- `no_asset` = no single tradeable asset; report the story, do not invent a ticker.

In a crash an asset can be `direction=down` AND `vs_market=outperform` — it fell
slower than the market (relative strength), not a bullish price move. Report both.

## Step 6: Clean feed for a topic (optional)

```bash
curl -s https://api.signaldaemon.com/v1/feed \
  -H "x-api-key: $SIGNALDAEMON_API_KEY" -H "content-type: application/json" \
  -d '{"query":"restaking","limit":8}'
```

If `coverage` is `thin`, say so. Treat divergence as **context and risk-framing, not
a proven trading edge or the sole reason to trade** — let your own strategy decide.

## Notes

- READ-ONLY. No trades, no mutations.
- Crypto/AI/macro and narrative/sector-level — for single-name equity sentiment, pair
  with a stock-sentiment skill instead.
- Fails safe: `no_asset` and `coverage: "thin"` are stated, never papered over.
- MCP alternative: the same data is available over remote MCP at
  `https://api.signaldaemon.com/mcp` (header `x-api-key`), tools `get_market_narratives`
  and `get_clean_feed`.

## Reference files

- `references/api_reference.md` — endpoints, field meanings, and the divergence schema.
