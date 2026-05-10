/**
 * tradingview search — symbol/instrument autocomplete via symbol-search.tradingview.com.
 *
 *   GET https://symbol-search.tradingview.com/symbol_search/v3/?text=<q>&...
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { tradingViewFetch } from './lib/cookies.js';

const SEARCH_BASE = 'https://symbol-search.tradingview.com/symbol_search/v3/';

const VALID_TYPES = [
  'stock', 'funds', 'index', 'futures', 'forex', 'crypto', 'bond', 'economic',
  'dr', 'cfd', 'option', 'structured',
];

cli({
  site: 'tradingview',
  name: 'search',
  description: 'Symbol search / autocomplete (returns ticker, exchange, type, country, description)',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'query', required: true, help: 'Search text (e.g. "AAPL", "apple", "BINANCE:BTC")' },
    {
      name: 'type',
      choices: VALID_TYPES,
      help: 'Filter to one asset type. Omit for all.',
    },
    { name: 'exchange', help: 'Filter to one exchange (NASDAQ, NYSE, BINANCE, OANDA, ...)' },
    { name: 'country', help: 'Filter to ISO-2 country code (US, GB, JP, ...)' },
    { name: 'lang', default: 'en', help: 'Language (default en)' },
    { name: 'limit', type: 'int', default: 20, help: 'Max results (default 20)' },
    { name: 'offset', type: 'int', default: 0, help: 'Pagination start' },
  ],
  columns: ['symbol', 'description', 'type', 'exchange', 'country', 'currency'],
  func: async (_page, args) => {
    const params = new URLSearchParams();
    params.set('text', String(args.query));
    params.set('hl', '1');
    params.set('lang', String(args.lang || 'en'));
    params.set('search_type', String(args.type || ''));
    params.set('domain', 'production');
    params.set('start', String(Math.max(0, Number(args.offset) || 0)));
    if (args.exchange) params.set('exchange', String(args.exchange));
    if (args.country) {
      params.set('country', String(args.country));
      params.set('sort_by_country', String(args.country));
    }

    const res = await tradingViewFetch(`${SEARCH_BASE}?${params.toString()}`);
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`search ${res.status}: ${text.slice(0, 200)}`);
    }
    const payload = await res.json();
    const symbols = Array.isArray(payload?.symbols) ? payload.symbols : [];
    const limit = Math.max(1, Number(args.limit) || 20);
    return symbols.slice(0, limit).map(normalizeSearchHit);
  },
});

function normalizeSearchHit(item) {
  const exchange = item.exchange ?? item.prefix ?? '';
  const sym = stripHl(item.symbol ?? '');
  return {
    symbol: exchange && sym ? `${exchange}:${sym}` : sym,
    description: stripHl(item.description ?? ''),
    type: item.type ?? '',
    exchange,
    country: item.country ?? '',
    currency: item.currency_code ?? item.currency ?? '',
  };
}

/** TradingView wraps query matches in <em> tags when hl=1. Strip them for plain output. */
function stripHl(s) {
  return String(s).replace(/<\/?em>/g, '');
}
