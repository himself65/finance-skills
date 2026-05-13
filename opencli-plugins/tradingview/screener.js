/**
 * tradingview screener — generic stock/crypto/forex/futures/bond screener.
 *
 * Backed by `scanner.tradingview.com/{market}/scan2`. Supports the full
 * scan2 grammar: column timeframe suffixes (RSI|60), filter clauses, sort,
 * and pagination. ~3,000 stock fields available; see TradingView field
 * catalogs for the per-market list.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { buildScreenerBody, decodeScannerRows, scannerFetch } from './lib/scanner.js';

const DEFAULT_COLUMNS = 'name,close,change,volume,market_cap_basic,sector.tr';
const DEFAULT_LIMIT = 50;

cli({
  site: 'tradingview',
  name: 'screener',
  description:
    'Generic screener via scanner.tradingview.com — stocks (per country), crypto, forex, futures, bonds, ETFs',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    {
      name: 'market',
      default: 'america',
      help: 'Market path segment: america, global, crypto, coin, forex, futures, bond, cfd, economics2, or any country code (uk, india, japan, ...)',
    },
    {
      name: 'columns',
      default: DEFAULT_COLUMNS,
      help: 'Comma-separated column list. Append |TF for timeframe (e.g. "RSI|60" for 1h RSI). Default: ' + DEFAULT_COLUMNS,
    },
    {
      name: 'filter',
      help:
        'JSON array of clauses. Each: {"left":"<field>","operation":"<op>","right":<value>}. ' +
        'Operations: equal,nequal,greater,egreater,less,eless,in_range,not_in_range,empty,nempty,match,nmatch,crosses,crosses_above,crosses_below,above%,below%',
    },
    {
      name: 'sort',
      default: 'volume:desc',
      help: 'Field:asc/desc, e.g. market_cap_basic:desc',
    },
    {
      name: 'tickers',
      help: 'Comma-separated explicit tickers (EXCH:SYM). Bypasses filter when set.',
    },
    {
      name: 'label-product',
      default: 'screener-stock',
      help: 'Server-side analytics label. Common: screener-stock, screener-crypto, screener-forex.',
    },
    { name: 'limit', type: 'int', default: DEFAULT_LIMIT, help: `Max rows (clamped 1..500, default ${DEFAULT_LIMIT})` },
    { name: 'offset', type: 'int', default: 0, help: 'Pagination offset' },
  ],
  columns: ['symbol', 'name', 'close', 'change', 'volume', 'market_cap_basic', 'sector.tr'],
  func: async (_page, args) => {
    const market = String(args.market).toLowerCase().trim();
    const columns = String(args.columns).split(',').map((c) => c.trim()).filter(Boolean);
    if (columns.length === 0) {
      throw new Error('--columns must be a non-empty comma-separated list');
    }

    const filter = parseJsonArg(args.filter, '--filter');
    const sort = parseSortArg(args.sort);
    const tickers = args.tickers
      ? String(args.tickers).split(',').map((t) => t.trim()).filter(Boolean)
      : undefined;

    const body = buildScreenerBody({
      market,
      columns,
      filter,
      sort,
      tickers,
      limit: Number(args.limit) || DEFAULT_LIMIT,
      offset: Number(args.offset) || 0,
    });

    const payload = await scannerFetch(`${encodeURIComponent(market)}/scan2`, body, {
      labelProduct: String(args['label-product'] || 'screener-stock'),
    });
    return decodeScannerRows(payload);
  },
});

function parseJsonArg(value, label) {
  if (!value) return undefined;
  try {
    return JSON.parse(String(value));
  } catch (err) {
    throw new Error(`${label} must be valid JSON: ${err instanceof Error ? err.message : String(err)}`);
  }
}

function parseSortArg(value) {
  if (!value) return undefined;
  const [field, order] = String(value).split(':');
  if (!field) return undefined;
  const normalized = (order || 'desc').toLowerCase();
  if (normalized !== 'asc' && normalized !== 'desc') {
    throw new Error(`--sort order must be 'asc' or 'desc', got: ${order}`);
  }
  return { sortBy: field, sortOrder: normalized };
}
