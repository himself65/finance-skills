/**
 * hyperliquid account — perp account margin summary for a 0x address via
 * `clearinghouseState`. Single row: account value, notional, margin used,
 * withdrawable, open-position count. Public, read-only.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch, normalizeAddress } from './lib/api.js';
import { normalizeMarginSummary } from './lib/account.js';

cli({
  site: 'hyperliquid',
  name: 'account',
  description: 'Perp account margin summary for an address (value, notional, margin used, withdrawable)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'user', required: true, help: 'Account 0x address (40 hex chars)' },
  ],
  columns: ['accountValue', 'totalNtlPos', 'totalRawUsd', 'totalMarginUsed', 'crossAccountValue', 'crossMaintenanceMarginUsed', 'withdrawable', 'numPositions', 'time'],
  func: async (args) => {
    const user = normalizeAddress(args.user);
    const state = await infoFetch({ type: 'clearinghouseState', user });
    return normalizeMarginSummary(state);
  },
});
