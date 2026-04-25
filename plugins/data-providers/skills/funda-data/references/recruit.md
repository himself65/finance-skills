# AI Company Recruit Signals Reference

Hiring-based alpha signals covering the major AI companies: **OpenAI**, **Anthropic**, **Google**, **xAI**, **SurgeAI**, **Mercor**.

Pipeline:

```
raw JDs  ─►  classifications ─►  product clusters ─►  launch probabilities ─►  stock impacts
                                                                        ╲
                                                                         ►  GTM products
news/emails ────────────────────────────────────────────►  enterprise events (with event-study alpha)
```

All list endpoints return paginated envelopes (`items`, `page`, `page_size`, `next_page`, `total_count`). Iterate with `page_size=500–1000` until `next_page=-1`.

---

## GET /v1/recruit-job-postings

Raw job postings scraped from company career pages. Both open (`is_active=true`) and historical closed postings are included; each item carries the full `description`.

### Key parameters

| Param | Values |
|---|---|
| `company` | `openai` \| `anthropic` \| `google` \| `xai` \| `surgeai` \| `mercor` |
| `department` | case-insensitive partial match |
| `location_type` | `remote` \| `onsite` \| `hybrid` |
| `employment_type` | `full_time` \| `part_time` \| `contract` \| `internship` |
| `experience_level` | `entry` \| `mid` \| `senior` \| `staff` \| `principal` \| `executive` |
| `is_active` | bool |
| `skill` | string (searches skills array) |
| `search` | title search (case-insensitive) |
| `posted_after` / `posted_before` | ISO 8601 datetimes |
| `order` | default `-posted_at` |
| `page` / `page_size` | max 1000 |

### GET /v1/recruit-job-postings/{job_posting_id}

Single posting by UUID. Detail adds `requirements`, `extra`, `updated_at`.

Notes: `salary_period` is `annual` for OpenAI/Anthropic/Google/xAI, `hourly` for Mercor contracts. Google live jobs have `posted_at=null`. Jobs with no description are excluded.

---

## GET /v1/recruit-jd-classifications

Claude-inferred metadata per JD (vertical, intent, function, seniority), linked to a job posting via `recruit_job_id`.

### Key parameters

| Param | Values |
|---|---|
| `company` | AI company slug |
| `vertical` | `Coding` \| `Finance` \| `Healthcare` \| `Legal` \| `Security` \| ... |
| `jd_intent` | `product_build` \| `capability_rd` \| `internal_ops` |
| `jd_function` | `engineering` \| `research` \| `product` \| `sales` \| `ops` \| `other` |
| `seniority` | `junior` \| `mid` \| `senior` \| `lead` \| `exec` |
| `posted_after` / `posted_before` | date |
| `search` | title search |

List items exclude `description`. `GET /v1/recruit-jd-classifications/{job_id}` returns the full record including `description` and `scraped_date`.

---

## GET /v1/recruit-product-signal-clusters

Product-level hiring signals grouped by `(company, vertical)` with urgency scoring and competing-company threat map.

### Key parameters

| Param | Values |
|---|---|
| `company` | AI company slug |
| `product_stage` | `research` \| `building` \| `launching` \| `selling` \| `mature` |
| `urgency` | `high` \| `medium` \| `low` |
| `generated_after` / `generated_before` | date |

List items include `competing_public_companies` but exclude `product_description`, `hiring_signal`, `func_dist`, `vert_dist`, `enterprise_verticals`, `evidence_quotes`. Detail (`/{cluster_id}`) returns all fields.

`competing_public_companies` entries: `{ticker, name, threat_level, reason, hop}` where `hop=1` is Claude-identified and `hop=2` is discovered via supply chain KG expansion.

---

## GET /v1/recruit-gtm-products

Claude-extracted product names from Sales/GTM JDs, grouped by `(company, vertical)`. Unique on `(company, vertical)`.

### Key parameters

| Param | Values |
|---|---|
| `company` | AI company slug |
| `vertical` | vertical name |
| `order` | default `-generated_at` |

Response fields: `product_names` (array), `jd_count`, `evidence_sample`, `generated_at`.

---

## GET /v1/recruit-launch-probabilities

Product launch probability matrix per `(company, vertical)` from JD time-series analysis, phase detection, and spike alerts.

### Key parameters

| Param | Values |
|---|---|
| `company` | AI company slug |
| `vertical` | vertical name |
| `phase` | `research` \| `build` \| `gtm` |
| `status` | `LAUNCHED` \| `PREDICTING` \| `RESEARCH` |
| `min_probability` | 0.0–1.0 |
| `order` | default `-launch_probability` |

List items exclude `monthly_jd_series`, `spike_alerts`, formula components (`jd_signal`, `spike_boost`, `phase_boost`). Detail (`/{item_id}`) returns the full record.

`status`: `LAUNCHED` = probability=1.0 (already in market), `PREDICTING` = active signal, `RESEARCH` = early stage.

---

## GET /v1/recruit-stock-impacts

Ticker-level impact scores — which public software stocks are most threatened by AI-company hiring signals. Unique on `(ticker, report_date)` (supports historical snapshots).

### Key parameters

| Param | Values |
|---|---|
| `ticker` | auto-uppercased |
| `urgency` | `HIGH` \| `MEDIUM` \| `LOW` |
| `report_date` | date (YYYY-MM-DD) |
| `min_adj_score` | float (0.0+) |
| `order` | default `-adj_score` |

List items exclude `related_products` and `vertical_breakdown`. Detail (`/{item_id}`) returns the full record.

Score definitions:
- `impact_score` = base sector exposure × vertical match weight
- `adj_score` = `impact_score` × boosted launch probability (primary ranking metric)
- `urgency = HIGH` when `adj_score >= 0.7` and launch probability is elevated
- `biz_pct` = estimated % revenue exposed to the threatened vertical (0–100)

---

## GET /v1/recruit-enterprise-events

AI-company events (new models, pricing changes, partnerships, acquisitions, feature launches) extracted from news and expert emails, with Claude-assessed magnitude and event-study alpha vs QQQ (T+1 to T+10).

### Key parameters

| Param | Values |
|---|---|
| `company` | AI company slug |
| `event_type` | `new_model` \| `pricing_change` \| `partnership` \| `acquisition` \| `feature_launch` \| `other` |
| `source` | `news_api` \| `expert_email` |
| `is_significant` | bool — p < 0.05 |
| `date_after` / `date_before` | date |
| `order` | default `-event_date` |

List items exclude `description` and `alpha_detail`. Detail (`/{item_id}`) returns the full record.

Fields:
- `magnitude`: 0.0–1.0 (Claude-assessed)
- `sentiment`: `positive` \| `negative` \| `neutral`
- `alpha_t1_t10`: cumulative abnormal return T+1→T+10 vs QQQ
- `alpha_tstat`: t-statistic; `is_significant` when p < 0.05
- `alpha_detail`: per-ticker breakdown `[{ticker, alpha, tstat}, ...]`

---

## Typical workflows

- **"What's OpenAI building in Healthcare?"** → `recruit-launch-probabilities?company=openai&vertical=Healthcare` + `recruit-product-signal-clusters?company=openai&vertical=Healthcare`
- **"Which public stocks are most threatened by AI hiring?"** → `recruit-stock-impacts?urgency=HIGH&order=-adj_score`
- **"Show significant AI-company events with market impact"** → `recruit-enterprise-events?is_significant=true&order=-event_date`
- **"What products is Anthropic selling?"** → `recruit-gtm-products?company=anthropic`
