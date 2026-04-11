# Hormuz Strait Monitor — Dashboard API Schema

**Endpoint:** `GET https://hormuzstraitmonitor.com/api/dashboard`

**Authentication:** None (public API)

**Response format:** JSON

---

## Top-level response

| Field | Type | Description |
|---|---|---|
| `success` | boolean | Whether the API call succeeded |
| `data` | object | Dashboard data (see sections below) |
| `timestamp` | string (ISO datetime) | Server response timestamp |

---

## `data.straitStatus`

Current operational status of the strait.

| Field | Type | Description |
|---|---|---|
| `status` | string | Current status (e.g., "OPEN", "RESTRICTED", "CLOSED") |
| `since` | string (ISO date) | Date the current status began |
| `description` | string | Human-readable status description |

---

## `data.shipCount`

Ship transit statistics.

| Field | Type | Description |
|---|---|---|
| `currentTransits` | number | Ships currently transiting the strait |
| `last24h` | number | Total transits in the last 24 hours |
| `normalDaily` | number | Normal daily transit count (baseline) |
| `percentOfNormal` | number | Current traffic as percentage of normal |

---

## `data.oilPrice`

Brent crude oil price and recent movement.

| Field | Type | Description |
|---|---|---|
| `brentPrice` | number | Current Brent crude price (USD/barrel) |
| `change24h` | number | Absolute price change in last 24 hours |
| `changePercent24h` | number | Percentage price change in last 24 hours |
| `sparkline` | number[] | 24-hour price history (array of prices) |

---

## `data.strandedVessels`

Vessels unable to transit the strait.

| Field | Type | Description |
|---|---|---|
| `total` | number | Total stranded vessels |
| `tankers` | number | Stranded tanker vessels |
| `bulk` | number | Stranded bulk carriers |
| `other` | number | Other stranded vessels |
| `changeToday` | number | Change in stranded vessel count today |

---

## `data.insurance`

Marine insurance and war risk premium levels.

| Field | Type | Description |
|---|---|---|
| `level` | string | Risk level enum (e.g., "normal", "elevated", "high", "critical") |
| `warRiskPercent` | number | Current war risk premium as percentage |
| `normalPercent` | number | Normal (baseline) insurance rate percentage |
| `multiplier` | number | Current rate as multiplier of normal rate |

---

## `data.throughput`

Cargo throughput in deadweight tonnage (DWT).

| Field | Type | Description |
|---|---|---|
| `todayDWT` | number | Today's cargo throughput in DWT |
| `averageDWT` | number | Average daily throughput in DWT |
| `percentOfNormal` | number | Today's throughput as percentage of average |
| `last7Days` | number[] | Daily DWT values for the last 7 days |

---

## `data.diplomacy`

Current diplomatic situation affecting the strait.

| Field | Type | Description |
|---|---|---|
| `status` | string | Diplomatic status enum |
| `headline` | string | Current diplomatic headline |
| `date` | string (ISO date) | Date of the latest diplomatic development |
| `parties` | string[] | Parties involved |
| `summary` | string | Summary of the diplomatic situation |

---

## `data.globalTradeImpact`

Estimated impact on global trade if the strait is disrupted.

| Field | Type | Description |
|---|---|---|
| `percentOfWorldOilAtRisk` | number | Percentage of global oil supply at risk |
| `estimatedDailyCostBillions` | number | Estimated daily cost of disruption in billions USD |
| `affectedRegions` | object[] | List of affected regions (see below) |
| `lngImpact` | object | LNG-specific impact (see below) |
| `alternativeRoutes` | object[] | Available alternative shipping routes (see below) |
| `supplyChainImpact` | object | Broader supply chain impact (see below) |

### `affectedRegions[]`

| Field | Type | Description |
|---|---|---|
| `name` | string | Region name |
| `severity` | string | Impact severity enum |
| `oilDependencyPercent` | number | Region's dependency on strait-transiting oil |
| `description` | string | Description of impact on this region |

### `lngImpact`

| Field | Type | Description |
|---|---|---|
| `percentOfWorldLngAtRisk` | number | Percentage of global LNG at risk |
| `estimatedLngDailyCostBillions` | number | Estimated daily LNG disruption cost (billions USD) |
| `topAffectedImporters` | string[] | Countries most affected by LNG disruption |
| `description` | string | Description of LNG impact |

### `alternativeRoutes[]`

| Field | Type | Description |
|---|---|---|
| `name` | string | Route name |
| `additionalDays` | number | Extra transit days vs. Hormuz route |
| `additionalCostPerVessel` | number | Extra cost per vessel (USD) |
| `currentUsageStatus` | string | Whether this route is currently in use |

### `supplyChainImpact`

| Field | Type | Description |
|---|---|---|
| `shippingRateIncreasePercent` | number | Percentage increase in shipping rates |
| `consumerPriceImpactPercent` | number | Estimated consumer price impact |
| `sprStatusDays` | number | Strategic Petroleum Reserve coverage in days |
| `keyDisruptions` | string[] | Key supply chain disruptions |

---

## `data.crisisTimeline`

Timeline of events related to the current situation.

### `events[]`

| Field | Type | Description |
|---|---|---|
| `date` | string (ISO date) | Event date |
| `type` | string | Event type enum (e.g., "military", "diplomatic", "economic") |
| `title` | string | Event title |
| `description` | string | Event description |

---

## `data.news`

Latest news articles related to the strait.

| Field | Type | Description |
|---|---|---|
| `title` | string | Article title |
| `source` | string | News source name |
| `url` | string | Link to the article |
| `publishedAt` | string (ISO datetime) | Publication timestamp |
| `description` | string | Article summary |

---

## `data.lastUpdated`

| Field | Type | Description |
|---|---|---|
| `lastUpdated` | string (ISO datetime) | When the dashboard data was last updated |
