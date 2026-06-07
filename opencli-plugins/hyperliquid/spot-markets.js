/**
 * hyperliquid spot-markets — spot pairs table via `spotMetaAndAssetCtxs`.
 * Mark/mid price, 24h change, 24h volume, circulating supply, and market cap.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { normalizeSpotMarkets } from './lib/markets.js';

const SORT_FIELDS = ['dayNtlVlm', 'change24hPct', 'marketCap', 'markPx', 'pair'];

cli({
  site: 'hyperliquid',
  name: 'spot-markets',
  description: 'Spot pairs — mark/mid price, 24h change, 24h volume, circulating supply, market cap',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'pair', help: 'Filter by pair or base token (e.g. PURR or PURR/USDC). Omit for all.' },
    { name: 'sort', default: 'dayNtlVlm', choices: SORT_FIELDS, help: 'Sort field (desc, except pair = asc)' },
    { name: 'limit', type: 'int', help: 'Max rows after sort (omit for all)' },
    { name: 'canonical-only', type: 'boolean', default: false, help: 'Only show canonical (named) pairs, hiding @index pairs' },
  ],
  columns: ['pair', 'base', 'markPx', 'midPx', 'change24hPct', 'dayNtlVlm', 'circulatingSupply', 'marketCap', 'canonical'],
  func: async (args) => {
    const [meta, ctxs] = await infoFetch({ type: 'spotMetaAndAssetCtxs' });
    let rows = normalizeSpotMarkets(meta, ctxs);

    if (args['canonical-only']) rows = rows.filter((r) => r.canonical);

    if (args.pair) {
      const q = String(args.pair).toUpperCase().trim();
      rows = rows.filter((r) => String(r.pair).toUpperCase().includes(q) || String(r.base).toUpperCase() === q);
      if (rows.length === 0) throw new Error(`No spot pair matching "${args.pair}".`);
    }

    const sortKey = String(args.sort || 'dayNtlVlm');
    if (sortKey === 'pair') {
      rows.sort((a, b) => String(a.pair).localeCompare(String(b.pair)));
    } else {
      rows.sort((a, b) => (b[sortKey] ?? -Infinity) - (a[sortKey] ?? -Infinity));
    }

    const limit = Number(args.limit);
    if (Number.isFinite(limit) && limit > 0) rows = rows.slice(0, limit);

    return rows.map(({ prevDayPx, ...rest }) => rest);
  },
});
