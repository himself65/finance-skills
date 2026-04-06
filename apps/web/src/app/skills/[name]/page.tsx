import { skills, getSkill, categoryLabels } from "@/data/skills";
import { notFound } from "next/navigation";
import { Link } from "next-view-transitions";

export function generateStaticParams() {
  return skills.map((s) => ({ name: s.name }));
}

const platformLabel: Record<string, string> = {
  cli: "CLI",
  "claude-ai": "Claude.ai",
  both: "All Platforms",
};

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

        {/* Install commands */}
        <div className="flex flex-wrap gap-2 mb-8">
          <div className="inline-flex items-center gap-2 bg-bg-elevated border border-border rounded-lg px-3 py-2 font-mono text-xs text-text-secondary">
            <span className="text-text-muted">$</span>
            npx plugins add himself65/finance-skills
          </div>
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
                    href={`/?category=${skill.category}`}
                    scroll={false}
                    className="text-xs border border-border rounded px-2 py-0.5 text-text-secondary hover:border-accent hover:text-accent transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
                  >
                    {categoryLabels[skill.category]}
                  </Link>
                  {skill.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-xs border border-border rounded px-2 py-0.5 text-text-secondary"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                {/* Example usage */}
                <div className="mt-6 pt-4 border-t border-border">
                  <h3 className="text-sm font-semibold mb-3">Example</h3>
                  <div className="bg-bg rounded-lg border border-border p-4 font-mono text-sm">
                    <div>
                      <span className="text-green">$</span>
                      <span className="text-text-secondary">
                        {" "}
                        claude &quot;{getExamplePrompt(skill.name)}&quot;
                      </span>
                    </div>
                    <div className="text-text-muted mt-2">
                      [skill:{skill.name}] activated
                    </div>
                    <div className="text-text-muted mt-1">
                      {getExampleOutput(skill.name)}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:w-56 shrink-0 space-y-6">
            <div>
              <p className="text-xs uppercase tracking-wider text-text-muted mb-1.5">
                Platform
              </p>
              <p className="text-sm">{platformLabel[skill.platform]}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wider text-text-muted mb-1.5">
                Category
              </p>
              <Link
                href={`/?category=${skill.category}`}
                scroll={false}
                className="text-sm text-accent hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded"
              >
                {categoryLabels[skill.category]}
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
                <p>npx plugins add himself65/finance-skills</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function getExamplePrompt(name: string): string {
  const prompts: Record<string, string> = {
    "earnings-preview": "earnings preview for NVDA",
    "earnings-recap": "how did AAPL earnings go",
    "estimate-analysis": "estimate revisions for TSLA",
    "yfinance-data": "get MSFT financials",
    "funda-data": "NVDA options flow",
    "options-payoff": "show payoff for AAPL 200/210 call spread",
    "stock-correlation": "what correlates with NVDA",
    "hormuz-strait": "Hormuz strait status",
    "generative-ui": "visualize AAPL revenue trend",
    "twitter-reader": "search Twitter for NVDA sentiment",
    "telegram-reader": "read my crypto Telegram channels",
    "discord-reader": "search Discord for AAPL discussion",
    "linkedin-reader": "what are analysts saying on LinkedIn about NVDA",
    "yc-reader": "show me YC fintech companies that are hiring",
    "startup-analysis": "analyze LangChain as a potential investment",
    "saas-valuation-compression": "analyze Vercel valuation compression from Series D to E",
  };
  return prompts[name] || `use ${name}`;
}

function getExampleOutput(name: string): string {
  const outputs: Record<string, string> = {
    "earnings-preview":
      "Fetching consensus estimates, beat/miss history, and analyst sentiment for NVDA...",
    "earnings-recap":
      "Analyzing AAPL Q1 results: EPS $2.18 vs $2.10 est (+3.8% surprise)...",
    "estimate-analysis":
      "Loading estimate revision trends for TSLA across 4 periods...",
    "yfinance-data":
      "Downloading MSFT income statement, balance sheet, and cash flow...",
    "funda-data": "Fetching NVDA options flow data from Funda AI API...",
    "options-payoff":
      "Generating interactive payoff chart for AAPL 200/210 bull call spread...",
    "stock-correlation":
      "Computing 90-day rolling correlations for NVDA against sector peers...",
    "hormuz-strait":
      "Fetching real-time transit data from Hormuz Strait Monitor...",
    "generative-ui": "Rendering interactive revenue chart widget for AAPL...",
    "twitter-reader":
      "Searching recent tweets for NVDA sentiment via opencli...",
    "telegram-reader": "Listing subscribed Telegram channels via tdl...",
    "discord-reader":
      "Searching AAPL mentions in connected Discord servers...",
    "linkedin-reader":
      "Reading LinkedIn feed for NVDA analyst commentary via opencli...",
    "yc-reader":
      "Fetching YC fintech companies from yc-oss API and filtering for hiring...",
    "startup-analysis":
      "Researching LangChain — gathering funding data, team info, market position for 3-perspective analysis...",
    "saas-valuation-compression":
      "Searching Vercel funding rounds, ARR estimates, and macro SaaS multiples — computing compression metrics...",
  };
  return outputs[name] || "Processing...";
}
