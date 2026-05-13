/**
 * tradingview news — TradingView news feed and story detail.
 *
 * Two modes:
 *   - List mode (default): GET /v2/headlines with filter args
 *   - Story mode (--id <story-id>): GET /v2/story, returns single row with flattened body text
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import {
  astToText,
  epochToIso,
  fetchHeadlines,
  fetchStory,
  normalizeHeadline,
} from './lib/news.js';

cli({
  site: 'tradingview',
  name: 'news',
  description: 'TradingView news headlines (filterable) or full story detail by id',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'id', help: 'Story id — when set, fetch full story instead of list' },
    { name: 'symbol', help: 'EXCH:SYM filter (omit for global feed)' },
    {
      name: 'category',
      choices: ['base', 'stock', 'etf', 'futures', 'forex', 'crypto', 'index', 'bond', 'economic'],
      help: 'Top-level category. Default: base (global)',
    },
    {
      name: 'area',
      choices: ['WLD', 'AME', 'EUR', 'ASI', 'OCN', 'AFR'],
      help: 'Geographic area filter',
    },
    {
      name: 'section',
      help: 'Section: press_release, financial_statement, insider_trading, esg, corp_activity, analysis, recommendation, prediction, markets_today, survey',
    },
    { name: 'provider', help: 'Filter to a single source (e.g. reuters, dow_jones, cointelegraph)' },
    { name: 'lang', default: 'en', help: 'Language (default en)' },
    { name: 'limit', type: 'int', default: 25, help: 'Max headlines (default 25)' },
  ],
  columns: ['id', 'published', 'provider', 'title', 'urgency', 'related_symbols', 'link'],
  func: async (_page, args) => {
    if (args.id) {
      return [await fetchStoryRow(args)];
    }
    return fetchHeadlinesRows(args);
  },
});

async function fetchHeadlinesRows(args) {
  const payload = await fetchHeadlines({
    symbol: args.symbol,
    category: args.category,
    area: args.area,
    section: args.section,
    provider: args.provider,
    lang: args.lang,
  });
  const items = Array.isArray(payload?.items) ? payload.items : [];
  const limit = Math.max(1, Number(args.limit) || 25);
  return items.slice(0, limit).map((it) => normalizeHeadline(it));
}

async function fetchStoryRow(args) {
  const story = await fetchStory(String(args.id), args.lang || 'en');
  const body = astToText(story?.astDescription).replace(/\n{3,}/g, '\n\n').trim();
  return {
    id: story?.id ?? args.id,
    published: epochToIso(story?.published),
    provider: story?.provider ?? story?.source ?? '',
    title: story?.title ?? '',
    body,
    tags: Array.isArray(story?.tags) ? story.tags.map((t) => t?.title ?? t).filter(Boolean).join(', ') : '',
    link: story?.link ?? (story?.storyPath ? `https://www.tradingview.com${story.storyPath}` : ''),
  };
}
