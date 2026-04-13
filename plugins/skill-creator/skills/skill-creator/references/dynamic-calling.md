# Dynamic Calling Patterns

Skills MUST detect what's available at runtime and adapt. Never hardcode a single tool or method. This reference catalogs every dynamic pattern used in production skills.

**Core principle:** The skill should work in as many environments as possible. A user with `gh` CLI gets the rich path. A user with only `git` gets the minimal path. A user with nothing gets clear install instructions. The skill never fails silently because a hardcoded tool is missing.

---

## Pattern 1: Detection Flow with Decision Tree

The foundational pattern. Every skill that touches external tools starts here.

### Structure

```markdown
## Step 1: Detection Flow

` ` `
!`(command -v tool_a && tool_a --version) 2>/dev/null || echo "TOOL_A_MISSING"`
` ` `

` ` `
!`(command -v tool_b && tool_b --version) 2>/dev/null || echo "TOOL_B_MISSING"`
` ` `

**Decision tree:**
1. If `tool_a` available and authenticated → use Method 1 (preferred)
2. If `tool_a` available but not authenticated → guide auth setup, then Method 1
3. If `tool_a` missing but `tool_b` available → use Method 2 (fallback)
4. If neither available → install `tool_a` (preferred) or `tool_b` (lighter)
```

### Real Example: github-auth (gh vs git)

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
- Detects 4 dimensions: git existence, gh existence, gh auth state, git credential state
- Three clear paths, each self-contained
- The skill works for everyone — from minimal git-only setups to full gh installations

---

## Pattern 2: Multi-Stage Detection (Install → Auth → Health)

For tools that need multiple checks before they're usable.

### Structure

```
!`(command -v tool && tool status 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

This single command checks three things:
1. Is the tool installed? (`command -v tool`)
2. Can it run? (`tool status`)
3. Is it healthy? (output + `echo "READY"`)

### Real Example: discord-reader (opencli)

```markdown
` ` `
!`(command -v opencli && opencli discord-app status 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
` ` `

If `READY`, skip to Step 2.
If `NOT_INSTALLED`, install first: `npm install -g @jackwener/opencli`
If `SETUP_NEEDED`, guide through CDP setup.
```

### Real Example: telegram-reader (tdl — two-stage)

```markdown
` ` `
!`command -v tdl 2>/dev/null && echo "TDL_INSTALLED" || echo "TDL_NOT_INSTALLED"`
` ` `

` ` `
!`tdl chat ls --limit 1 2>/dev/null && echo "TDL_AUTHENTICATED" || echo "TDL_NOT_AUTHENTICATED"`
` ` `

Decision tree:
1. Both OK → proceed to Step 2
2. Installed but not authenticated → run `tdl login`
3. Not installed → install via `go install` or binary download
```

**Why two-stage:** Some tools pass `--version` but fail on actual operations because auth is missing. Checking auth separately gives better error messages.

---

## Pattern 3: Library Version Detection with Fallback

For Python skills that need specific libraries.

### Structure

```
!`python3 -c "import lib; print('lib ' + lib.__version__)" 2>/dev/null || echo "LIB_NOT_INSTALLED"`
```

### Real Example: stock-correlation (multi-package + algorithm fallback)

```markdown
` ` `
!`python3 -c "import yfinance, pandas, numpy; print(f'yfinance={yfinance.__version__} pandas={pandas.__version__} numpy={numpy.__version__}')" 2>/dev/null || echo "DEPS_MISSING"`
` ` `

If `DEPS_MISSING`, install:
` ` `python
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "numpy"])
` ` `
```

And later in the clustering step:
```markdown
Note: if `scipy` is not available, fall back to sorting by average correlation
instead of hierarchical clustering.
```

**Key insight:** The detection happens at Step 1, but the fallback logic is **also** in the core step that uses the optional dependency. Don't just detect — also provide alternatives at each usage point.

---

## Pattern 4: API Key Detection

For skills that wrap external APIs.

### Structure

```
!`echo $API_KEY | head -c 8 && echo "...KEY_SET" || echo "KEY_NOT_SET"`
```

### Real Example: funda-data

```markdown
` ` `
!`echo $FUNDA_API_KEY | head -c 8 && echo "...KEY_SET" || echo "KEY_NOT_SET"`
` ` `

If `KEY_NOT_SET`:
- Ask the user for their Funda API key
- Guide them to https://funda.ai/dashboard to get one
- Once provided, export it: `export FUNDA_API_KEY=<key>`
```

### Real Example: finance-sentiment (multi-line Python check)

```markdown
` ` `
!`python3 -c "
import os
key = os.environ.get('ADANOS_API_KEY', '')
if key:
    print(f'KEY={key[:8]}...SET')
else:
    print('KEY_NOT_SET')
" 2>/dev/null || echo "PYTHON_UNAVAILABLE"`
` ` `
```

**Why show partial key:** Showing the first 8 characters lets the user verify they have the right key without exposing the full secret.

---

## Pattern 5: Live Data Injection

For skills that need current market data, not stale defaults.

### Structure

```
!`python3 -c "import yfinance as yf; print(f'PRICE={yf.Ticker(\"^GSPC\").fast_info[\"lastPrice\"]:.0f}')" 2>/dev/null || echo "PRICE_UNAVAILABLE"`
```

### Real Example: options-payoff (current SPX price)

```markdown
**Current SPX reference price:**
` ` `
!`python3 -c "import yfinance as yf; print(f'SPX ≈ {yf.Ticker(\"^GSPC\").fast_info[\"lastPrice\"]:.0f}')" 2>/dev/null || echo "SPX price unavailable — check market data"`
` ` `
```

**Why this matters for options:** A default spot price of "5000" becomes wrong within days. Live injection means the payoff chart is immediately useful without manual adjustment.

**Fallback design:** When live data fails, the skill still works — it just uses a static default and tells the user to check.

---

## Pattern 6: Frontmatter Conditional Activation

Skills can declare themselves as fallbacks or require specific tools at the YAML level.

### `fallback_for_toolsets` — Activate when primary is missing

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]
```

**Real example:** duckduckgo-search only appears when the web toolset (with API keys) is NOT configured. Once the user sets up Firecrawl, the skill auto-hides.

### `requires_toolsets` — Only show when tools exist

```yaml
metadata:
  hermes:
    requires_toolsets: [terminal]
```

**Real example:** docker-management only appears when terminal tools are active — it makes no sense on Claude.ai.

### Combining with runtime detection

Frontmatter controls **whether the skill loads**. Runtime detection controls **how the skill behaves once loaded**. Use both:

```yaml
# Frontmatter: only load when terminal is available
metadata:
  hermes:
    requires_toolsets: [terminal]
```

```markdown
# Runtime: detect WHICH terminal tools are available
!`command -v gh && echo "GH_OK" || echo "GH_MISSING"`
```

---

## Pattern 7: Dual-Method Skills (CLI preferred, Python fallback)

The most common pattern for data-fetching skills.

### Structure

```markdown
## Step 2: Fetch Data

### If CLI detected (preferred)
` ` `bash
ddgs text -k "query" -m 5 -o json
` ` `

### If Python library available (fallback)
` ` `python
from ddgs import DDGS
with DDGS() as ddgs:
    results = list(ddgs.text("query", max_results=5))
` ` `

### If neither available
Install the CLI: `pip install ddgs`
```

### Real Example: duckduckgo-search decision tree

```markdown
1. If `ddgs` CLI is installed → prefer `terminal` + `ddgs` (fastest, simplest)
2. If `ddgs` CLI is missing → do not assume `execute_code` can import `ddgs`
3. If the user wants DuckDuckGo specifically → install `ddgs` first
4. Otherwise → fall back to built-in web/browser tools
```

**Critical runtime awareness:**
> Terminal and `execute_code` are separate runtimes. A successful shell install does not guarantee `execute_code` can import `ddgs`. Never assume third-party Python packages are preinstalled inside `execute_code`.

---

## Pattern 8: Runtime Environment Awareness

Different execution environments have different capabilities. Skills must not assume.

### Key distinctions

| Environment | Has shell | Has pip | Has browser | Has internet |
|---|---|---|---|---|
| Claude Code (CLI) | Yes | Yes | No (unless MCP) | Yes |
| Claude.ai (web) | Sandboxed | Limited | No | Restricted |
| Hermes Agent (terminal) | Yes | Yes | Configurable | Yes |
| execute_code sandbox | Isolated | Pre-installed only | No | Varies |

### Rule: Test in the runtime you'll use

```markdown
# WRONG — installs in terminal, uses in execute_code
` ` `bash
pip install ddgs
` ` `
` ` `python
# In execute_code — this might fail because it's a different runtime!
from ddgs import DDGS
` ` `

# RIGHT — verify in the runtime where you'll use it
` ` `python
# Check if available in this runtime
try:
    from ddgs import DDGS
    print("DDGS available")
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "ddgs"])
    from ddgs import DDGS
` ` `
```

---

## Pattern 9: Graceful Degradation Chain

When multiple tools can do the same job, prefer the richest and fall back gracefully.

### Structure

```
Preferred (richest) → Standard → Minimal → Manual instruction
```

### Example: Web search degradation

```
1. web_search tool (if available) → richest, API-backed
2. ddgs CLI (if installed) → free, no key needed
3. ddgs Python library (if importable) → same but in sandbox
4. curl + manual URL → always works but crudest
5. Ask user to search → last resort
```

### Example: GitHub operations degradation

```
1. gh CLI authenticated → full API (PRs, issues, reviews, CI)
2. gh CLI not authenticated → guide auth, then full API
3. git + curl + token → basic API (push, pull, simple operations)
4. git only (no token) → read-only operations on public repos
```

---

## Anti-Patterns to Avoid

### Hardcoded single tool

```markdown
# BAD — fails immediately if yfinance not installed
` ` `python
import yfinance as yf
data = yf.download("AAPL")
` ` `
```

**Fix:** Always detect first, then use.

### Assuming install means available

```markdown
# BAD — installs in shell, assumes execute_code has it
pip install ddgs
# ... later in execute_code ...
from ddgs import DDGS  # might fail!
```

**Fix:** Check in the same runtime where you'll use the library.

### Static tool paths

```markdown
# BAD — path differs across OS and installs
/usr/local/bin/gh auth status
```

**Fix:** Use `command -v gh` to find the tool wherever it is.

### No fallback on detection failure

```markdown
# BAD — no || fallback, command hangs or errors silently
!`tool_a --version`
```

**Fix:** Always use `|| echo "SENTINEL"` fallbacks.

### Detecting once, ignoring later

```markdown
# BAD — detects scipy in Step 1 but hardcodes scipy.cluster in Step 4
```

**Fix:** Every step that uses an optional tool should have inline fallback logic, not just the detection step.

---

## Quick Reference: Detection Commands

| What to detect | Command |
|---|---|
| CLI tool exists | `command -v tool 2>/dev/null` |
| CLI tool version | `tool --version 2>/dev/null` |
| Tool is authenticated | `tool auth status 2>/dev/null` |
| Python module available | `python3 -c "import mod; print(mod.__version__)"` |
| Env var is set | `echo $VAR \| head -c 8 && echo "...SET"` |
| File exists | `test -f ~/.config/tool/creds && echo "OK"` |
| API is reachable | `curl -sf endpoint \| head -c 100` |
| Runtime has internet | `curl -sf https://httpbin.org/get > /dev/null && echo "OK"` |

All commands should end with `|| echo "FALLBACK_SENTINEL"` for graceful handling.
