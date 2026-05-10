import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  buildChainBody,
  buildQuoteBody,
  decodeScannerRows,
  normalizeChainRow,
  strikesAroundSpot,
  summarizeExpiries,
} from '../lib/scanner.js';

const SAMPLE_PAYLOAD = {
  totalCount: 2,
  fields: [
    'ask', 'bid', 'currency', 'delta', 'expiration', 'gamma', 'iv',
    'option-type', 'pricescale', 'rho', 'root', 'strike', 'theoPrice',
    'theta', 'vega', 'bid_iv', 'ask_iv',
  ],
  symbols: [
    {
      s: 'OPRA:SNDK260522C2090.0',
      f: [18.4, 12.9, 'USD', 0.1035, 20260522, 0.000542, 1.0953,
          'call', 10, 0.0552, 'SNDK', 2090, 15, -2.177, 0.5456, 1.0546, 1.1540],
    },
    {
      s: 'OPRA:SNDK260522P2090.0',
      f: [9.5, 6.2, 'USD', -0.42, 20260522, 0.00031, 1.07,
          'put', 10, -0.04, 'SNDK', 2090, 7.85, -1.93, 0.51, 1.04, 1.10],
    },
  ],
  time: '2026-05-10T07:40:28Z',
};

const NOW = new Date('2026-05-10T00:00:00Z');

test('decodeScannerRows — maps fields[] positions to row dicts', () => {
  const rows = decodeScannerRows(SAMPLE_PAYLOAD);
  assert.equal(rows.length, 2);
  assert.equal(rows[0].symbol, 'OPRA:SNDK260522C2090.0');
  assert.equal(rows[0]['option-type'], 'call');
  assert.equal(rows[0].strike, 2090);
  assert.equal(rows[0].expiration, 20260522);
});

test('normalizeChainRow — converts to user schema with mid + dte', () => {
  const raw = decodeScannerRows(SAMPLE_PAYLOAD)[0];
  const row = normalizeChainRow(raw, NOW);
  assert.equal(row.expiry, '2026-05-22');
  assert.equal(row.dte, 12);
  assert.equal(row.type, 'call');
  assert.equal(row.bid, 12.9);
  assert.equal(row.ask, 18.4);
  assert.equal(row.mid, (12.9 + 18.4) / 2);
  assert.equal(row.symbol, 'OPRA:SNDK260522C2090.0');
});

test('normalizeChainRow — handles missing bid/ask', () => {
  const raw = { 'option-type': 'call', expiration: 20260522, strike: 100, bid: null, ask: 5 };
  const row = normalizeChainRow(raw, NOW);
  assert.equal(row.bid, null);
  assert.equal(row.ask, 5);
  assert.equal(row.mid, null);
});

test('strikesAroundSpot — symmetric band of 2N+1 per (expiry × type)', () => {
  const expiry = '2026-05-22';
  const baseRow = { expiry, dte: 12, type: 'call', bid: 1, ask: 2, mid: 1.5,
                    iv: 1, delta: 0, gamma: 0, theta: 0, vega: 0, rho: 0,
                    theo: 0, bid_iv: 1, ask_iv: 1, symbol: 'X' };
  const rows = [];
  for (let strike = 50; strike <= 150; strike += 10) {
    rows.push({ ...baseRow, strike });
    rows.push({ ...baseRow, strike, type: 'put' });
  }
  // Spot 100, halfBand 3 → expect strikes 70..130 (7 strikes) per type
  const filtered = strikesAroundSpot(rows, 100, 3);
  const callStrikes = filtered.filter((r) => r.type === 'call').map((r) => r.strike).sort((a, b) => a - b);
  assert.deepEqual(callStrikes, [70, 80, 90, 100, 110, 120, 130]);
});

test('strikesAroundSpot — halfBand 0 = passthrough', () => {
  const rows = [{ expiry: '2026-05-22', type: 'call', strike: 100 }];
  assert.equal(strikesAroundSpot(rows, 100, 0).length, 1);
});

test('summarizeExpiries — aggregates contract counts per expiry', () => {
  const rows = [
    normalizeChainRow(decodeScannerRows(SAMPLE_PAYLOAD)[0], NOW),
    normalizeChainRow(decodeScannerRows(SAMPLE_PAYLOAD)[1], NOW),
  ];
  const summary = summarizeExpiries(rows);
  assert.equal(summary.length, 1);
  assert.equal(summary[0].expiry, '2026-05-22');
  assert.equal(summary[0].dte, 12);
  assert.equal(summary[0].contracts_count, 2);
});

test('buildQuoteBody — tickers + columns shape', () => {
  const body = buildQuoteBody('NASDAQ', 'MU');
  assert.deepEqual(body.symbols.tickers, ['NASDAQ:MU']);
  assert.ok(Array.isArray(body.columns));
  assert.ok(body.columns.includes('close'));
  assert.ok(body.columns.includes('description'));
});

test('buildChainBody — uses index_filters + filter2 (NOT markets/range)', () => {
  // This shape was reverse-engineered from the live request the TradingView
  // options-chain page sends. Critical that we don't regress it: the prior
  // {markets,filter,range} shape returns HTTP 400 from the real server.
  const body = buildChainBody('NASDAQ', 'MU');
  assert.deepEqual(body.index_filters, [
    { name: 'underlying_symbol', values: ['NASDAQ:MU'] },
  ]);
  assert.equal(body.filter2.operator, 'and');
  assert.equal(body.filter2.operands[0].expression.left, 'type');
  assert.equal(body.filter2.operands[0].expression.right, 'option');
  assert.equal(body.ignore_unknown_fields, false);
  assert.ok(Array.isArray(body.columns));
  // Negative assertions — make sure the bad fields aren't there
  assert.equal(body.markets, undefined);
  assert.equal(body.filter, undefined);
  assert.equal(body.range, undefined);
});
