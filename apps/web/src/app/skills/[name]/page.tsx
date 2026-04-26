import { skills, getSkill, categoryLabels, pluginGroupLabels } from "@/data/skills";
import type { Skill } from "@/data/skills";
import { notFound } from "next/navigation";
import { Link } from "next-view-transitions";
import { SepaStudyGuide } from "./sepa-study-guide";
import dynamic from "next/dynamic";
import type { TabContent, TerminalLine } from "../../terminal-animation";

const TerminalAnimation = dynamic(
  () => import("../../terminal-animation").then((mod) => mod.TerminalAnimation)
);

export function generateStaticParams() {
  return skills.map((s) => ({ name: s.name }));
}

export default async function SkillDetailPage({
  params,
}: {
  params: Promise<{ name: string }>;
}) {
  const { name } = await params;
  const skill = getSkill(name);
  if (!skill) notFound();

  return (
    <div className="min-h-screen">
      {/* Nav */}
      <nav className="border-b border-border px-6 py-3" style={{ viewTransitionName: "site-nav" }}>
        <div className="max-w-5xl mx-auto flex items-center gap-2 text-sm">
          <Link href="/" scroll={false} className="font-semibold hover:text-accent transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded">
            Finance Skills
          </Link>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-8" style={{ viewTransitionName: "page-content" }}>
        {/* Breadcrumb */}
        <p className="text-sm text-text-muted mb-4">
          <Link href="/" scroll={false} className="hover:text-text-secondary transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded">
            skills
          </Link>
          <span className="mx-1.5">/</span>
          <Link href="/" scroll={false} className="hover:text-text-secondary transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded">
            himself65
          </Link>
          <span className="mx-1.5">/</span>
          <Link href="/" scroll={false} className="hover:text-text-secondary transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded">
            finance-skills
          </Link>
          <span className="mx-1.5">/</span>
          <span className="text-text-secondary">{skill.name}</span>
        </p>

        {/* Title */}
        <div className="flex items-center gap-3 mb-3">
          <h1 className="text-3xl font-bold tracking-tight text-balance">
            {skill.name}
          </h1>
          {skill.badge === "new" && (
            <span className="text-xs font-semibold uppercase tracking-wider bg-accent/15 text-accent px-2 py-1 rounded">
              New
            </span>
          )}
          {skill.badge === "paid" && (
            <span className="text-xs font-semibold uppercase tracking-wider bg-yellow/15 text-yellow px-2 py-1 rounded">
              Paid
            </span>
          )}
        </div>

        <div className="flex gap-10 flex-col lg:flex-row">
          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="border border-border rounded-lg overflow-hidden">
              <div className="border-b border-border px-4 py-2.5 bg-bg-elevated flex items-center gap-2 text-xs text-text-muted">
                <svg
                  className="w-4 h-4"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 13.25 16h-9.5A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h9.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 9 4.25V1.5Zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914Z" />
                </svg>
                SKILL.md
              </div>
              <div className="p-6 space-y-4">
                <h2 className="text-xl font-bold">{skill.title}</h2>
                <p className="text-text-secondary leading-relaxed">
                  {skill.description}
                </p>

                <div className="flex gap-2 flex-wrap">
                  <Link
                    href={`/?plugin=${skill.plugin}`}
                    scroll={false}
                    className="text-xs border border-border rounded px-2 py-0.5 text-text-secondary hover:border-accent hover:text-accent transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
                  >
                    {pluginGroupLabels[skill.plugin]}
                  </Link>
                  <span className="text-xs border border-border rounded px-2 py-0.5 text-text-secondary">
                    {categoryLabels[skill.category]}
                  </span>
                  {skill.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-xs border border-border rounded px-2 py-0.5 text-text-secondary"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* Terminal — example usage */}
              <div className="border-t border-border">
                <div className="px-4 py-2.5 bg-bg-elevated flex items-center gap-2 text-xs text-text-muted">
                  <svg className="w-4 h-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                    <path d="M0 2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25Zm.5 3.5a.75.75 0 0 1 .55-.72l.2-.03a.75.75 0 0 1 .53.22l2 2a.75.75 0 0 1 0 1.06l-2 2a.75.75 0 0 1-1.06-1.06L3.94 8 2.47 6.53a.75.75 0 0 1-.22-.53ZM7 10.25a.75.75 0 0 1 .75-.75h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75Z" />
                  </svg>
                  Example
                </div>
                <TerminalAnimation
                  tabs={buildSkillTabs(skill)}
                  variant="card"
                  minHeight="auto"
                />
              </div>
            </div>

            {/* Skill-specific study guide */}
            {skill.name === "sepa-strategy" && <SepaStudyGuide />}
          </div>

          {/* Sidebar */}
          <div className="lg:w-56 shrink-0 space-y-6">
            <div>
              <p className="text-xs uppercase tracking-wider text-text-muted mb-1.5">
                Plugin
              </p>
              <Link
                href={`/?plugin=${skill.plugin}`}
                scroll={false}
                className="text-sm text-accent hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded"
              >
                {pluginGroupLabels[skill.plugin]}
              </Link>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wider text-text-muted mb-1.5">
                Repository
              </p>
              <a
                href="https://github.com/himself65/finance-skills"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-accent hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded"
              >
                himself65/finance-skills
              </a>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wider text-text-muted mb-1.5">
                Install
              </p>
              <div className="space-y-1.5 text-xs text-text-secondary font-mono">
                <p>npx plugins add himself65/finance-skills --plugin finance-{skill.plugin}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Helpers — line builders for mock Claude Code output
// ---------------------------------------------------------------------------

const c = {
  muted: "var(--color-text-muted)",
  secondary: "var(--color-text-secondary)",
  accent: "var(--color-accent)",
  green: "var(--color-green)",
  yellow: "var(--color-yellow)",
} as const;

/** Claude "thinking" line */
function thinking(text: string, delay = 300): TerminalLine {
  return { text: `  ● ${text}`, color: c.accent, delay };
}

/** Tool call header */
function tool(name: string, arg: string, delay = 200): TerminalLine {
  return { text: `  ⏵ ${name}  ${arg}`, color: c.secondary, delay };
}

/** Indented output */
function out(text: string, delay = 80): TerminalLine {
  return { text: `    ${text}`, color: c.muted, delay };
}

/** Blank spacer */
function gap(delay = 60): TerminalLine {
  return { text: "", delay };
}

/** Green success line */
function ok(text: string, delay = 150): TerminalLine {
  return { text: `    ✓ ${text}`, color: c.green, delay };
}

/** Yellow warning line */
function warn(text: string, delay = 150): TerminalLine {
  return { text: `    ⚠ ${text}`, color: c.yellow, delay };
}

/** Plain response text from Claude */
function reply(text: string, delay = 40): TerminalLine {
  return { text: `  ${text}`, color: c.secondary, delay };
}

// ---------------------------------------------------------------------------
// Per-skill mock sessions
// ---------------------------------------------------------------------------

type MockSession = { prompt: string; lines: TerminalLine[] };

const mockSessions: Record<string, MockSession> = {
  "earnings-preview": {
    prompt: "earnings preview for NVDA",
    lines: [
      gap(),
      thinking("Reading skill: earnings-preview"),
      gap(),
      tool("Bash", "pip install yfinance --quiet", 300),
      ok("yfinance installed"),
      gap(),
      tool("Bash", "python3 fetch_earnings.py NVDA", 400),
      out("Fetching consensus estimates from Yahoo Finance..."),
      gap(),
      reply("## NVDA — Earnings Preview (Q4 FY2026)"),
      gap(),
      reply("Report Date:     May 28, 2026 (after close)"),
      reply("Consensus EPS:   $0.89  (12 analysts)"),
      reply("Consensus Rev:   $44.2B (15 analysts)"),
      gap(),
      reply("Beat/Miss History (last 4 quarters):"),
      { text: "    Q3 +12.4%   Q2 +8.7%   Q1 +15.2%   Q4 +11.8%", color: c.green, delay: 80 },
      gap(),
      reply("Analyst Sentiment: Bullish — 82% Buy, 14% Hold, 4% Sell"),
      reply("Options IV (earnings week): 8.2% vs 4.1% 30-day avg"),
    ],
  },

  "earnings-recap": {
    prompt: "how did AAPL earnings go",
    lines: [
      gap(),
      thinking("Reading skill: earnings-recap"),
      gap(),
      tool("Bash", "python3 fetch_recap.py AAPL", 400),
      out("Fetching Q1 FY2026 actuals vs estimates..."),
      gap(),
      reply("## AAPL — Earnings Recap (Q1 FY2026)"),
      gap(),
      reply("EPS:  $2.18 actual vs $2.10 est  → +3.8% surprise"),
      reply("Rev:  $124.3B actual vs $121.1B est  → +2.6% beat"),
      gap(),
      reply("Stock Reaction: +4.2% after-hours"),
      reply("iPhone revenue: $71.4B (+6% YoY) — above expectations"),
      reply("Services: $26.3B (+14% YoY) — new record"),
      gap(),
      reply("Management raised Q2 guidance above consensus."),
    ],
  },

  "estimate-analysis": {
    prompt: "estimate revisions for TSLA",
    lines: [
      gap(),
      thinking("Reading skill: estimate-analysis"),
      gap(),
      tool("Bash", "python3 fetch_estimates.py TSLA", 400),
      out("Loading estimate revision data across 4 periods..."),
      gap(),
      reply("## TSLA — Estimate Revisions"),
      gap(),
      reply("                 Current    7d ago    30d ago   90d ago"),
      reply("FY2026 EPS       $3.42      $3.38     $3.21     $2.98"),
      reply("FY2026 Rev       $128.5B    $127.1B   $124.8B   $119.2B"),
      reply("FY2027 EPS       $4.81      $4.75     $4.52     $4.11"),
      gap(),
      reply("Trend: Consistent upward revisions across all periods."),
      reply("Revisions (30d): 18 up / 3 down / 2 unchanged"),
    ],
  },

  "etf-premium": {
    prompt: "is BITO trading at a premium to NAV?",
    lines: [
      gap(),
      thinking("Reading skill: etf-premium"),
      gap(),
      tool("Bash", "python3 etf_premium.py BITO", 400),
      out("Fetching market price and NAV from Yahoo Finance..."),
      gap(),
      reply("## BITO — Premium/Discount Analysis"),
      gap(),
      reply("Market Price:   $10.06"),
      reply("NAV:            $9.90"),
      reply("Premium:        +1.57%  ($0.16/share)"),
      reply("Bid-Ask Spread: 0.20%  → premium is real, not noise"),
      gap(),
      reply("Peer Comparison (Digital Assets category):"),
      reply("  BITO   +1.57%  ◄ lowest premium"),
      reply("  GBTC   +1.64%"),
      reply("  ARKB   +1.75%"),
      reply("  FBTC   +1.76%"),
      reply("  IBIT   +1.84%"),
      reply("  ETHA   +1.99%"),
      gap(),
      reply("All crypto ETFs at premium today — category-wide pattern."),
      reply("Normal range for crypto ETFs: 0.5% to 3.0%."),
    ],
  },

  "yfinance-data": {
    prompt: "get MSFT financials",
    lines: [
      gap(),
      thinking("Reading skill: yfinance-data"),
      gap(),
      tool("Bash", "python3 -c \"import yfinance; ...\"", 400),
      out("Downloading MSFT financial statements..."),
      gap(),
      reply("## MSFT — Financial Summary"),
      gap(),
      reply("Market Cap:      $3.18T"),
      reply("Revenue (TTM):   $254.2B  (+14.8% YoY)"),
      reply("Net Income:      $89.4B   (+18.2% YoY)"),
      reply("Free Cash Flow:  $74.1B"),
      gap(),
      reply("Margins:  Gross 69.8%  |  Operating 44.6%  |  Net 35.2%"),
      reply("P/E: 35.4x  |  Fwd P/E: 30.1x  |  EV/EBITDA: 26.8x"),
    ],
  },

  "funda-data": {
    prompt: "NVDA options flow",
    lines: [
      gap(),
      thinking("Reading skill: funda-data"),
      gap(),
      tool("Bash", "curl -s 'api.funda.ai/v1/options/flow?symbol=NVDA'", 400),
      out("Fetching live options flow from Funda AI..."),
      gap(),
      reply("## NVDA — Options Flow (today)"),
      gap(),
      reply("Total premium:  $842M  (calls 64% / puts 36%)"),
      reply("Largest block:  NVDA Jul 140C  × 12,000  $18.4M  ask-side"),
      reply("GEX flip:       $128.50"),
      reply("Put wall:       $120.00  (28k OI)"),
      reply("Call wall:      $150.00  (41k OI)"),
      gap(),
      reply("Net delta: +$1.2B — bullish positioning"),
    ],
  },

  "options-payoff": {
    prompt: "show payoff for AAPL 200/210 call spread",
    lines: [
      gap(),
      thinking("Reading skill: options-payoff"),
      gap(),
      tool("Bash", "python3 black_scholes.py AAPL 200 210 call", 400),
      out("Computing Black-Scholes pricing..."),
      gap(),
      reply("## AAPL — Bull Call Spread  200/210"),
      gap(),
      reply("Long  200C:  $8.42   Delta 0.58  IV 24.1%"),
      reply("Short 210C:  $4.18   Delta 0.38  IV 23.6%"),
      reply("Net debit:   $4.24"),
      gap(),
      reply("Max profit:  $5.76  (+135.8%)  at $210+"),
      reply("Max loss:    $4.24  (-100%)     at $200−"),
      reply("Breakeven:   $204.24"),
      gap(),
      reply("P(profit) at expiry: ~52%"),
    ],
  },

  "stock-correlation": {
    prompt: "what correlates with NVDA",
    lines: [
      gap(),
      thinking("Reading skill: stock-correlation"),
      gap(),
      tool("Bash", "python3 correlation.py NVDA --period 90d", 400),
      out("Computing 90-day rolling correlations..."),
      gap(),
      reply("## NVDA — Correlated Stocks (90d)"),
      gap(),
      reply("  AMD     0.91   ████████████████████▏"),
      reply("  AVGO    0.87   ███████████████████▎ "),
      reply("  MRVL    0.84   ██████████████████▋  "),
      reply("  TSM     0.82   ██████████████████▏  "),
      reply("  MU      0.79   █████████████████▌   "),
      gap(),
      reply("Inverse:  TLT −0.41  |  XLU −0.38"),
    ],
  },

  "hormuz-strait": {
    prompt: "Hormuz strait status",
    lines: [
      gap(),
      thinking("Reading skill: hormuz-strait"),
      gap(),
      tool("WebFetch", "tankertracking.com/api/hormuz", 400),
      tool("WebFetch", "oilprice.com/api/brent", 200),
      out("Fetching real-time strait transit data..."),
      gap(),
      reply("## Strait of Hormuz — Live Status"),
      gap(),
      reply("Transits (24h):   38 vessels  (avg: 41)"),
      reply("Oil throughput:    18.2M bbl/d"),
      reply("Brent crude:       $82.14  (+0.8%)"),
      gap(),
      reply("Risk level:  ELEVATED"),
      warn("2 tankers delayed — Iranian naval exercise reported"),
      gap(),
      reply("Insurance premium: +15bps WoW"),
    ],
  },

  "generative-ui": {
    prompt: "visualize AAPL revenue trend",
    lines: [
      gap(),
      thinking("Reading skill: generative-ui"),
      gap(),
      tool("show_widget", "interactive SVG chart", 400),
      out("Rendering inline revenue chart..."),
      gap(),
      reply("## AAPL Revenue — Quarterly Trend"),
      gap(),
      reply("  Q1  ██████████████████████████  $124.3B"),
      reply("  Q4  █████████████████████████   $119.6B"),
      reply("  Q3  ████████████████████████    $116.2B"),
      reply("  Q2  ███████████████████████     $108.4B"),
      gap(),
      reply("↑ Interactive chart rendered in conversation above."),
    ],
  },

  "twitter-reader": {
    prompt: "search Twitter for NVDA sentiment",
    lines: [
      gap(),
      thinking("Reading skill: twitter-reader"),
      gap(),
      tool("Bash", "opencli x search 'NVDA OR $NVDA' --limit 50", 400),
      out("Searching recent tweets..."),
      gap(),
      reply("## NVDA — Twitter Sentiment (last 24h)"),
      gap(),
      reply("Tweets analyzed:  1,284"),
      reply("Sentiment:        72% bullish / 18% neutral / 10% bearish"),
      gap(),
      reply("Top themes:"),
      reply("  • Data center demand surge (382 mentions)"),
      reply("  • Blackwell GPU ramp (241 mentions)"),
      reply("  • Valuation concerns (128 mentions)"),
    ],
  },

  "telegram-reader": {
    prompt: "read my crypto Telegram channels",
    lines: [
      gap(),
      thinking("Reading skill: telegram-reader"),
      gap(),
      tool("Bash", "tdl chat ls --filter subscribed", 300),
      out("Listing subscribed channels..."),
      tool("Bash", "tdl chat export -c 'Crypto Signals' --limit 20", 400),
      gap(),
      reply("## Telegram — Recent Crypto Intel"),
      gap(),
      reply("Channel: Crypto Signals (12.4k members)"),
      reply("  • BTC breaking $72k resistance — watch $74.5k"),
      reply("  • ETH/BTC ratio at 3-month low"),
      gap(),
      reply("Channel: DeFi Alpha"),
      reply("  • New Eigenlayer restaking vault — 8.4% APY"),
      reply("  • Aave v4 governance vote passing"),
    ],
  },

  "discord-reader": {
    prompt: "search Discord for AAPL discussion",
    lines: [
      gap(),
      thinking("Reading skill: discord-reader"),
      gap(),
      tool("Bash", "discordcli search --query 'AAPL' --channels trading", 400),
      out("Searching connected trading servers..."),
      gap(),
      reply("## Discord — AAPL Discussion (48h)"),
      gap(),
      reply("Messages found: 89 across 3 servers"),
      gap(),
      reply("#stocks-general — WallStreet Hub"),
      reply("  \"AAPL broke out of the cup and handle\"  ↑12 reactions"),
      reply("  \"Services revenue is the real story\"     ↑8 reactions"),
      gap(),
      reply("#earnings — Trading Floor"),
      reply("  \"Guidance was the key — bullish into Q2\"  ↑15 reactions"),
    ],
  },

  "linkedin-reader": {
    prompt: "what are analysts saying on LinkedIn about NVDA",
    lines: [
      gap(),
      thinking("Reading skill: linkedin-reader"),
      gap(),
      tool("Bash", "opencli linkedin search 'NVDA analyst' --type posts", 400),
      out("Reading LinkedIn analyst posts..."),
      gap(),
      reply("## LinkedIn — NVDA Analyst Commentary"),
      gap(),
      reply("Dan Ives (Wedbull)  — 2h ago"),
      reply("  \"AI spending is not slowing. NVDA remains our top pick.\""),
      reply("  → 1.2k reactions"),
      gap(),
      reply("Lisa Su (AMD CEO)  — 6h ago"),
      reply("  \"The AI infrastructure buildout is a decade-long trend.\""),
      reply("  → 8.4k reactions"),
    ],
  },

  "opencli-reader": {
    prompt: "pull Eastmoney hot rank and HackerNews top stories",
    lines: [
      gap(),
      thinking("Reading skill: opencli-reader"),
      gap(),
      tool("Bash", "opencli list -f json | grep -E 'eastmoney|hackernews'", 300),
      out("Discovering available adapters..."),
      gap(),
      tool("Bash", "opencli eastmoney hot-rank -f json", 400),
      out("Fetching Eastmoney hot-rank (PUBLIC strategy)..."),
      gap(),
      reply("## Eastmoney — Hot Rank (retail flow)"),
      reply("  1. 贵州茅台 (SH600519)   +2.4%   ¥1,782"),
      reply("  2. 比亚迪 (SZ002594)     +3.1%   ¥248"),
      reply("  3. 宁德时代 (SZ300750)   +1.8%   ¥215"),
      gap(),
      tool("Bash", "opencli hackernews top --limit 5 -f json", 300),
      out("Fetching HN top (PUBLIC strategy)..."),
      gap(),
      reply("## HackerNews — Top 5"),
      reply("  • Show HN: Fast LLM inference on CPU       842 pts"),
      reply("  • The economics of running a side project  614 pts"),
      reply("  • Why we switched from Postgres to DuckDB  489 pts"),
      gap(),
      ok("Fallback successful — both sources pulled without a dedicated skill"),
    ],
  },

  "yc-reader": {
    prompt: "show me YC fintech companies that are hiring",
    lines: [
      gap(),
      thinking("Reading skill: yc-reader"),
      gap(),
      tool("Bash", "curl -s 'api.ycombinator.com/v0.1/companies?tags=fintech'", 400),
      out("Fetching YC fintech companies..."),
      gap(),
      reply("## YC Fintech — Hiring Now"),
      gap(),
      reply("  Mercury (W19)      Banking for startups        42 roles"),
      reply("  Brex (W17)         Corporate cards & spend     38 roles"),
      reply("  Ramp (W19)         Expense management          35 roles"),
      reply("  Stripe (S09)       Payments infrastructure     124 roles"),
      reply("  Plaid (W13)        Banking APIs                28 roles"),
      gap(),
      reply("Total: 23 fintech companies actively hiring (267 roles)"),
    ],
  },

  "startup-analysis": {
    prompt: "analyze LangChain as a potential investment",
    lines: [
      gap(),
      thinking("Reading skill: startup-analysis"),
      gap(),
      tool("WebSearch", "LangChain funding valuation 2026", 400),
      tool("WebFetch", "crunchbase.com/organization/langchain", 300),
      out("Gathering funding data, team info, market position..."),
      gap(),
      reply("## LangChain — 3-Perspective Analysis"),
      gap(),
      reply("VC Investor View:"),
      reply("  Valuation: $3B (Series B, Oct 2025)"),
      reply("  ARR est:   $45M → ~66x revenue multiple"),
      reply("  Risk:      High burn, crowded LLM tooling market"),
      gap(),
      reply("Job Applicant View:"),
      reply("  Team: 142 employees, strong eng culture"),
      reply("  Glassdoor: 4.2/5  |  Runway: ~24 months"),
      gap(),
      reply("CEO/Founder View:"),
      reply("  Moat: developer ecosystem + LangSmith lock-in"),
    ],
  },

  "saas-valuation-compression": {
    prompt: "analyze Vercel valuation from Series D to E",
    lines: [
      gap(),
      thinking("Reading skill: saas-valuation-compression"),
      gap(),
      tool("WebSearch", "Vercel Series D E valuation ARR", 400),
      out("Searching funding rounds and ARR estimates..."),
      gap(),
      reply("## Vercel — Valuation Compression Analysis"),
      gap(),
      reply("Series D (Nov 2021):  $2.5B at ~150x ARR"),
      reply("Series E (May 2024):  $3.2B at ~40x ARR"),
      reply("Compression:          −73% multiple reduction"),
      gap(),
      reply("ARR growth:  $17M → $80M (+370%)"),
      reply("But multiple shrunk faster than ARR grew."),
      gap(),
      reply("Macro attribution: ~60% rate environment"),
      reply("AI premium:        +12x vs non-AI SaaS peers"),
    ],
  },

  "sepa-strategy": {
    prompt: "analyze NVDA using SEPA — is it a good setup?",
    lines: [
      gap(),
      thinking("Reading skill: sepa-strategy"),
      gap(),
      tool("Bash", "python3 sepa_analysis.py NVDA", 500),
      out("Running Minervini SEPA checklist..."),
      gap(),
      reply("## NVDA — SEPA Strategy Analysis"),
      gap(),
      reply("Stage: 2 (Advancing) ✓"),
      gap(),
      reply("Trend Template (8 conditions):"),
      ok("Price > 50-day MA ($132.40)"),
      ok("Price > 200-day MA ($118.60)"),
      ok("200-day MA trending up 4+ months"),
      ok("50-day MA > 200-day MA"),
      ok("Price > 52-week low by ≥30%"),
      ok("Price within 25% of 52-week high"),
      ok("RS rating ≥ 70  (current: 94)"),
      ok("Current price above 50-day MA"),
      gap(),
      reply("VCP: Base #3 forming — 28% → 14% → 6% contraction"),
      reply("Pivot: $142.80 on volume > 48M"),
      reply("Stop: $134.20 (−6.0%)  |  R/R: 3.2:1"),
    ],
  },

  "stock-liquidity": {
    prompt: "analyze TSLA liquidity profile",
    lines: [
      gap(),
      thinking("Reading skill: stock-liquidity"),
      gap(),
      tool("Bash", "python3 liquidity.py TSLA", 400),
      out("Analyzing bid-ask spreads, volume, and depth..."),
      gap(),
      reply("## TSLA — Liquidity Profile"),
      gap(),
      reply("Avg Daily Volume:    128.4M shares"),
      reply("Bid-Ask Spread:      $0.01 (0.004%)"),
      reply("Amihud Illiquidity:  0.0021 (highly liquid)"),
      gap(),
      reply("Turnover Ratio:      4.1% daily"),
      reply("Market Impact (1M shares): ~$0.12 (0.05%)"),
      gap(),
      reply("Verdict: Extremely liquid — minimal slippage risk."),
    ],
  },

  "finance-sentiment": {
    prompt: "cross-source sentiment for AAPL",
    lines: [
      gap(),
      thinking("Reading skill: finance-sentiment"),
      gap(),
      tool("Bash", "curl -s 'api.adanos.ai/v1/sentiment?symbol=AAPL'", 400),
      out("Fetching cross-source sentiment via Adanos API..."),
      gap(),
      reply("## AAPL — Multi-Source Sentiment"),
      gap(),
      reply("Source        Buzz    Bullish%  Mentions  Trend"),
      reply("Reddit        High    74%       2,841     ↑"),
      reply("X.com         Med     68%       1,422     →"),
      reply("News          High    81%       384       ↑"),
      reply("Polymarket    —       72%       —         ↑"),
      gap(),
      reply("Composite score: 73% bullish (above 30d avg of 65%)"),
    ],
  },
};

// ---------------------------------------------------------------------------
// Build terminal tabs for a skill
// ---------------------------------------------------------------------------

function buildSkillTabs(skill: Skill): TabContent[] {
  const session = mockSessions[skill.name];

  if (session) {
    return [
      {
        label: "example",
        command: `claude "${session.prompt}"`,
        lines: session.lines,
      },
    ];
  }

  return [
    {
      label: "example",
      command: `claude "use ${skill.name}"`,
      lines: [
        gap(),
        thinking(`Reading skill: ${skill.name}`),
        gap(),
        reply(skill.description),
        gap(),
        { text: "  ✓ Done", color: c.green, delay: 300 },
      ],
    },
  ];
}
