/**
 * hyperliquid open-orders — resting orders for a 0x address via
 * `frontendOpenOrders` (includes order type + trigger detail). Read-only.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch, normalizeAddress } from './lib/api.js';
import { normalizeOpenOrders } from './lib/orders.js';

cli({
  site: 'hyperliquid',
  name: 'open-orders',
  description: 'Resting open orders for an address (coin, side, type, price, size, TIF, trigger)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'user', required: true, help: 'Account 0x address (40 hex chars)' },
    { name: 'coin', help: 'Filter to one coin (e.g. BTC)' },
  ],
  columns: ['coin', 'side', 'orderType', 'limitPx', 'sz', 'origSz', 'oid', 'tif', 'reduceOnly', 'triggerCondition', 'triggerPx', 'time'],
  func: async (args) => {
    const user = normalizeAddress(args.user);
    const orders = await infoFetch({ type: 'frontendOpenOrders', user });
    let rows = normalizeOpenOrders(orders);
    if (args.coin) {
      const c = String(args.coin).toUpperCase().trim();
      rows = rows.filter((r) => String(r.coin).toUpperCase() === c);
    }
    return rows;
  },
});
