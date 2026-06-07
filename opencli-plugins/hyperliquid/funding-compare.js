/**
 * hyperliquid funding-compare — cross-venue predicted funding via
 * `predictedFundings`, pivoted to one row per coin with each venue's APR and
 * the HL-vs-venue spread. A funding-arb screen.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { normalizePredictedFundings } from './lib/funding.js';

const SORT_FIELDS = ['hlVsBinancePct', 'hlVsBybitPct', 'hlAprPct', 'binanceAprPct', 'bybitAprPct', 'coin'];

cli({
  site: 'hyperliquid',
  name: 'funding-compare',
  description: 'Cross-venue predicted funding (HL vs Binance vs Bybit), annualized, with spreads — funding-arb screen',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'coin', help: 'Filter to one coin (e.g. BTC). Omit for all.' },
    { name: 'sort', default: 'hlVsBinancePct', choices: SORT_FIELDS, help: 'Sort field (by absolute value desc, except coin = asc)' },
    { name: 'limit', type: 'int', help: 'Max rows after sort (omit for all)' },
  ],
  columns: ['coin', 'hlAprPct', 'binanceAprPct', 'bybitAprPct', 'hlVsBinancePct', 'hlVsBybitPct', 'nextHlFunding'],
  func: async (args) => {
    const data = await infoFetch({ type: 'predictedFundings' });
    let rows = normalizePredictedFundings(data, args.coin);
    if (args.coin && rows.length === 0) {
      throw new Error(`No predicted funding for coin "${args.coin}".`);
    }

    const sortKey = String(args.sort || 'hlVsBinancePct');
    if (sortKey === 'coin') {
      rows.sort((a, b) => String(a.coin).localeCompare(String(b.coin)));
    } else {
      // Spread fields rank by magnitude; raw APR fields rank signed-desc.
      const byMagnitude = sortKey.startsWith('hlVs');
      rows.sort((a, b) => {
        const av = a[sortKey];
        const bv = b[sortKey];
        const ak = av == null ? -Infinity : byMagnitude ? Math.abs(av) : av;
        const bk = bv == null ? -Infinity : byMagnitude ? Math.abs(bv) : bv;
        return bk - ak;
      });
    }

    const limit = Number(args.limit);
    if (Number.isFinite(limit) && limit > 0) rows = rows.slice(0, limit);
    return rows;
  },
});
