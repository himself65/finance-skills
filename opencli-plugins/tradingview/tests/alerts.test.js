import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeAlerts } from '../lib/alerts.js';

test('normalizeAlerts — live shape: { s: "ok", r: [...] }', () => {
  // Captured from live pricealerts.tradingview.com/list_alerts
  const payload = {
    s: 'ok',
    id: 'kh76-65262949',
    r: [
      {
        id: 12345,
        name: 'KORU dip',
        symbol: '={"symbol":"AMEX:KORU","adjustment":"splits","session":"extended","currency-id":"USD"}',
        resolution: '1',
        condition: { type: 'cross_down', params: [10.5] },
        active: true,
        status: 'active',
      },
      {
        id: 67890,
        name: '',
        symbol: 'NASDAQ:NVDA',
        condition: { type: 'cross_up', value: 200 },
        active: false,
        status: 'paused',
      },
    ],
  };

  const rows = normalizeAlerts(payload);
  assert.equal(rows.length, 2);

  // First row: AMEX:KORU extracted from JSON-encoded symbol blob
  assert.equal(rows[0].id, 12345);
  assert.equal(rows[0].name, 'KORU dip');
  assert.equal(rows[0].symbol, 'AMEX:KORU');
  assert.equal(rows[0].condition, 'cross_down');
  assert.equal(rows[0].value, 10.5);
  assert.equal(rows[0].active, true);
  assert.equal(rows[0].status, 'active');

  // Second row: plain symbol, condition.value extracted
  assert.equal(rows[1].symbol, 'NASDAQ:NVDA');
  assert.equal(rows[1].condition, 'cross_up');
  assert.equal(rows[1].value, 200);
  assert.equal(rows[1].active, false);
});

test('normalizeAlerts — fallback to alerts/items/data array keys', () => {
  // Older shapes from community docs
  assert.equal(normalizeAlerts({ alerts: [{ id: 1 }] }).length, 1);
  assert.equal(normalizeAlerts({ items: [{ id: 2 }] }).length, 1);
  assert.equal(normalizeAlerts({ data: [{ id: 3 }] }).length, 1);
  assert.equal(normalizeAlerts({}).length, 0);
  assert.equal(normalizeAlerts(null).length, 0);
});

test('normalizeAlerts — handles bare array payload', () => {
  const rows = normalizeAlerts([{ id: 'a', symbol: 'NASDAQ:AAPL' }]);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].symbol, 'NASDAQ:AAPL');
});
