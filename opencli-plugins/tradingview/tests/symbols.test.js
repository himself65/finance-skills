import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseOpraSymbol, expirationToIso, daysToExpiry, buildTvSymbol } from '../lib/symbols.js';

test('parseOpraSymbol — call', () => {
  const parsed = parseOpraSymbol('OPRA:SNDK260522C2090.0');
  assert.deepEqual(parsed, { root: 'SNDK', expiry: '2026-05-22', type: 'call', strike: 2090 });
});

test('parseOpraSymbol — put', () => {
  const parsed = parseOpraSymbol('OPRA:AAPL260619P185.0');
  assert.deepEqual(parsed, { root: 'AAPL', expiry: '2026-06-19', type: 'put', strike: 185 });
});

test('parseOpraSymbol — fractional strike', () => {
  const parsed = parseOpraSymbol('OPRA:SPY260515C595.5');
  assert.equal(parsed.strike, 595.5);
});

test('parseOpraSymbol — rejects malformed input', () => {
  assert.throws(() => parseOpraSymbol('AAPL'));
  assert.throws(() => parseOpraSymbol('OPRA:AAPL2606XX185.0'));
});

test('expirationToIso — integer YYYYMMDD', () => {
  assert.equal(expirationToIso(20260522), '2026-05-22');
  assert.equal(expirationToIso('20260101'), '2026-01-01');
});

test('expirationToIso — rejects bad input', () => {
  assert.throws(() => expirationToIso(202605));
  assert.throws(() => expirationToIso('not-a-date'));
});

test('daysToExpiry — future', () => {
  const now = new Date('2026-05-10T12:00:00Z');
  assert.equal(daysToExpiry('2026-05-22', now), 12);
});

test('daysToExpiry — past', () => {
  const now = new Date('2026-05-10T12:00:00Z');
  assert.equal(daysToExpiry('2026-05-01', now), -9);
});

test('buildTvSymbol — uppercase + colon', () => {
  assert.equal(buildTvSymbol('nasdaq', 'aapl'), 'NASDAQ:AAPL');
  assert.equal(buildTvSymbol('NYSEARCA', 'spy'), 'NYSEARCA:SPY');
});
