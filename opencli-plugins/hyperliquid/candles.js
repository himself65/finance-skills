/**
 * hyperliquid candles — OHLCV history via `candleSnapshot`.
 * Pulls the most recent `--limit` candles of `--interval` for a coin.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { infoFetch } from './lib/api.js';
import { INTERVAL_MS, normalizeCandles } from './lib/candles.js';

const INTERVALS = Object.keys(INTERVAL_MS);

cli({
  site: 'hyperliquid',
  name: 'candles',
  description: 'OHLCV candles for a coin (most recent N of a given interval)',
  access: 'read',
  strategy: Strategy.PUBLIC,
  browser: false,
  args: [
    { name: 'coin', required: true, help: 'Coin or spot pair (e.g. BTC, PURR/USDC)' },
    { name: 'interval', default: '1h', choices: INTERVALS, help: 'Candle interval (default 1h)' },
    { name: 'limit', type: 'int', default: 100, help: 'Number of most-recent candles (default 100, max 5000)' },
  ],
  columns: ['time', 'open', 'high', 'low', 'close', 'volume', 'trades'],
  func: async (args) => {
    const coin = String(args.coin).trim();
    const interval = String(args.interval);
    const stepMs = INTERVAL_MS[interval];
    if (!stepMs) throw new Error(`Unsupported interval "${interval}". One of: ${INTERVALS.join(', ')}`);

    const limit = Math.min(Math.max(1, Number(args.limit) || 100), 5000);
    const endTime = Date.now();
    const startTime = endTime - stepMs * limit;

    const rows = await infoFetch({
      type: 'candleSnapshot',
      req: { coin, interval, startTime, endTime },
    });
    const out = normalizeCandles(rows);
    if (out.length === 0) {
      throw new Error(`No candles returned for "${coin}" @ ${interval} — check the coin/pair symbol.`);
    }
    return out.slice(-limit);
  },
});
