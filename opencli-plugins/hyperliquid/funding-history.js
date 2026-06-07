/**
 * hyperliquid funding-history — historical hourly funding for a coin via
 * `fundingHistory`. Returns prints from now back `--hours` hours.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { normalizeFundingHistory } from './lib/funding.js';

const HOUR_MS = 3_600_000;

cli({
  site: 'hyperliquid',
  name: 'funding-history',
  description: 'Historical hourly funding rates (+ APR, premium) for a coin',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'coin', required: true, help: 'Coin (e.g. BTC)' },
    { name: 'hours', type: 'int', default: 24, help: 'Lookback window in hours (default 24)' },
    { name: 'limit', type: 'int', help: 'Cap rows to the most recent N (omit for all in window)' },
  ],
  columns: ['coin', 'fundingRatePct', 'fundingAprPct', 'premiumPct', 'time'],
  func: async (args) => {
    const coin = String(args.coin).toUpperCase().trim();
    const hours = Math.max(1, Number(args.hours) || 24);
    const startTime = Date.now() - hours * HOUR_MS;

    const rows = await infoFetch({ type: 'fundingHistory', coin, startTime });
    let out = normalizeFundingHistory(rows);
    out.sort((a, b) => String(b.time).localeCompare(String(a.time))); // newest first

    const limit = Number(args.limit);
    if (Number.isFinite(limit) && limit > 0) out = out.slice(0, limit);
    return out;
  },
});
