/**
 * tradingview watchlists — read-only access to user's watchlists.
 *
 *   default                  → list all custom watchlists (id + name + count)
 *   --id <id>                → fetch one custom watchlist's symbols
 *   --color <flag-color>     → fetch a colored-flag list (red, orange, yellow,
 *                              green, blue, purple)
 *
 * Auth: cookies harvested via CDP. READ-ONLY: append/replace endpoints are
 * not exposed.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { tradingViewFetch } from './lib/cookies.js';

const API_BASE = 'https://www.tradingview.com/api/v1/symbols_list';
const VALID_COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple'];

cli({
  site: 'tradingview',
  name: 'watchlists',
  description: 'TradingView watchlists (read-only): list all, fetch by id, or fetch colored-flag list',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'id', help: 'Watchlist id (numeric or 8-char alphanumeric). When set, returns symbols of that watchlist.' },
    {
      name: 'color',
      choices: VALID_COLORS,
      help: 'Colored-flag list to fetch (red, orange, yellow, green, blue, purple)',
    },
  ],
  columns: ['id', 'name', 'symbol_count', 'symbols'],
  func: async (args) => {
    if (args.id && args.color) {
      throw new Error('--id and --color are mutually exclusive');
    }
    if (args.id) {
      const payload = await getJson(`${API_BASE}/custom/${encodeURIComponent(String(args.id))}/`);
      return [normalizeOne(payload, args.id)];
    }
    if (args.color) {
      const color = String(args.color).toLowerCase();
      if (!VALID_COLORS.includes(color)) {
        throw new Error(`--color must be one of: ${VALID_COLORS.join(', ')}`);
      }
      const payload = await getJson(`${API_BASE}/colored/${color}/`);
      return [normalizeOne(payload, color, `colored:${color}`)];
    }

    const payload = await getJson(`${API_BASE}/all/`);
    const lists = pickListArray(payload);
    return lists.map((wl) => normalizeOne(wl, wl.id, wl.name));
  },
});

function pickListArray(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.results)) return payload.results;
  if (Array.isArray(payload?.lists)) return payload.lists;
  if (Array.isArray(payload?.items)) return payload.items;
  return [];
}

function normalizeOne(payload, idFallback = '', nameFallback = '') {
  const symbols = Array.isArray(payload?.symbols) ? payload.symbols : [];
  return {
    id: payload?.id ?? idFallback,
    name: payload?.name ?? nameFallback,
    symbol_count: symbols.length,
    symbols: symbols.join(','),
  };
}

async function getJson(url) {
  const res = await tradingViewFetch(url);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`watchlists ${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}
