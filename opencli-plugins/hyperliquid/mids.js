/**
 * hyperliquid mids — current mid price for every market via `allMids`.
 * Perp mids are keyed by coin name; spot mids by "@<index>", resolved to the
 * pair name via `spotMeta`.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { resolveMids } from './lib/markets.js';

cli({
  site: 'hyperliquid',
  name: 'mids',
  description: 'Current mid price for every perp + spot market (allMids)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'coin', help: 'Case-insensitive substring filter (e.g. BTC). Omit for all markets.' },
  ],
  columns: ['coin', 'mid'],
  func: async (args) => {
    const [allMids, spotMeta] = await Promise.all([
      infoFetch({ type: 'allMids' }),
      infoFetch({ type: 'spotMeta' }),
    ]);
    const rows = resolveMids(allMids, spotMeta, args.coin);
    if (args.coin && rows.length === 0) {
      throw new Error(`No market matching "${args.coin}".`);
    }
    rows.sort((a, b) => String(a.coin).localeCompare(String(b.coin)));
    return rows;
  },
});
