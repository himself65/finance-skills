/**
 * tradingview status — CDP connection state + active TradingView tabs.
 *
 * Hits /json on the CDP endpoint (resolved via OPENCLI_CDP_ENDPOINT, falling back
 * to http://127.0.0.1:9222) and filters returned targets to TradingView pages.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';

const DEFAULT_ENDPOINT = 'http://127.0.0.1:9222';

cli({
  site: 'tradingview',
  name: 'status',
  description: 'CDP connection state and active TradingView tabs',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [],
  columns: ['connected', 'tabs'],
  func: async () => {
    const endpoint = (process.env.OPENCLI_CDP_ENDPOINT || DEFAULT_ENDPOINT).replace(/\/$/, '');
    let targets;
    try {
      const res = await fetch(`${endpoint}/json`);
      if (!res.ok) {
        return [{ connected: false, tabs: [], endpoint, error: `HTTP ${res.status}` }];
      }
      targets = await res.json();
    } catch (err) {
      return [{ connected: false, tabs: [], endpoint, error: errorMessage(err) }];
    }

    const tabs = (Array.isArray(targets) ? targets : [])
      .filter((t) => t.type === 'page' && isTradingViewUrl(t.url))
      .map((t) => ({
        id: t.id,
        type: classifyTab(t.url),
        url: t.url,
        title: t.title,
      }));

    return [{ connected: true, tabs, endpoint }];
  },
});

function isTradingViewUrl(url) {
  if (typeof url !== 'string') return false;
  if (!url.startsWith('https://www.tradingview.com/')) return false;
  if (url.includes('app.asar')) return false;
  return true;
}

function classifyTab(url) {
  if (url.includes('/chart/')) return 'chart';
  if (url.includes('/symbols/') && url.includes('/options-chain/')) return 'options';
  if (url.includes('/symbols/')) return 'symbol';
  return 'other';
}

function errorMessage(err) {
  if (err && typeof err === 'object' && 'message' in err) return String(err.message);
  return String(err);
}
