# ETF Premium/Discount Reference

## Core Formula

```
Premium/Discount (%) = (Market Price - NAV) / NAV × 100
```

Where:
- **Market Price** = the price at which the ETF is currently trading on the exchange
- **NAV** (Net Asset Value) = the per-share value of the ETF's underlying holdings, calculated by the fund at end of day

A **positive** value means the ETF trades at a **premium** (more expensive than underlying assets).
A **negative** value means the ETF trades at a **discount** (cheaper than underlying assets).

---

## How ETF Premiums and Discounts Work

### The Creation/Redemption Mechanism

ETFs maintain price alignment with NAV through authorized participants (APs) — large institutional players (banks, broker-dealers) who can:

1. **Create shares**: Buy the underlying basket of securities, deliver them to the ETF issuer, and receive new ETF shares. This increases supply and pushes the price down toward NAV.
2. **Redeem shares**: Return ETF shares to the issuer and receive the underlying basket. This reduces supply and pushes the price up toward NAV.

This arbitrage mechanism keeps most liquid ETFs within a few basis points of NAV. When it breaks down — due to illiquidity, market stress, or structural constraints — premiums and discounts appear.

### Why the Mechanism Can Fail

| Cause | Effect | ETF Types Affected |
|---|---|---|
| Underlying market closed | Price reflects expectations, NAV is stale | International (EEM, VWO, KWEB) |
| Underlying assets illiquid | APs can't efficiently create/redeem | Bond (HYG, JNK, EMB), Small-cap |
| Market stress / volatility | APs widen spreads or step back | All types, especially credit |
| Regulatory constraints | Creation units restricted | Crypto (IBIT, BITO) early days |
| Futures contango/backwardation | NAV drag from roll costs | Commodity (USO, UNG) |
| Daily leverage reset | Compounding creates tracking error | Leveraged (TQQQ, SQQQ) |
| Retail demand surge | Buying pressure exceeds AP capacity | Thematic (ARKK), new launches |

---

## Data Source: yfinance

### Key Fields

| Field | Description | Notes |
|---|---|---|
| `navPrice` | Most recent official NAV per share | Updated daily at market close |
| `regularMarketPrice` | Current/last trading price | May be delayed 15 min |
| `previousClose` | Prior day closing price | Use as fallback for price |
| `totalAssets` | Total fund AUM in dollars | Not per-share |
| `netExpenseRatio` | Annual expense ratio (decimal) | e.g., 0.03 = 0.03% |
| `category` | Morningstar category | e.g., "Intermediate Core Bond" |
| `fundFamily` | ETF issuer | e.g., "iShares", "Vanguard" |
| `quoteType` | Security type | Must be "ETF" |
| `bid` / `ask` | Current bid and ask prices | For spread calculation |
| `averageVolume` | Average daily volume | Liquidity indicator |
| `yield` | Distribution yield (decimal) | e.g., 0.039 = 3.9% |

### Limitations

- **No historical NAV**: yfinance only provides the most recent `navPrice`. You cannot build a time series of premiums/discounts from yfinance alone.
- **NAV timing**: The `navPrice` reflects end-of-day calculation. During trading hours, the market price moves but NAV is static until the next calculation.
- **Not all tickers**: Some very new or obscure ETFs may not have `navPrice` populated.
- **Delay**: Market prices may be delayed 15 minutes for some exchanges.

---

## Category-Specific Benchmarks

### What's "Normal" Premium/Discount by Category

| Category | Typical Range | Explanation |
|---|---|---|
| US Large-Cap Equity (SPY, QQQ, VOO) | ±0.01% to ±0.05% | Extremely liquid, tight arbitrage |
| US Mid/Small-Cap (IWM, IJR) | ±0.02% to ±0.10% | Slightly wider due to smaller underlying stocks |
| US Bond - Investment Grade (AGG, BND, LQD) | ±0.05% to ±0.30% | Bond market less liquid than equities |
| US Bond - High Yield (HYG, JNK) | ±0.10% to ±0.50% | Corporate bonds can be very illiquid |
| EM Bonds (EMB) | ±0.20% to ±1.0% | Illiquid underlyings + time-zone issues |
| International Equity (EFA, EEM, VWO) | ±0.10% to ±0.50% | Time-zone mismatch when US trades but foreign markets closed |
| China/EM Single-Country (KWEB, FXI, INDA) | ±0.15% to ±0.80% | Capital controls, ADR conversion, and time-zone effects |
| Commodity (GLD, SLV, IAU) | ±0.05% to ±0.20% | Physical backing is straightforward but has storage costs |
| Futures-Based Commodity (USO, UNG) | ±0.20% to ±1.0% | Contango/backwardation and roll mechanics |
| Crypto (IBIT, BITO, FBTC) | ±0.50% to ±3.0% | Young market, high demand, AP mechanics still developing |
| Leveraged/Inverse (TQQQ, SQQQ) | ±0.20% to ±1.5% | Daily reset, compounding effects, and swap counterparty risk |
| Thematic/Active (ARKK, JEPI) | ±0.10% to ±0.50% | Varies with popularity and underlying liquidity |

### Stress Scenarios

During market stress (e.g., March 2020 COVID crash, 2022 bond rout), discounts can widen dramatically:
- Bond ETFs saw discounts of 3-5% during March 2020
- High-yield ETFs (HYG, JNK) hit 5%+ discounts
- International ETFs can gap to 2-3% premiums/discounts during geopolitical events

---

## Common ETF Universe for Screening

### Tier 1: Core Liquid ETFs (good for baseline comparison)

```
SPY, QQQ, IVV, VOO, VTI, DIA, IWM
AGG, BND, TLT, HYG, LQD
EFA, EEM, VWO
GLD, SLV
```

### Tier 2: Category Leaders

```
# Bond
VCIT, VCSH, BNDX, EMB, JNK, MUB, TIP, GOVT, SHY, IEF

# International
IEMG, KWEB, FXI, INDA, VEA, MCHI, EWZ, EWJ

# Commodity
USO, UNG, DBC, IAU, PDBC, GSG, WEAT, CORN

# Crypto
IBIT, BITO, FBTC, ETHA, ARKB, GBTC

# Leveraged/Inverse
TQQQ, SQQQ, SPXU, UPRO, JNUG, JDST, SOXL, SOXS

# Sector
XLF, XLE, XLK, XLV, XLI, XLP, XLU, XLRE, XLC, XLB, XLY

# Sector - Semis/Tech (often show large premiums/discounts)
SOXX, SMH, IGV, XSD

# Sector - Healthcare (frequently discounted during volatility)
XBI, IBB, IHI

# Income / Dividend
JEPI, JEPQ, SCHD, VYM, DVY, DIVO, HDV, QYLD

# Thematic / Active (prone to large premiums/discounts due to illiquid underlyings)
ARKK, ARKW, ARKG, HACK, CLOU, WCLD, BUG, BOTZ, ROBO, LIT, TAN, ICLN
```

### Tier 3: Peer Comparison Groups

When analyzing a single ETF, compare it to peers in the same category. This helps distinguish ETF-specific deviations from market-wide patterns.

```
Digital Assets:          IBIT, BITO, FBTC, ETHA, ARKB, GBTC
Intermediate Core Bond:  AGG, BND, SCHZ
High Yield Bond:         HYG, JNK, USHY
Long Government:         TLT, VGLT, SPTL
EM Bond:                 EMB, VWOB, PCY
Large Growth:            QQQ, VUG, IWF, SCHG
Large Blend:             SPY, VOO, IVV, VTI
Commodities:             GLD, IAU, SLV, DBC
China Region:            KWEB, FXI, MCHI
Leveraged Bull:          TQQQ, UPRO, SOXL, JNUG
Leveraged Bear:          SQQQ, SPXU, SOXS, JDST
Derivative Income:       JEPI, JEPQ, QYLD
Large Value/Dividend:    SCHD, VYM, DVY, HDV
```

---

## Bid-Ask Spread as a Reality Check

A premium/discount that is smaller than the bid-ask spread is not economically meaningful — it's just the cost of trading. Always compare:

```
If |Premium%| < Bid-Ask Spread%:
    → The premium/discount is within market microstructure noise
    → Not actionable

If |Premium%| > Bid-Ask Spread%:
    → The premium/discount represents a real deviation from NAV
    → Worth investigating further
```

---

## Historical Context (Cannot Be Computed from yfinance Alone)

For historical premium/discount analysis, users would need:
- **ETF issuer websites**: iShares, Vanguard, SPDR publish historical premium/discount data for their funds
- **Bloomberg Terminal**: Gold standard for historical NAV time series
- **SEC N-PORT filings**: Contain NAV data but lag by ~60 days
- **SSGA website**: Publishes daily premium/discount history with downloadable Excel files for SPDR ETFs

The skill focuses on **current snapshot** analysis since yfinance provides only the most recent NAV.
