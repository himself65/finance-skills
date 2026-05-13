/**
 * tradingview quote — single-symbol spot quote via scanner.tradingview.com.
 *
 * Cookies are harvested via CDP (see lib/cookies.js) and the POST is fired
 * from Node directly — page-context fetch is rejected by browser CORS.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { buildQuoteBody, decodeScannerRows, scannerFetch } from './lib/scanner.js';

cli({
  site: 'tradingview',
  name: 'quote',
  description: 'Single-symbol spot quote (close, change, currency)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'ticker', required: true, help: 'Symbol (e.g. AAPL)' },
    { name: 'exchange', default: 'NASDAQ', help: 'TradingView exchange code (NASDAQ, NYSE, NYSEARCA, ...)' },
  ],
  columns: ['symbol', 'description', 'close', 'change', 'change_abs', 'currency', 'time'],
  func: async (_page, args) => {
    const ticker = String(args.ticker).toUpperCase().trim();
    const exchange = String(args.exchange).toUpperCase().trim();

    const body = buildQuoteBody(exchange, ticker);
    const payload = await scannerFetch('global/scan2', body);
    const rows = decodeScannerRows(payload);

    if (rows.length === 0) {
      throw new Error(`No quote returned for ${exchange}:${ticker} — verify the exchange.`);
    }
    const row = rows[0];
    return [{
      symbol: row.symbol,
      description: row.description ?? null,
      close: numericOrNull(row.close),
      change: numericOrNull(row.change),
      change_abs: numericOrNull(row.change_abs),
      currency: row.currency ?? null,
      time: payload?.time ?? null,
    }];
  },
});

function numericOrNull(v) {
  if (v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
