import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildScreenerBody } from '../lib/scanner.js';

test('buildScreenerBody — minimal stock query', () => {
  const body = buildScreenerBody({
    market: 'america',
    columns: ['name', 'close', 'volume'],
    sort: { sortBy: 'volume', sortOrder: 'desc' },
    limit: 50,
  });
  assert.deepEqual(body.markets, ['america']);
  assert.deepEqual(body.columns, ['name', 'close', 'volume']);
  assert.deepEqual(body.sort, { sortBy: 'volume', sortOrder: 'desc' });
  assert.deepEqual(body.range, [0, 50]);
  assert.equal(body.options.lang, 'en');
});

test('buildScreenerBody — clamps limit to [1, 500]', () => {
  // 5000 → clamp down to 500
  assert.deepEqual(buildScreenerBody({ market: 'america', columns: ['x'], limit: 5000 }).range, [0, 500]);
  // 0 / undefined → default 50
  assert.deepEqual(buildScreenerBody({ market: 'america', columns: ['x'], limit: 0 }).range, [0, 50]);
  // negative → clamp up to 1
  assert.deepEqual(buildScreenerBody({ market: 'america', columns: ['x'], limit: -10 }).range, [0, 1]);
});

test('buildScreenerBody — offset shifts range', () => {
  const body = buildScreenerBody({ market: 'america', columns: ['x'], limit: 25, offset: 100 });
  assert.deepEqual(body.range, [100, 125]);
});

test('buildScreenerBody — explicit tickers populate symbols.tickers', () => {
  const body = buildScreenerBody({
    market: 'america',
    columns: ['close'],
    tickers: ['NASDAQ:AAPL', 'NASDAQ:MSFT'],
  });
  assert.deepEqual(body.symbols.tickers, ['NASDAQ:AAPL', 'NASDAQ:MSFT']);
  assert.deepEqual(body.symbols.query, { types: [] });
});

test('buildScreenerBody — passes through filter and filter2', () => {
  const filter = [{ left: 'market_cap_basic', operation: 'egreater', right: 1e9 }];
  const filter2 = { operator: 'and', operands: [{ expression: { left: 'sector', operation: 'equal', right: 'Technology Services' } }] };
  const body = buildScreenerBody({
    market: 'america',
    columns: ['x'],
    filter,
    filter2,
  });
  assert.deepEqual(body.filter, filter);
  assert.deepEqual(body.filter2, filter2);
});

test('buildScreenerBody — sortOrder defaults to desc', () => {
  const body = buildScreenerBody({
    market: 'america',
    columns: ['x'],
    sort: { sortBy: 'volume' },
  });
  assert.equal(body.sort.sortOrder, 'desc');
});

test('buildScreenerBody — market lowercased', () => {
  const body = buildScreenerBody({ market: 'AMERICA', columns: ['x'] });
  assert.deepEqual(body.markets, ['america']);
});
