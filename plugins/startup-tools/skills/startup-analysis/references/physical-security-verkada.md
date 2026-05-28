# Verkada / Cloud Physical Security Research Notes

Use these notes when analyzing Verkada or adjacent cloud physical-security companies (cameras, access control, alarms, sensors, visitor/workplace tools). Treat company-provided figures as claims to verify against independent reporting where possible.

## Verkada public traction signals found in May 2026 session

Primary/company sources:
- Verkada announced a CapitalG-led investment valuing the company at **$5.8B** and said it had surpassed **$1B in annualized bookings** (Verkada blog, Dec. 3 2025; CNBC also reported the round and valuation).
- Verkada said **2M+ devices** were deployed across **171 countries** and **30,000+ organizations** used the platform (Verkada blog, Dec. 2025).
- Verkada's Feb. 2025 Series E announcement: **$200M Series E**, **$4.5B valuation**, **$700M+ total funding**, customer base grew **111%** since Sept. 2022 Series D, revenue grew **95%** over the same period, **90+ Fortune 500** customers, and **70%+ of large customers use 2+ Verkada products**.
- Verkada careers page said the company had **almost 2,200 employees globally**.
- Verkada claims Omdia ranked it #1 worldwide in Video Surveillance as a Service (VSaaS) and #1 in cloud-native access control; quote as company-cited Omdia claims unless independently verified.

Independent/third-party notes:
- CNBC reported the Dec. 2025 CapitalG-led round, $5.8B valuation, and $1B+ annualized bookings.
- FTC announced in Aug. 2024 that Verkada would implement a comprehensive information security program and pay a **$2.95M CAN-SPAM penalty**. FTC/DOJ complaint alleged inappropriate security practices, a 2021 breach, misleading compliance claims, undisclosed employee/investor reviews, and CAN-SPAM violations.
- Verkada's own FTC settlement explainer states attackers gained access to footage for **97 of then-6,000 customers** and that there was no fine related to the security incident, while the $2.95M payment resolved email marketing claims. Present both the regulator's allegations and Verkada's framing.
- Contrary Research (Feb. 2024) notes founders Filip Kaliszan, Benjamin Bercovitz, James Ren, and Hans Robertson; Robertson previously co-founded Meraki, acquired by Cisco for $1.2B. This is relevant founder-market fit for cloud-managed hardware/software.

## Quick derived ratios

When current figures remain valid:
- $5.8B valuation / $1B annualized bookings ≈ **5.8x bookings**.
- $1B bookings / 30,000 customers ≈ **$33K annualized bookings/customer**.
- 2M devices / 30,000 customers ≈ **67 devices/customer**.
- $4.5B to $5.8B valuation increase ≈ **29%**.
- 1.5M to 2M devices ≈ **33% device growth**.

## Analysis framing for this category

Bull case:
- Legacy physical security is fragmented and under-clouded.
- Unified cloud platform across cameras/access/alarms/sensors creates switching costs and land-and-expand.
- AI makes passive video more operationally valuable: search, anomaly detection, deterrence, incident response.
- Hardware deployment creates account stickiness when software attach and multi-product adoption are high.

Bear/risk case:
- Security/privacy trust failures are central, not incidental, because the company sells security and handles sensitive footage.
- Bookings are not revenue or gross profit; ask for ARR, recognized revenue, gross margin by hardware vs software, NDR, churn, CAC payback, burn multiple.
- Hardware adds supply-chain, support, installation, inventory, and margin complexity.
- Surveillance, facial authentication, schools/hospitals/law enforcement, and workplace monitoring create regulatory/reputational exposure.
- Aggressive go-to-market should be checked against culture and compliance maturity.

## Interview/diligence prompts

For job candidates:
1. What changed technically and organizationally after the 2021 breach and FTC settlement?
2. What are current SOC 2 / ISO / FedRAMP / security audit commitments, and who owns them?
3. Is equity options or RSUs? What is the 409A, strike price, preferred price, exercise window, tender/liquidity history, and expected IPO timing?
4. What is team-level attrition and work-hour/on-call expectation?
5. How much of growth comes from expansion vs new logos?

For investors:
1. Reconcile annualized bookings, ARR, GAAP revenue, deferred revenue, and backlog.
2. Segment gross margin into hardware, subscriptions, storage, support, and professional services.
3. Calculate attach rate and NDR by product count and customer cohort.
4. Inspect security roadmap, audit results, incident response history, and privacy/legal exposure.
5. Validate channel vs direct sales efficiency and CAC payback by segment.