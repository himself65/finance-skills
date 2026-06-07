/**
 * hyperliquid spot-balances — spot token balances for a 0x address via
 * `spotClearinghouseState`. One row per token. Public, read-only.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch, normalizeAddress } from './lib/api.js';
import { normalizeSpotBalances } from './lib/account.js';

cli({
  site: 'hyperliquid',
  name: 'spot-balances',
  description: 'Spot token balances for an address (total, hold, available, entry notional)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'user', required: true, help: 'Account 0x address (40 hex chars)' },
  ],
  columns: ['coin', 'total', 'hold', 'available', 'entryNtl'],
  func: async (args) => {
    const user = normalizeAddress(args.user);
    const state = await infoFetch({ type: 'spotClearinghouseState', user });
    return normalizeSpotBalances(state);
  },
});
