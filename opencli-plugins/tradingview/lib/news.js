/**
 * News helpers for news-headlines.tradingview.com/v2/*.
 *
 * Two endpoints:
 *   GET /v2/headlines  — paginated headline list with filtering
 *   GET /v2/story?id=… — full story (returns AST in `astDescription`)
 */

import { tradingViewFetch } from './cookies.js';

const NEWS_BASE = 'https://news-headlines.tradingview.com/v2';

/**
 * Build the query string for the headlines endpoint.
 * @param {object} opts
 * @param {string} [opts.symbol]    EXCH:SYM (optional — omit for global feed)
 * @param {string} [opts.category]  base|stock|etf|futures|forex|crypto|index|bond|economic
 * @param {string} [opts.area]      WLD|AME|EUR|ASI|OCN|AFR
 * @param {string} [opts.section]   press_release|financial_statement|insider_trading|esg|...
 * @param {string} [opts.provider]  reuters|dow_jones|cointelegraph|...
 * @param {string} [opts.lang]      default 'en'
 */
export function buildHeadlinesUrl(opts = {}) {
  const params = new URLSearchParams();
  params.set('client', 'web');
  params.set('lang', opts.lang ?? 'en');
  params.set('streaming', 'false');
  if (opts.category) params.set('category', String(opts.category));
  if (opts.area) params.set('area', String(opts.area));
  if (opts.section) params.set('section', String(opts.section));
  if (opts.symbol) params.set('symbol', String(opts.symbol));
  if (opts.provider) params.set('provider', String(opts.provider));
  return `${NEWS_BASE}/headlines?${params.toString()}`;
}

/**
 * Build the query URL for a single story.
 * @param {string} storyId
 * @param {string} [lang]
 */
export function buildStoryUrl(storyId, lang = 'en') {
  const params = new URLSearchParams({ id: String(storyId), lang });
  return `${NEWS_BASE}/story?${params.toString()}`;
}

/**
 * Normalize a headlines item to a flat row.
 */
export function normalizeHeadline(item, opts = {}) {
  const limitSyms = opts.limitRelatedSymbols ?? 6;
  const related = Array.isArray(item.relatedSymbols)
    ? item.relatedSymbols
        .slice(0, limitSyms)
        .map((s) => (typeof s === 'string' ? s : s?.symbol ?? ''))
        .filter(Boolean)
        .join(',')
    : '';
  const link = item.link
    ? String(item.link)
    : item.storyPath
    ? `https://www.tradingview.com${item.storyPath}`
    : '';
  return {
    id: item.id ?? null,
    published: epochToIso(item.published),
    provider: item.source ?? item.provider ?? '',
    title: item.title ?? '',
    urgency: item.urgency ?? null,
    related_symbols: related,
    link,
  };
}

/**
 * Walk TradingView's news AST and produce plain text. Adds line breaks
 * between block-level elements; ignores attributes other than text content.
 *
 * Node shapes seen in the wild:
 *   { type: 'text',  value: '...' }
 *   { type: 'p',     children: [...] }
 *   { type: 'h2',    children: [...] }
 *   { type: 'a',     href: '...',   children: [...] }
 *   { type: 'br' }
 *   { type: 'list-item' | 'list', children: [...] }
 */
export function astToText(node) {
  if (node == null) return '';
  if (typeof node === 'string') return node;
  if (Array.isArray(node)) return node.map(astToText).join('');
  if (typeof node === 'object') {
    if (node.value != null && (!node.children || node.children.length === 0)) {
      return String(node.value);
    }
    if (node.text != null && (!node.children || node.children.length === 0)) {
      return String(node.text);
    }
    const inner = node.children ? astToText(node.children) : '';
    const type = String(node.type || '').toLowerCase();
    if (type === 'br') return '\n';
    if (type === 'p' || type === 'paragraph') return inner + '\n\n';
    if (type === 'h1' || type === 'h2' || type === 'h3' || type === 'h4') {
      return `\n${inner}\n\n`;
    }
    if (type === 'list-item') return `- ${inner}\n`;
    if (type === 'list') return inner + '\n';
    return inner;
  }
  return String(node);
}

/**
 * Convert epoch seconds OR milliseconds to ISO string. Returns '' for falsy
 * inputs (including 0 — there's no realistic news from 1970).
 */
export function epochToIso(value) {
  if (value == null || value === '' || value === 0) return '';
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) return '';
  // Heuristic: > 1e12 = milliseconds, otherwise seconds.
  const ms = n > 1e12 ? n : n * 1000;
  return new Date(ms).toISOString();
}

/**
 * Fetch the headlines feed.
 * @param {Parameters<typeof buildHeadlinesUrl>[0]} opts
 */
export async function fetchHeadlines(opts) {
  const url = buildHeadlinesUrl(opts);
  const res = await tradingViewFetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`news headlines ${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}

/**
 * Fetch a single story.
 */
export async function fetchStory(storyId, lang = 'en') {
  const url = buildStoryUrl(storyId, lang);
  const res = await tradingViewFetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`news story ${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}

export { NEWS_BASE };
