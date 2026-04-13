# Annotated Skill Examples

Real excerpts from the best skills in this repo, with annotations explaining why specific patterns work.

## Example 1: Exhaustive Description (sepa-strategy)

```yaml
description: >
  Analyze stocks using Mark Minervini's SEPA (Specific Entry Point Analysis) methodology.
  Use this skill whenever the user mentions SEPA, Minervini, superperformance, trend template,
  VCP (Volatility Contraction Pattern), Stage 2 uptrend, stage analysis, pivot point breakout,
  or asks about growth stock screening criteria. Also triggers when the user wants to evaluate
  whether a stock meets swing trading entry criteria, check moving average alignment (bullish
  stacking: price above 50MA above 150MA above 200MA), assess breakout quality with volume confirmation,
  calculate position sizing based on risk percentage, or identify consolidation patterns like
  cup-with-handle, flat base, bull flag, or high tight flag. Use this skill even when the user
  simply asks "should I buy this stock" or "is this a good setup" in the context of growth/momentum
  trading, or when they share a stock chart and want pattern analysis.
```

**Why this works:**
- Starts with the formal methodology name (expert trigger)
- Lists 8+ domain-specific terms (VCP, Stage 2, pivot point, bullish stacking)
- Describes behavioral triggers ("evaluate whether a stock meets...")
- Includes sideways entries ("should I buy this stock", "is this a good setup")
- Covers input modalities ("share a stock chart")

---

## Example 2: Comprehensive Defaults Table (options-payoff)

```markdown
| Field | Where to find it | Default if missing |
|---|---|---|
| Strategy type | Title bar / leg description | "custom" |
| Underlying | Ticker symbol | SPX |
| Strike(s) | K1, K2, K3... in title or leg table | nearest round number |
| Premium paid/received | Filled price or avg price | 5.00 |
| Quantity | Position size | 1 |
| Multiplier | 100 for equity options, 100 for SPX | 100 |
| Expiry | Date in title | 30 DTE |
| Spot price | Current underlying price (NOT strike) | middle strike |
| IV | Shown in greeks panel, or estimate from vega | 20% |
| Risk-free rate | — | 4.3% |
```

**Why this works:**
- Three columns: Field, Where to find it (extraction guidance), Default
- Covers EVERY parameter — the skill never stalls
- Defaults are reasonable (SPX is the most common underlying, 30 DTE is standard)
- Includes a critical warning: "spot price is NOT the strike"

---

## Example 3: Pass/Fail Gate (sepa-strategy, Step 2)

```markdown
## Step 2: Stage Analysis — Identify the Current Stage

| Stage | Characteristics | Action |
|---|---|---|
| **Stage 1** — Basing | Price near 200MA, MA flat/declining | Do nothing, wait |
| **Stage 2** — Advancing | Higher highs/lows, bullish MA alignment | **Only stage to buy** |
| **Stage 3** — Topping | Wide swings at highs, false breakouts | Reduce, no new positions |
| **Stage 4** — Declining | Below all MAs, bearish alignment | Full cash, stay away |

If the stock is NOT in Stage 2, stop here and tell the user. No further analysis needed.
```

**Why this works:**
- Clear classification table (4 options, each with characteristics and action)
- **Hard gate**: "stop here" — prevents wasted analysis on Stage 1/3/4 stocks
- The gate is explicit and non-negotiable, not a suggestion
- Saves tokens and produces more accurate results

---

## Example 4: Router Pattern (stock-correlation, Step 2)

```markdown
## Step 2: Route to the Correct Sub-Skill

| User Request | Route To | Examples |
|---|---|---|
| Single ticker, wants related stocks | **Sub-Skill A** | "what correlates with NVDA" |
| Two+ tickers, wants relationship | **Sub-Skill B** | "correlation between AMD and NVDA" |
| Group, wants structure/grouping | **Sub-Skill C** | "correlation matrix for FAANG" |
| Time-varying or conditional | **Sub-Skill D** | "rolling correlation AMD NVDA" |

If ambiguous, default to **Sub-Skill A** for single tickers, **Sub-Skill B** for two tickers.
```

**Why this works:**
- Routing table with concrete examples for each path
- Default behavior for ambiguous cases — the skill never stalls
- Each sub-skill is self-contained with its own sub-steps (A1, A2, A3)

---

## Example 5: Detection Flow with Decision Tree (github-auth)

```markdown
## Detection Flow

` ` `bash
git --version
gh --version 2>/dev/null || echo "gh not installed"
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
` ` `

**Decision tree:**
1. If `gh auth status` shows authenticated → use `gh` for everything
2. If `gh` is installed but not authenticated → use "gh auth" method
3. If `gh` is not installed → use "git-only" method (no sudo needed)
```

**Why this works:**
- Detects 4 dimensions in one block: git, gh, gh auth, credential helper
- Decision tree has 3 clear paths — skill works for everyone
- Each path leads to a self-contained method section
- Never assumes — always checks first

---

## Example 5b: Dual-Method with Runtime Awareness (duckduckgo-search)

```markdown
## Detection Flow

` ` `bash
command -v ddgs >/dev/null && echo "DDGS_CLI=installed" || echo "DDGS_CLI=missing"
` ` `

Decision tree:
1. If `ddgs` CLI is installed → prefer `terminal` + `ddgs`
2. If `ddgs` CLI is missing → do not assume `execute_code` can import `ddgs`
3. If the user wants DuckDuckGo specifically → install `ddgs` first
4. Otherwise → fall back to built-in web/browser tools

**Important runtime note:**
- Terminal and `execute_code` are separate runtimes
- A successful shell install does not guarantee `execute_code` can import `ddgs`
```

**Why this works:**
- Explicitly warns about the terminal vs execute_code runtime boundary
- 4-level degradation chain: CLI → Python → install → built-in fallback
- `fallback_for_toolsets: [web]` in frontmatter auto-hides when web toolset is configured
- Combines frontmatter-level activation control with runtime-level method selection

---

## Example 6: Runtime Dependency Check with Algorithm Fallback (stock-correlation)

```markdown
## Step 1: Ensure Dependencies Are Available

**Current environment status:**

` ` `
!`python3 -c "import yfinance, pandas, numpy; print(f'yfinance={yfinance.__version__} pandas={pandas.__version__} numpy={numpy.__version__}')" 2>/dev/null || echo "DEPS_MISSING"`
` ` `

If `DEPS_MISSING`, install required packages before running any code:

` ` `python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "numpy"])
` ` `

If all dependencies are already installed, skip the install step and proceed directly.
```

**Why this works:**
- Checks at runtime, not static instructions
- Reports actual versions (useful for debugging)
- Graceful fallback (`|| echo "DEPS_MISSING"`)
- Conditional action: only install if needed, skip otherwise
- Includes the exact install command — no guessing

---

## Example 7: Structured Output Template (sepa-strategy, Step 9)

```markdown
## Step 9: Respond to the User

Present a structured analysis report with these sections:

1. **Stock & Stage**: Ticker, current price, identified stage, base count
2. **Trend Template Scorecard**: 8-condition checklist with pass/fail and actual values
3. **Fundamental Grade**: A/B/C/D with EPS growth, acceleration, revenue, margins
4. **Pattern Identified**: Which pattern, key measurements
5. **Entry Assessment**: Pivot price, buy zone, breakout volume requirement
6. **Position Sizing**: Exact shares, stop price, targets, reward/risk ratio
7. **Market Environment**: Current assessment and sizing impact
8. **Overall Verdict**: Strong Buy Setup / Watch List / Pass

Always end with the disclaimer that this is educational analysis, not investment advice.
```

**Why this works:**
- 8 numbered sections — output is always structured identically
- Each section specifies exactly what data to include
- Verdict system with 3 clear options (not a spectrum, a decision)
- Mirrors the step structure (steps 2-8 → output sections 1-8)
- Ends with required disclaimer

---

## Example 8: Reference File Pointer Pattern (sepa-strategy)

```markdown
## Reference Files

- `references/stage-analysis.md` — Four-stage theory, transition signals, base counting
- `references/trend-template.md` — Detailed 8-condition explanations and memory aids
- `references/fundamentals.md` — EPS, revenue, margins, institutional holdings, catalysts
- `references/patterns.md` — VCP 7 rules, cup-with-handle, flat base, flag, HTF
- `references/entry-rules.md` — Pivot point mechanics, buy zone, true vs false breakout
- `references/position-sizing.md` — Formula, stop loss evolution, pyramiding, loss handling
- `references/market-environment.md` — Bull/choppy/bear criteria and position adjustments
```

**Why this works:**
- Each reference file is listed with a one-line description
- Descriptions tell you what's in the file without opening it (saves tokens)
- Files are organized by concept-cluster, not by step
- 7 files is near the sweet spot for methodology-pattern skills

---

## Example 9: Edge Cases in Reference File (options-payoff, strategies.md)

```markdown
## Edge Cases

- **DTE = 0**: skip BS entirely, use intrinsic value only
- **IV = 0**: BS undefined (σ=0), use max(intrinsic, 0)
- **K1 > K2**: warn user, auto-sort strikes ascending
- **Negative theoretical value**: clip to 0 for display (arbitrage-free floor)
- **Calendar with IV skew**: use separate IV sliders for near vs far leg
```

**Why this works:**
- Specific conditions, not vague "handle errors"
- Each edge case has an exact resolution
- Placed in the reference file (not SKILL.md) to keep main instructions lean
- These are the cases that would cause bugs without explicit handling

---

## Anti-Example: Vague Output (avoid this)

```markdown
## Respond to the User

Summarize the analysis results in a clear and readable format.
Include relevant metrics and insights.
```

**Why this fails:**
- "Clear and readable" means different things every time
- "Relevant metrics" — which ones? All of them? Top 3?
- No numbered sections → inconsistent output across runs
- No verdict → user must interpret everything themselves
