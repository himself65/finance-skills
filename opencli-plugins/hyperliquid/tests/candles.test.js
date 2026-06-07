import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeCandles, INTERVAL_MS } from '../lib/candles.js';

// Shape captured live from candleSnapshot.
const CANDLES = [
  { t: 1780804800000, T: 1780808399999, s: 'BTC', i: '1h', o: '61685.0', c: '61871.0', h: '61888.0', l: '61463.0', v: '1376.39573', n: 18040 },
  { t: 1780808400000, T: 1780811999999, s: 'BTC', i: '1h', o: '61871.0', c: '61721.0', h: '62130.0', l: '61630.0', v: '1733.82548', n: 24641 },
];

test('normalizeCandles — OHLCV with ISO open time', () => {
  const rows = normalizeCandles(CANDLES);
  assert.equal(rows.length, 2);
  const c = rows[0];
  assert.equal(c.time, new Date(1780804800000).toISOString());
  assert.equal(c.open, 61685);
  assert.equal(c.high, 61888);
  assert.equal(c.low, 61463);
  assert.equal(c.close, 61871);
  assert.equal(c.volume, 1376.39573);
  assert.equal(c.trades, 18040);
});

test('normalizeCandles — empty input', () => {
  assert.deepEqual(normalizeCandles([]), []);
  assert.deepEqual(normalizeCandles(null), []);
});

test('INTERVAL_MS — covers the documented set, consistent math', () => {
  assert.equal(INTERVAL_MS['1h'], 3_600_000);
  assert.equal(INTERVAL_MS['1d'], 24 * INTERVAL_MS['1h']);
  assert.equal(INTERVAL_MS['1w'], 7 * INTERVAL_MS['1d']);
  assert.equal(INTERVAL_MS['15m'], 15 * INTERVAL_MS['1m']);
  assert.ok(Object.keys(INTERVAL_MS).includes('1M'));
});
