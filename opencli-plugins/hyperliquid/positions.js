/**
 * hyperliquid positions — open perp positions for a 0x address via
 * `clearinghouseState`. One row per position. Public, read-only.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch, normalizeAddress } from './lib/api.js';
import { normalizePositions } from './lib/account.js';

cli({
  site: 'hyperliquid',
  name: 'positions',
  description: 'Open perp positions for an address (side, size, entry, uPnL, ROE, leverage, liq price)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'user', required: true, help: 'Account 0x address (40 hex chars)' },
    { name: 'coin', help: 'Filter to one coin (e.g. BTC)' },
  ],
  columns: ['coin', 'side', 'size', 'entryPx', 'positionValue', 'unrealizedPnl', 'roePct', 'leverage', 'leverageType', 'liquidationPx', 'marginUsed', 'fundingSinceOpen'],
  func: async (args) => {
    const user = normalizeAddress(args.user);
    const state = await infoFetch({ type: 'clearinghouseState', user });
    let rows = normalizePositions(state);
    if (args.coin) {
      const c = String(args.coin).toUpperCase().trim();
      rows = rows.filter((r) => String(r.coin).toUpperCase() === c);
    }
    return rows;
  },
});
