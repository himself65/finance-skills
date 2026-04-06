---
name: startup-analysis
description: >
  Analyze a startup from three distinct perspectives: VC investor, job applicant, and CEO/founder.
  Use this skill whenever the user wants to evaluate a startup company, assess whether to invest in
  or join a startup, do due diligence on a company, evaluate a job offer from a startup, understand
  a startup's competitive position, or assess company health and trajectory.
  Triggers include: "analyze this startup", "should I join [company]", "is [company] a good investment",
  "evaluate [company]", "due diligence on [company]", "what do you think of [startup]",
  "tell me about [company] as an investment", "should I take this startup job offer",
  "how healthy is [company]", "startup assessment", "company analysis", "evaluate this company",
  "is [company] worth joining", "what's the outlook for [company]", "research [company] for me",
  any mention of evaluating, analyzing, or assessing a startup or tech company from investment,
  career, or strategic perspectives — even if the user doesn't specify a perspective, provide all three.
---

# Startup Analysis

Produces a multi-perspective analysis of a startup, examining it through three lenses that each reveal different aspects of company health and potential:

1. **VC Investor Lens** — Is this a good investment? Market size, unit economics, growth trajectory, team quality, defensibility
2. **Job Applicant Lens** — Should I work here? Equity value, runway risk, culture signals, career growth, compensation fairness
3. **CEO/Founder Lens** — How healthy is this company? Product-market fit, burn efficiency, competitive moat, organizational health

Each perspective surfaces insights the others miss. A company can be a great investment but a terrible place to work (or vice versa). The goal is to give the user a 360-degree view so they can make informed decisions.

---

## Step 1: Gather Information

Before analyzing, collect as much public information as possible about the startup. Use web search, the company's website, Crunchbase data, press coverage, and any other available sources.

**Key data to gather:**

| Category | What to find |
|----------|-------------|
| **Basics** | Founded year, HQ location, employee count, what the product does |
| **Funding** | Total raised, last round (size, date, valuation if known), key investors |
| **Product** | What they sell, who buys it, pricing model, key competitors |
| **Traction** | Users, revenue (if public), growth signals, notable customers |
| **Team** | Founders' backgrounds, key hires, LinkedIn headcount trends |
| **Market** | Industry, market size estimates, tailwinds/headwinds |
| **News** | Recent press, product launches, partnerships, layoffs, pivots |

If certain data isn't publicly available (e.g., revenue for private companies), note the gap and infer what you can from indirect signals (hiring pace, customer logos, web traffic proxies, job postings).

---

## Step 2: Determine Which Perspectives to Cover

By default, produce all three perspectives. If the user specifies a particular angle (e.g., "I'm considering joining them" or "should I invest"), emphasize that perspective but still include the others as context — they often reveal relevant information.

| User's situation | Primary perspective | Still include |
|-----------------|-------------------|---------------|
| Considering investing | VC Investor | Job Applicant (talent signal), CEO (operational health) |
| Considering a job offer | Job Applicant | VC Investor (funding runway), CEO (strategic direction) |
| Running the company / advisory | CEO/Founder | VC Investor (how investors see you), Job Applicant (talent attractiveness) |
| General curiosity / research | All equally | — |

---

## Step 3: Analyze from Each Perspective

Read the relevant reference files for the detailed framework for each perspective. These contain the specific criteria, metrics, and red/green flags to evaluate.

### VC Investor Analysis

Read `references/vc-framework.md` for the full evaluation framework.

Core areas to assess:
- **Market opportunity** — TAM/SAM/SOM, market timing, secular trends
- **Product & traction** — Product-market fit signals, growth metrics, retention
- **Unit economics** — CAC, LTV, margins, burn multiple, path to profitability
- **Team** — Founder-market fit, technical depth, hiring ability
- **Defensibility** — Moats (network effects, switching costs, data, brand, regulatory)
- **Deal terms context** — Stage-appropriate valuation, comparable exits

Produce a clear **Investment Thesis** (bull case) and **Key Risks** (bear case). End with a verdict: Strong Pass / Lean Pass / Lean Invest / Strong Invest, with reasoning.

### Job Applicant Analysis

Read `references/job-applicant-framework.md` for the full evaluation framework.

Core areas to assess:
- **Financial stability** — Runway, burn rate, funding trajectory, revenue health
- **Equity value** — Option/equity package analysis, dilution risk, liquidation preferences, realistic exit scenarios
- **Career growth** — Role scope, learning opportunity, resume value, mentorship
- **Culture & work-life** — Glassdoor signals, employee tenure data, leadership style
- **Product & market risk** — Is PMF real? What happens if the startup fails?
- **Red flags** — High turnover, constant pivots, vague metrics, founders cashing out

Produce a clear **Why Join** (pros) and **Watch Out For** (risks). End with a verdict: Strong Pass / Lean Pass / Lean Join / Strong Join, with reasoning.

### CEO/Founder Analysis

Read `references/ceo-framework.md` for the full evaluation framework.

Core areas to assess:
- **Product-market fit** — Retention curves, organic growth, Sean Ellis test proxy
- **Growth efficiency** — Burn multiple, CAC payback, magic number
- **Competitive position** — Moat strength, competitive dynamics, market share trajectory
- **Organizational health** — Hiring pipeline, attrition, team capability gaps
- **Fundraising readiness** — Metrics vs. benchmarks for next round, investor narrative
- **Strategic risks** — Platform dependency, customer concentration, regulatory exposure

Produce a clear **Strengths to Double Down On** and **Urgent Areas to Address**. End with a health grade: Critical / Struggling / Stable / Strong / Exceptional, with reasoning.

---

## Step 4: Synthesize Cross-Perspective Insights

After the three analyses, add a synthesis section that highlights:

1. **Where perspectives agree** — If all three lenses flag the same strength or weakness, it's probably real
2. **Where perspectives diverge** — A company can be VC-attractive (huge market) but employee-risky (high burn, low runway). Call these out.
3. **The bottom line** — One paragraph summary: what kind of company is this, what's its most likely trajectory, and what should the user do based on their stated (or implied) situation

---

## Step 5: Present the Report

Structure the output as a clean, scannable report:

```
# [Company Name] — Startup Analysis

## Summary
[2-3 sentence overview with key verdict]

## VC Investor Perspective
### Market Opportunity
### Product & Traction
### Unit Economics (if available)
### Team
### Defensibility
### Investment Verdict: [Strong Pass / Lean Pass / Lean Invest / Strong Invest]
[Reasoning]

## Job Applicant Perspective
### Financial Stability
### Equity Value Assessment
### Career Growth Potential
### Culture & Work-Life Signals
### Risk Factors
### Employment Verdict: [Strong Pass / Lean Pass / Lean Join / Strong Join]
[Reasoning]

## CEO/Founder Perspective
### Product-Market Fit Assessment
### Growth Efficiency
### Competitive Position
### Organizational Health
### Strategic Risks
### Health Grade: [Critical / Struggling / Stable / Strong / Exceptional]
[Reasoning]

## Cross-Perspective Synthesis
### Points of Agreement
### Points of Divergence
### Bottom Line
```

Adapt section depth to available data — if financials are completely opaque, say so and focus on what's observable. Don't fabricate metrics, but do make informed inferences and state your confidence level.

---

## Reference Files

- `references/vc-framework.md` — VC due diligence checklist with metrics, benchmarks, and red/green flags
- `references/job-applicant-framework.md` — Job seeker evaluation framework with equity analysis and culture assessment
- `references/ceo-framework.md` — CEO self-assessment framework with operational metrics and strategic analysis

Read these when you need the detailed criteria and benchmarks for each perspective.
