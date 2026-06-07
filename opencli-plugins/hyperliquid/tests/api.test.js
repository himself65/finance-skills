import { test } from 'node:test';
import assert from 'node:assert/strict';
import { num, pctChange, fundingToApr, normalizeAddress, isoTime } from '../lib/api.js';

test('num — coerces numeric strings, else null', () => {
  assert.equal(num('61791.0'), 61791);
  assert.equal(num(42), 42);
  assert.equal(num(0), 0);
  assert.equal(num(null), null);
  assert.equal(num(undefined), null);
  assert.equal(num('not-a-number'), null);
});

test('pctChange — basic + guards', () => {
  assert.equal(pctChange(110, 100), 10);
  assert.equal(pctChange('61791.0', '61001.0').toFixed(4), '1.2951');
  assert.equal(pctChange(100, 0), null);
  assert.equal(pctChange(null, 100), null);
  assert.equal(pctChange(100, null), null);
});

test('fundingToApr — hourly and multi-hour intervals', () => {
  // 0.0000125 hourly → 0.0000125 * 24 * 365 * 100 = 10.95% APR
  assert.equal(fundingToApr('0.0000125', 1).toFixed(4), '10.9500');
  // Same rate over a 4h interval annualizes to a quarter of the hourly figure.
  assert.equal(fundingToApr('0.0000125', 4).toFixed(5), '2.73750');
  assert.equal(fundingToApr(null), null);
  // Missing/zero interval defaults to hourly.
  assert.equal(fundingToApr('0.0000125', 0).toFixed(4), '10.9500');
  assert.equal(fundingToApr('0.0000125').toFixed(4), '10.9500');
});

test('normalizeAddress — validates + lowercases', () => {
  assert.equal(
    normalizeAddress('0x31CA8395CF837DE08B24DA3F660E77761DFB974B'),
    '0x31ca8395cf837de08b24da3f660e77761dfb974b',
  );
  assert.throws(() => normalizeAddress('0x123'), /40-hex/);
  assert.throws(() => normalizeAddress('31ca8395cf837de08b24da3f660e77761dfb974b'), /0x-prefixed/);
  assert.throws(() => normalizeAddress(''), /0x-prefixed/);
});

test('isoTime — ms epoch → ISO, null-safe', () => {
  assert.equal(isoTime(1780813166432), '2026-06-07T06:19:26.432Z');
  assert.equal(isoTime(null), null);
  assert.equal(isoTime('not-a-number'), null);
});
