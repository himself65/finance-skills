/**
 * tradingview screenshot — PNG of a chart tab via CDP Page.captureScreenshot.
 */

import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve as resolvePath } from 'node:path';
import { homedir } from 'node:os';
import { cli, Strategy } from '@jackwener/opencli/registry';
import { pickTab, screenshotTab } from './lib/cdp.js';

cli({
  site: 'tradingview',
  name: 'screenshot',
  description: 'PNG screenshot of an active TradingView chart tab',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'tab', help: 'Tab id (from `opencli tradingview status`). Default: first chart tab.' },
    { name: 'output', help: 'Output PNG path (default: ~/tradingview-<timestamp>.png)' },
  ],
  columns: ['path', 'bytes', 'tab_id'],
  func: async (args) => {
    const tab = await pickTab(args.tab);
    const outPath = resolveOutputPath(args.output);
    const png = await screenshotTab(tab);
    const dir = dirname(outPath);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    writeFileSync(outPath, png);
    return [{ path: outPath, bytes: png.length, tab_id: tab.id }];
  },
});

function resolveOutputPath(arg) {
  if (arg) return resolvePath(String(arg).replace(/^~/, homedir()));
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  return resolvePath(homedir(), `tradingview-${stamp}.png`);
}
