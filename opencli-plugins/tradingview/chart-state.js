/**
 * tradingview chart-state — current symbol/interval/layout of an active chart tab.
 *
 * Reads the chart URL via CDP Runtime.evaluate. Layout id lives in the URL
 * (/chart/<layout_id>/...); symbol and interval are read from page metadata.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { evaluateOnTab, pickTab } from './lib/cdp.js';

cli({
  site: 'tradingview',
  name: 'chart-state',
  description: 'Current symbol, interval, and layout id of an active chart tab',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'tab', help: 'Tab id (from `opencli tradingview status`). Default: first chart tab.' },
  ],
  columns: ['layout_id', 'symbol', 'interval', 'url', 'tab_id'],
  func: async (_page, args) => {
    const tab = await pickTab(args.tab);

    const url = String(await evaluateOnTab(tab, 'window.location.href'));
    const layoutMatch = url.match(/\/chart\/([\w-]+)\//);
    const layoutId = layoutMatch ? layoutMatch[1] : null;

    const state = await evaluateOnTab(
      tab,
      `(() => {
        // Symbol — try multiple selectors. TradingView's chart UI iterates fast,
        // so this is a best-effort cascade with common known anchors.
        const symbolSelectors = [
          '#header-toolbar-symbol-search div',
          '[data-name="legend-source-title"]',
          '[class*="mainTitle"]',
          '[data-symbol-short]',
        ];
        let symbol = '';
        for (const sel of symbolSelectors) {
          const el = document.querySelector(sel);
          const text = (el?.dataset?.symbolShort || el?.textContent || '').trim();
          if (text && /^[A-Z0-9._:-]+$/i.test(text)) { symbol = text; break; }
        }
        // Interval — resolution button text
        const intervalEl = document.querySelector(
          '[data-name="resolution-button"] [class*="value"], #header-toolbar-intervals button[aria-pressed="true"]'
        );
        const interval = intervalEl ? intervalEl.textContent.trim() : '';
        return { symbol, interval };
      })()`,
    );

    return [{
      layout_id: layoutId,
      symbol: String(state?.symbol ?? ''),
      interval: String(state?.interval ?? ''),
      url,
      tab_id: tab.id,
    }];
  },
});
