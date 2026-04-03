import { Suspense } from "react";
import dynamic from "next/dynamic";
import { skills } from "@/data/skills";

const SkillList = dynamic(() => import("./skill-list").then((mod) => mod.SkillList));

async function getStarCount(): Promise<number | null> {
  try {
    const res = await fetch("https://api.github.com/repos/himself65/finance-skills", {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data.stargazers_count ?? null;
  } catch {
    return null;
  }
}

export default async function Home() {
  const stars = await getStarCount();
  return (
    <div className="min-h-screen">
      {/* Nav */}
      <nav className="border-b border-border px-6 py-3" style={{ viewTransitionName: "site-nav" }}>
        <div className="max-w-3xl mx-auto flex items-center gap-2 text-sm">
          <span className="font-semibold">Finance Skills</span>
        </div>
      </nav>

      <main className="max-w-3xl mx-auto px-6" style={{ viewTransitionName: "page-content" }}>
        {/* Header */}
        <div className="py-10">
          <p className="text-sm text-text-muted mb-2">
            <span>skills</span>
            <span className="mx-1.5">/</span>
            <span className="text-text-secondary">himself65</span>
            <span className="mx-1.5">/</span>
            <span className="text-text-secondary">finance-skills</span>
          </p>
          <h1 className="text-3xl font-bold tracking-tight text-balance">
            himself65/finance-skills
          </h1>
          <p className="mt-3 text-text-secondary leading-relaxed max-w-xl">
            Agent skills for financial analysis and trading. Earnings reports,
            market data, options strategies, risk monitoring, and sentiment
            analysis — installable into Claude Code, Claude.ai, and other
            AI agents.
          </p>
          <div className="flex items-center gap-4 mt-4 text-sm text-text-secondary">
            <span>{skills.length} skills</span>
            <a
              href="https://github.com/himself65/finance-skills"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 hover:text-text transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent rounded"
            >
              <svg className="w-4 h-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
              </svg>
              {stars !== null && (
                <span>
                  <svg className="w-3.5 h-3.5 inline -mt-px" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                    <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25z" />
                  </svg>
                  {" "}{stars.toLocaleString()}
                </span>
              )}
            </a>
          </div>
        </div>

        {/* Usage */}
        <div className="pb-8 space-y-4">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-text-muted">
            Usage
          </h2>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-text-muted mb-1.5">Install as a plugin (recommended)</p>
              <div className="inline-flex items-center gap-2 bg-bg-elevated border border-border rounded-lg px-4 py-2.5 font-mono text-sm text-text-secondary">
                <span className="text-text-muted">$</span>
                <span>npx plugins add himself65/finance-skills</span>
              </div>
            </div>
            <div>
              <p className="text-xs text-text-muted mb-1.5">Install all skills</p>
              <div className="inline-flex items-center gap-2 bg-bg-elevated border border-border rounded-lg px-4 py-2.5 font-mono text-sm text-text-secondary">
                <span className="text-text-muted">$</span>
                <span>npx skills add himself65/finance-skills</span>
              </div>
            </div>
            <div>
              <p className="text-xs text-text-muted mb-1.5">Install a single skill</p>
              <div className="inline-flex items-center gap-2 bg-bg-elevated border border-border rounded-lg px-4 py-2.5 font-mono text-sm text-text-secondary">
                <span className="text-text-muted">$</span>
                <span>npx skills add himself65/finance-skills --skill earnings-preview</span>
              </div>
            </div>
          </div>
        </div>

        {/* Skills by category with filter */}
        <div className="border-t border-border pt-6">
          <Suspense>
            <SkillList skills={skills} />
          </Suspense>
        </div>
      </main>
    </div>
  );
}
