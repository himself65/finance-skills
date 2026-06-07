/**
 * hyperliquid book — L2 order book snapshot via `l2Book`.
 * Up to `--depth` levels per side; bids first, then asks.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { normalizeBook } from './lib/book.js';

cli({
  site: 'hyperliquid',
  name: 'book',
  description: 'L2 order book snapshot (top N levels per side) for a coin',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'coin', required: true, help: 'Coin or spot pair (e.g. BTC, PURR/USDC)' },
    { name: 'depth', type: 'int', default: 10, help: 'Levels per side (1-20, default 10)' },
    { name: 'n-sig-figs', type: 'int', help: 'Price aggregation significant figures (2-5). Omit for full precision.' },
  ],
  columns: ['side', 'level', 'px', 'sz', 'orders'],
  func: async (args) => {
    const coin = String(args.coin).trim();
    const body = { type: 'l2Book', coin };
    const nSigFigs = Number(args['n-sig-figs']);
    if (Number.isFinite(nSigFigs)) body.nSigFigs = nSigFigs;

    const payload = await infoFetch(body);
    const rows = normalizeBook(payload, args.depth);
    if (rows.length === 0) {
      throw new Error(`No order book returned for "${coin}" — check the coin/pair symbol.`);
    }
    return rows;
  },
});
