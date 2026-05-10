/**
 * tradingview options-expiries — list available expirations with DTE + contract count.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import {
  buildChainBody,
  decodeScannerRows,
  normalizeChainRow,
  scannerFetch,
  summarizeExpiries,
} from './lib/scanner.js';

cli({
  site: 'tradingview',
  name: 'options-expiries',
  description: 'List available options expirations with DTE and contract count',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'ticker', required: true, help: 'Underlying ticker' },
    { name: 'exchange', default: 'NASDAQ', help: 'TradingView exchange code' },
    {
      name: 'include-expired',
      type: 'boolean',
      default: false,
      help: 'Include expired (DTE < 0). Default: false',
    },
  ],
  columns: ['expiry', 'dte', 'contracts_count'],
  func: async (_page, args) => {
    const ticker = String(args.ticker).toUpperCase().trim();
    const exchange = String(args.exchange).toUpperCase().trim();
    const includeExpired = Boolean(args['include-expired']);
    const payload = await scannerFetch('options/scan2', buildChainBody(exchange, ticker));
    let rows = decodeScannerRows(payload).map((r) => normalizeChainRow(r));
    if (rows.length === 0) {
      throw new Error(`No options for ${exchange}:${ticker} — check tier or exchange.`);
    }
    if (!includeExpired) rows = rows.filter((r) => r.dte >= 0);
    return summarizeExpiries(rows);
  },
});
