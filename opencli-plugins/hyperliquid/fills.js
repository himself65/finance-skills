/**
 * hyperliquid fills — recent fills (trades) for a 0x address via `userFills`.
 * Up to 2000 most-recent fills; `--limit` caps the returned count. Read-only.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch, normalizeAddress } from './lib/api.js';
import { normalizeFills } from './lib/orders.js';

cli({
  site: 'hyperliquid',
  name: 'fills',
  description: 'Recent fills/trades for an address (coin, dir, price, size, closed PnL, fee)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'user', required: true, help: 'Account 0x address (40 hex chars)' },
    { name: 'coin', help: 'Filter to one coin (e.g. BTC)' },
    { name: 'limit', type: 'int', default: 50, help: 'Max fills to return (default 50, API max 2000)' },
  ],
  columns: ['coin', 'dir', 'side', 'px', 'sz', 'notional', 'closedPnl', 'fee', 'feeToken', 'crossed', 'time', 'hash'],
  func: async (args) => {
    const user = normalizeAddress(args.user);
    const fills = await infoFetch({ type: 'userFills', user });
    let rows = normalizeFills(fills); // newest-first as returned
    if (args.coin) {
      const c = String(args.coin).toUpperCase().trim();
      rows = rows.filter((r) => String(r.coin).toUpperCase() === c);
    }
    const limit = Number(args.limit);
    if (Number.isFinite(limit) && limit > 0) rows = rows.slice(0, limit);
    return rows;
  },
});
