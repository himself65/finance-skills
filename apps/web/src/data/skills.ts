export type SkillCategory =
  | "analysis"
  | "data"
  | "risk"
  | "sentiment"
  | "visualization";

export type SkillBadge = "new" | "paid";

export interface Skill {
  name: string;
  title: string;
  description: string;
  category: SkillCategory;
  platform: "cli" | "claude-ai" | "both";
  tags: string[];
  badge?: SkillBadge;
}

export const categoryLabels: Record<SkillCategory, string> = {
  analysis: "Analysis",
  data: "Market Data",
  risk: "Risk",
  sentiment: "Sentiment",
  visualization: "Visualization",
};

export const skills: Skill[] = [
  {
    name: "earnings-preview",
    title: "Earnings Preview",
    description:
      "Generate a pre-earnings briefing for any stock — consensus estimates, beat/miss track record, and analyst sentiment overview.",
    category: "analysis",
    platform: "cli",
    tags: ["Predictive", "EPS"],
    badge: "new",
  },
  {
    name: "earnings-recap",
    title: "Earnings Recap",
    description:
      "Post-earnings analysis covering actual vs estimated numbers, surprise magnitude, stock price reaction, and financial context.",
    category: "analysis",
    platform: "cli",
    tags: ["Post-Earnings", "Reaction"],
    badge: "new",
  },
  {
    name: "estimate-analysis",
    title: "Estimate Analysis",
    description:
      "Deep-dive into analyst estimate revisions, EPS/revenue distributions, and growth projections across periods.",
    category: "analysis",
    platform: "cli",
    tags: ["Revisions", "Trends"],
    badge: "new",
  },
  {
    name: "yfinance-data",
    title: "yfinance Data",
    description:
      "Fetch stock prices, financials, options chains, dividends, earnings, and analyst data from Yahoo Finance via yfinance.",
    category: "data",
    platform: "cli",
    tags: ["Market Data", "Fundamentals"],
  },
  {
    name: "funda-data",
    title: "Funda Data",
    description:
      "Funda AI API for quotes, fundamentals, SEC filings, options flow/GEX, supply chain, sentiment, congressional trades, and more.",
    category: "data",
    platform: "cli",
    tags: ["API", "Options Flow"],
    badge: "paid",
  },
  {
    name: "options-payoff",
    title: "Options Payoff",
    description:
      "Interactive payoff curve charts with dynamic sliders for any options strategy — spreads, straddles, condors, butterflies.",
    category: "visualization",
    platform: "both",
    tags: ["Interactive", "Black-Scholes"],
  },
  {
    name: "stock-correlation",
    title: "Stock Correlation",
    description:
      "Find correlated stocks, sector peers, and trading pairs with rolling correlation and co-movement analysis.",
    category: "analysis",
    platform: "cli",
    tags: ["Correlation", "Pairs"],
  },
  {
    name: "hormuz-strait",
    title: "Hormuz Strait Monitor",
    description:
      "Real-time Strait of Hormuz status — shipping transits, oil prices, stranded vessels, insurance risk, and diplomatic developments.",
    category: "risk",
    platform: "cli",
    tags: ["Geopolitical", "Oil"],
  },
  {
    name: "generative-ui",
    title: "Generative UI",
    description:
      "Design system for Claude's show_widget tool — render interactive HTML/SVG widgets inline in claude.ai conversations.",
    category: "visualization",
    platform: "claude-ai",
    tags: ["Widgets", "Design System"],
  },
  {
    name: "twitter-reader",
    title: "Twitter Reader",
    description:
      "Read-only Twitter/X access for financial research — search tweets, view bookmarks, and gather market sentiment.",
    category: "sentiment",
    platform: "cli",
    tags: ["Social", "Read-Only"],
  },
  {
    name: "telegram-reader",
    title: "Telegram Reader",
    description:
      "Read-only Telegram channel access for financial news — export messages, search channels, monitor market intelligence.",
    category: "sentiment",
    platform: "cli",
    tags: ["Social", "Read-Only"],
  },
  {
    name: "discord-reader",
    title: "Discord Reader",
    description:
      "Read-only Discord access for financial research — trading servers, crypto channels, and community sentiment.",
    category: "sentiment",
    platform: "cli",
    tags: ["Social", "Read-Only"],
  },
  {
    name: "finance-sentiment",
    title: "Finance Sentiment",
    description:
      "Structured stock sentiment research — compare Reddit, X.com, news, and Polymarket using buzz, bullish %, mentions, and trend via the Adanos Finance API.",
    category: "data",
    platform: "cli",
    tags: ["Cross-Source", "API"],
    badge: "paid",
  },
];

export function getSkill(name: string): Skill | undefined {
  return skills.find((s) => s.name === name);
}
