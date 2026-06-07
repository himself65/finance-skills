/**
 * hyperliquid markets — perpetual markets table via `metaAndAssetCtxs`.
 * Mark/oracle price, 24h change, funding (hourly + annualized), open interest,
 * and 24h notional volume for every listed perp.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { normalizePerpMarkets } from './lib/markets.js';

const SORT_FIELDS = ['dayNtlVlm', 'change24hPct', 'fundingAprPct', 'fundingHrPct', 'openInterest', 'oiNotional', 'markPx', 'coin'];

cli({
  site: 'hyperliquid',
  name: 'markets',
  description: 'Perpetual markets — mark/oracle price, 24h change, funding (hourly + APR), open interest, 24h volume',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'coin', help: 'Filter to one coin (e.g. BTC). Omit for all perps.' },
    { name: 'sort', default: 'dayNtlVlm', choices: SORT_FIELDS, help: 'Sort field (desc, except coin = asc)' },
    { name: 'limit', type: 'int', help: 'Max rows after sort (omit for all)' },
    { name: 'include-delisted', type: 'boolean', default: false, help: 'Include delisted markets' },
  ],
  columns: ['coin', 'markPx', 'midPx', 'oraclePx', 'change24hPct', 'fundingHrPct', 'fundingAprPct', 'openInterest', 'oiNotional', 'dayNtlVlm', 'premiumPct', 'maxLeverage'],
  func: async (args) => {
    const [meta, ctxs] = await infoFetch({ type: 'metaAndAssetCtxs' });
    let rows = normalizePerpMarkets(meta, ctxs);
    if (!args['include-delisted']) rows = rows.filter((r) => !r.delisted);

    if (args.coin) {
      const c = String(args.coin).toUpperCase().trim();
      rows = rows.filter((r) => r.coin.toUpperCase() === c);
      if (rows.length === 0) throw new Error(`No perp market for coin "${args.coin}" — check the symbol.`);
    }

    const sortKey = String(args.sort || 'dayNtlVlm');
    if (sortKey === 'coin') {
      rows.sort((a, b) => String(a.coin).localeCompare(String(b.coin)));
    } else {
      rows.sort((a, b) => (b[sortKey] ?? -Infinity) - (a[sortKey] ?? -Infinity));
    }

    const limit = Number(args.limit);
    if (Number.isFinite(limit) && limit > 0) rows = rows.slice(0, limit);

    // Drop internal-only fields from the emitted rows.
    return rows.map(({ delisted, prevDayPx, ...rest }) => rest);
  },
});
