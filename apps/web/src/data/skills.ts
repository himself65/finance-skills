export type SkillCategory =
  | "analysis"
  | "data"
  | "risk"
  | "sentiment"
  | "strategy"
  | "visualization";

export type PluginGroup =
  | "market-analysis"
  | "social-readers"
  | "data-providers"
  | "startup-tools"
  | "ui-tools";

export type SkillBadge = "new" | "paid";

export interface Skill {
  name: string;
  title: string;
  description: string;
  category: SkillCategory;
  plugin: PluginGroup;

  tags: string[];
  badge?: SkillBadge;
}

export const categoryLabels: Record<SkillCategory, string> = {
  analysis: "Analysis",
  data: "Market Data",
  risk: "Risk",
  sentiment: "Sentiment",
  strategy: "Trading Strategy",
  visualization: "Visualization",
};

export const pluginGroupLabels: Record<PluginGroup, string> = {
  "market-analysis": "Market Analysis",
  "social-readers": "Social Readers",
  "data-providers": "Data Providers",
  "startup-tools": "Startup Tools",
  "ui-tools": "UI Tools",
};

export const skills: Skill[] = [
  {
    name: "earnings-preview",
    title: "Earnings Preview",
    description:
      "Generate a pre-earnings briefing for any stock — consensus estimates, beat/miss track record, and analyst sentiment overview.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["Predictive", "EPS"],
  },
  {
    name: "earnings-recap",
    title: "Earnings Recap",
    description:
      "Post-earnings analysis covering actual vs estimated numbers, surprise magnitude, stock price reaction, and financial context.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["Post-Earnings", "Reaction"],
  },
  {
    name: "estimate-analysis",
    title: "Estimate Analysis",
    description:
      "Deep-dive into analyst estimate revisions, EPS/revenue distributions, and growth projections across periods.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["Revisions", "Trends"],
  },
  {
    name: "etf-premium",
    title: "ETF Premium/Discount",
    description:
      "Calculate ETF premium or discount vs NAV — single ETF snapshots, peer comparisons, and cross-category screener for 90+ ETFs.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["ETF", "NAV", "Screener"],
    badge: "new",
  },
  {
    name: "yfinance-data",
    title: "yfinance Data",
    description:
      "Fetch stock prices, financials, options chains, dividends, earnings, and analyst data from Yahoo Finance via yfinance.",
    category: "data",
    plugin: "market-analysis",
    tags: ["Market Data", "Fundamentals"],
  },
  {
    name: "funda-data",
    title: "Funda Data",
    description:
      "Funda AI API for quotes, fundamentals, SEC filings, options flow/GEX, supply chain, sentiment, congressional trades, and more.",
    category: "data",
    plugin: "data-providers",
    tags: ["API", "Options Flow"],
    badge: "paid",
  },
  {
    name: "options-payoff",
    title: "Options Payoff",
    description:
      "Interactive payoff curve charts with dynamic sliders for any options strategy — spreads, straddles, condors, butterflies.",
    category: "visualization",
    plugin: "market-analysis",
    tags: ["Interactive", "Black-Scholes"],
  },
  {
    name: "stock-correlation",
    title: "Stock Correlation",
    description:
      "Find correlated stocks, sector peers, and trading pairs with rolling correlation and co-movement analysis.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["Correlation", "Pairs"],
  },
  {
    name: "stock-liquidity",
    title: "Stock Liquidity",
    description:
      "Analyze stock liquidity — bid-ask spreads, volume profiles, order book depth, market impact estimates, Amihud illiquidity ratio, and turnover ratios.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["Liquidity", "Spreads", "Volume"],
    badge: "new",
  },
  {
    name: "startup-analysis",
    title: "Startup Analysis",
    description:
      "Multi-perspective startup analysis — evaluate any company from VC investor, job applicant, and CEO/founder viewpoints with detailed frameworks.",
    category: "analysis",
    plugin: "startup-tools",
    tags: ["Startups", "Due Diligence"],
    badge: "new",
  },
  {
    name: "hormuz-strait",
    title: "Hormuz Strait Monitor",
    description:
      "Real-time Strait of Hormuz status — shipping transits, oil prices, stranded vessels, insurance risk, and diplomatic developments.",
    category: "risk",
    plugin: "data-providers",
    tags: ["Geopolitical", "Oil"],
  },
  {
    name: "generative-ui",
    title: "Generative UI",
    description:
      "Design system for Claude's show_widget tool — render interactive HTML/SVG widgets inline in claude.ai conversations.",
    category: "visualization",
    plugin: "ui-tools",
    tags: ["Widgets", "Design System"],
  },
  {
    name: "twitter-reader",
    title: "Twitter Reader",
    description:
      "Read-only Twitter/X access for financial research — search tweets, view bookmarks, and gather market sentiment.",
    category: "sentiment",
    plugin: "social-readers",
    tags: ["Social"],
  },
  {
    name: "telegram-reader",
    title: "Telegram Reader",
    description:
      "Read-only Telegram channel access for financial news — export messages, search channels, monitor market intelligence.",
    category: "sentiment",
    plugin: "social-readers",
    tags: ["Social"],
  },
  {
    name: "discord-reader",
    title: "Discord Reader",
    description:
      "Read-only Discord access for financial research — trading servers, crypto channels, and community sentiment.",
    category: "sentiment",
    plugin: "social-readers",
    tags: ["Social"],
  },
  {
    name: "linkedin-reader",
    title: "LinkedIn Reader",
    description:
      "Read-only LinkedIn access for financial research — professional market commentary, analyst posts, and finance job search.",
    category: "sentiment",
    plugin: "social-readers",
    tags: ["Social", "Jobs"],
    badge: "new",
  },
  {
    name: "yc-reader",
    title: "YC Reader",
    description:
      "Y Combinator company data — browse batches, filter by industry/tag, track hiring, and research the YC startup ecosystem.",
    category: "data",
    plugin: "social-readers",
    tags: ["YC", "Startups"],
    badge: "new",
  },
  {
    name: "opencli-reader",
    title: "opencli Reader",
    description:
      "Generic read-only fallback for 90+ opencli adapters — Yahoo Finance, Bloomberg, Reuters, Eastmoney, Xueqiu, Reddit, HackerNews, Substack, arXiv, and more.",
    category: "sentiment",
    plugin: "social-readers",
    tags: ["Fallback", "Multi-Source"],
    badge: "new",
  },
  {
    name: "finance-sentiment",
    title: "Finance Sentiment",
    description:
      "Structured stock sentiment research — compare Reddit, X.com, news, and Polymarket using buzz, bullish %, mentions, and trend via the Adanos Finance API.",
    category: "data",
    plugin: "data-providers",
    tags: ["Cross-Source", "API"],
    badge: "paid",
  },
  {
    name: "sepa-strategy",
    title: "SEPA Strategy",
    description:
      "Mark Minervini's SEPA strategy analysis — trend template, VCP patterns, precise entry points, position sizing, and risk management for growth stocks.",
    category: "strategy",
    plugin: "market-analysis",
    tags: ["Minervini", "VCP", "Swing Trading"],
    badge: "new",
  },
  {
    name: "saas-valuation-compression",
    title: "SaaS Valuation Compression",
    description:
      "Analyze round-to-round valuation compression for SaaS companies — ARR multiples, macro attribution, AI narrative premium, and peer comparisons with inline visualizations.",
    category: "analysis",
    plugin: "market-analysis",
    tags: ["SaaS", "Valuation", "VC"],
    badge: "new",
  },
];

export function getSkill(name: string): Skill | undefined {
  return skills.find((s) => s.name === name);
}
