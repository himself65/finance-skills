# Supply Chain Knowledge Graph Reference

Knowledge graph with stocks, edges (relationships), and graph traversal endpoints.

- **Layers**: T0 (raw materials) to T8 (vertical applications)
- **Universe**: `semi` (semiconductor), `software`, `foundation_model`
- **Edge types**: `CUSTOMER_OF`, `SUPPLIER_TO`, `COMPETES_WITH`, `PARTNER_OF`
- **Confidence**: 0.0–1.0 (higher = more reliable)

---

## GET /v1/supply-chain/stocks

List stocks in the supply chain KG.

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | Page index (0-based) |
| `page_size` | int | 20 | Items per page (max: 500) |
| `ticker` | str | - | Filter by ticker |
| `layer` | str | - | Filter by layer (T0-T8) |
| `universe` | str | - | Filter by universe (semi/software/foundation_model) |
| `is_bottleneck` | bool | - | Filter bottleneck stocks |
| `country` | str | - | Filter by country |

Response fields: `ticker`, `name`, `layer`, `universe`, `is_bottleneck`, `country`.

---

## GET /v1/supply-chain/stocks/{ticker}

Detailed info for a single stock.

Response fields: `ticker`, `name`, `layer`, `exchange`, `country`, `notes`, `is_bottleneck`, `market_cap_usd`, `universe`, `sub_category`, `macro_market`, `extra_metadata`.

---

## GET /v1/supply-chain/stocks/bottlenecks

All bottleneck stocks (critical chokepoints with monopolistic positions).

### Parameters

| Param | Type | Description |
|---|---|---|
| `layer` | str | Filter by layer |
| `universe` | str | Filter by universe |

---

## GET /v1/supply-chain/kg-edges

List knowledge graph edges (relationships between stocks).

### Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int | 0 | Page index |
| `page_size` | int | 20 | Items per page (max: 500) |
| `source_ticker` | str | - | Filter by source ticker |
| `target_ticker` | str | - | Filter by target ticker |
| `edge_type` | str | - | Filter by type (CUSTOMER_OF, SUPPLIER_TO, COMPETES_WITH, PARTNER_OF) |
| `confidence_min` | float | - | Minimum confidence (0-1) |
| `confidence_max` | float | - | Maximum confidence (0-1) |
| `is_active` | bool | - | Filter active edges |
| `universe` | str | - | Filter by universe |

Edge semantics:
- `CUSTOMER_OF`: source buys from target
- `SUPPLIER_TO`: source supplies to target

Detailed edge response includes: `id`, `source_ticker`, `target_ticker`, `edge_type`, `label`, `confidence`, `source_doc`, `universe`, `is_active`, `attributes`.

---

## Graph Traversal Endpoints

All return nodes with: `ticker`, `name`, `layer`, `edge_type`, `label`, `confidence`, `distance`.

### GET /v1/supply-chain/kg-edges/graph/suppliers/{ticker}

Upstream suppliers (recursive traversal).

| Param | Type | Default | Description |
|---|---|---|---|
| `depth` | int | 1 | Traversal depth (1-5) |
| `min_confidence` | float | 0.5 | Min confidence (0-1) |

### GET /v1/supply-chain/kg-edges/graph/customers/{ticker}

Downstream customers (recursive).

| Param | Type | Default | Description |
|---|---|---|---|
| `depth` | int | 1 | Traversal depth (1-5) |
| `min_confidence` | float | 0.5 | Min confidence (0-1) |

### GET /v1/supply-chain/kg-edges/graph/competitors/{ticker}

Competitors.

| Param | Type | Default | Description |
|---|---|---|---|
| `min_confidence` | float | 0.5 | Min confidence |
| `layer` | str | - | Filter by layer |

### GET /v1/supply-chain/kg-edges/graph/partners/{ticker}

Partners.

| Param | Type | Default | Description |
|---|---|---|---|
| `min_confidence` | float | 0.5 | Min confidence |

### GET /v1/supply-chain/kg-edges/graph/neighbors/{ticker}

All direct neighbors (1-hop), grouped by relationship type.

| Param | Type | Default | Description |
|---|---|---|---|
| `min_confidence` | float | 0.5 | Min confidence |

### Examples

```bash
# NVDA suppliers (2-level deep)
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/supply-chain/kg-edges/graph/suppliers/NVDA?depth=2"

# NVDA customers
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/supply-chain/kg-edges/graph/customers/NVDA?depth=2"

# NVDA competitors
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/supply-chain/kg-edges/graph/competitors/NVDA"

# All NVDA neighbors
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/supply-chain/kg-edges/graph/neighbors/NVDA"

# Bottleneck stocks in semiconductors
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/supply-chain/stocks/bottlenecks?universe=semi"

# Relationship edges with high confidence
curl -s -H "Authorization: Bearer $FUNDA_API_KEY" \
  "https://api.funda.ai/v1/supply-chain/kg-edges?source_ticker=NVDA&confidence_min=0.8"
```
