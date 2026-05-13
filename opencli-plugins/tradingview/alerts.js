/**
 * tradingview alerts — read-only access to pricealerts.tradingview.com.
 *
 * One command, multiple modes via --type:
 *   list      → /list_alerts          all alerts (active + paused)
 *   active    → /get_active_alerts    currently armed
 *   triggered → /get_triggered_alerts recently fired
 *   offline   → /get_offline_fires    fired while user was offline
 *   log       → /get_log              full historical fire log
 *
 * Auth: cookies harvested via CDP. READ-ONLY: write endpoints (create_alert,
 * edit_alert, remove_alert, restart_alert) are intentionally NOT exposed.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { tradingViewFetch } from './lib/cookies.js';
import { normalizeAlerts } from './lib/alerts.js';

const ALERTS_BASE = 'https://pricealerts.tradingview.com';

const ENDPOINTS = {
  list: '/list_alerts',
  active: '/get_active_alerts',
  triggered: '/get_triggered_alerts',
  offline: '/get_offline_fires',
  log: '/get_log',
};

cli({
  site: 'tradingview',
  name: 'alerts',
  description: 'TradingView price alerts (read-only): list, active, triggered, offline-fires, log',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    {
      name: 'type',
      default: 'list',
      choices: ['list', 'active', 'triggered', 'offline', 'log'],
      help: 'Which alert view to fetch (default: list)',
    },
  ],
  columns: ['id', 'name', 'symbol', 'type', 'condition', 'value', 'active', 'status', 'fired_at'],
  func: async (args) => {
    const which = String(args.type || 'list').toLowerCase();
    const path = ENDPOINTS[which];
    if (!path) throw new Error(`Unknown alerts --type: ${which}. One of: ${Object.keys(ENDPOINTS).join(', ')}`);

    const res = await tradingViewFetch(`${ALERTS_BASE}${path}`);
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`alerts ${res.status}: ${text.slice(0, 200)}`);
    }
    const payload = await res.json();
    return normalizeAlerts(payload);
  },
});
