---
name: hormuz-strait
description: >
  Check the current status of the Strait of Hormuz — shipping transit data, oil price impact,
  stranded vessels, insurance risk levels, diplomatic developments, and global trade impact.
  Use this skill whenever the user asks about the Strait of Hormuz, Hormuz chokepoint, Persian Gulf
  shipping risk, oil transit disruption, war risk premium in the Gulf, Middle East shipping routes,
  tanker traffic through Hormuz, oil supply chain risk, or geopolitical risk affecting energy markets.
  Triggers include: "Hormuz status", "Strait of Hormuz", "is Hormuz open", "shipping through the Gulf",
  "oil chokepoint", "Persian Gulf tanker traffic", "war risk premium", "Hormuz crisis",
  "energy supply chain risk", "oil transit disruption", "Middle East shipping",
  any mention of Hormuz or Persian Gulf in context of oil, shipping, or geopolitical risk.
---

# Hormuz Strait Monitor Skill

Fetches real-time status of the Strait of Hormuz from the [Hormuz Strait Monitor](https://hormuzstraitmonitor.com) dashboard API. Covers shipping transits, oil prices, stranded vessels, insurance risk, diplomatic status, global trade impact, and crisis timeline.

**This skill is read-only.** It fetches public dashboard data — no authentication required.

---

## Step 1: Fetch Dashboard Data

Use `curl` to fetch the dashboard API:

```bash
curl -s https://hormuzstraitmonitor.com/api/dashboard
```

Parse the JSON response. The API returns `{ "success": true, "data": { ... }, "timestamp": "..." }`.

If `success` is `false` or the request fails, inform the user the monitor is temporarily unavailable and suggest checking https://hormuzstraitmonitor.com directly.

---

## Step 2: Identify What the User Needs

Match the user's request to the relevant data sections. If the user asks for a general status update, present all sections. If they ask about something specific, focus on the relevant section(s).

| User Request | Data Section | Key Fields |
|---|---|---|
| General status / "is Hormuz open?" | `straitStatus` | `status`, `since`, `description` |
| Ship traffic / transit count | `shipCount` | `currentTransits`, `last24h`, `normalDaily`, `percentOfNormal` |
| Oil price impact | `oilPrice` | `brentPrice`, `change24h`, `changePercent24h`, `sparkline` |
| Stranded / stuck vessels | `strandedVessels` | `total`, `tankers`, `bulk`, `other`, `changeToday` |
| Insurance / war risk | `insurance` | `level`, `warRiskPercent`, `normalPercent`, `multiplier` |
| Cargo throughput | `throughput` | `todayDWT`, `averageDWT`, `percentOfNormal`, `last7Days` |
| Diplomatic situation | `diplomacy` | `status`, `headline`, `parties`, `summary` |
| Global trade impact | `globalTradeImpact` | `percentOfWorldOilAtRisk`, `estimatedDailyCostBillions`, `affectedRegions`, `lngImpact`, `alternativeRoutes`, `supplyChainImpact` |
| Crisis timeline / events | `crisisTimeline` | `events[]` with `date`, `type`, `title`, `description` |
| Latest news | `news` | `title`, `source`, `url`, `publishedAt`, `description` |

---

## Step 3: Present the Data

Format the results clearly for financial research. Adapt the presentation based on what the user asked for.

### General status briefing (default)

When the user asks for a general update, present a concise briefing covering all key sections:

1. **Strait Status** — lead with the current status (e.g., "OPEN", "RESTRICTED", "CLOSED"), how long it's been in that state, and the description
2. **Ship Traffic** — current transits, last 24h count, and percent of normal
3. **Oil Price** — Brent price with 24h change
4. **Stranded Vessels** — total count broken down by type, with today's change
5. **Insurance Risk** — risk level, war risk premium percentage, and multiplier vs. normal
6. **Cargo Throughput** — today's DWT vs. average, percent of normal
7. **Diplomatic Status** — current status, headline, and brief summary
8. **Global Trade Impact** — percent of world oil at risk, estimated daily cost, and top affected regions

### Formatting guidelines

- Use tables for structured data (vessel counts, affected regions, alternative routes)
- Highlight abnormal values — if `percentOfNormal` is below 80% or above 120%, call it out
- For `oilPrice.sparkline`, describe the trend (rising, falling, stable) rather than listing raw numbers
- For `throughput.last7Days`, describe the trend direction
- Show `lastUpdated` timestamp so the user knows data freshness
- For news items, include the source and link
- For crisis timeline events, present chronologically with event type labels

### Risk assessment

Based on the data, provide a brief risk assessment:

| Insurance Level | Interpretation |
|---|---|
| `normal` | No elevated risk — shipping operating normally |
| `elevated` | Some disruption concerns — monitor closely |
| `high` | Significant risk — active disruption or credible threat |
| `critical` | Severe disruption — major impact on global oil supply |

If the strait status is anything other than fully open, highlight:
- The estimated daily cost to global trade
- Which regions are most affected and their oil dependency
- Available alternative routes with additional transit days and cost
- LNG impact if applicable
- SPR (Strategic Petroleum Reserve) status in days

---

## Step 4: Respond to the User

- Lead with the most important information: strait status and any active disruption
- Include data freshness (`lastUpdated` timestamp)
- If the situation is elevated or worse, proactively include the global trade impact summary
- Keep the response concise for routine "all clear" statuses; expand for active incidents
- Add a disclaimer: data is sourced from Hormuz Strait Monitor and may have delays

---

## Reference Files

- `references/api_schema.md` — Complete API response schema with field descriptions and data types

Read the reference file when you need exact field names or data type details.
