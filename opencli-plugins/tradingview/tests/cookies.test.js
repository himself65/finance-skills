import { test } from 'node:test';
import assert from 'node:assert/strict';
import { TV_HEADERS, getCdpEndpoint } from '../lib/cookies.js';

test('TV_HEADERS — has Origin, Referer, User-Agent', () => {
  assert.equal(TV_HEADERS.Origin, 'https://www.tradingview.com');
  assert.equal(TV_HEADERS.Referer, 'https://www.tradingview.com/');
  assert.match(TV_HEADERS['User-Agent'], /TradingView/);
  assert.match(TV_HEADERS['User-Agent'], /TVDesktop/);
});

test('getCdpEndpoint — defaults to 127.0.0.1:9222', () => {
  const before = process.env.OPENCLI_CDP_ENDPOINT;
  delete process.env.OPENCLI_CDP_ENDPOINT;
  try {
    assert.equal(getCdpEndpoint(), 'http://127.0.0.1:9222');
  } finally {
    if (before !== undefined) process.env.OPENCLI_CDP_ENDPOINT = before;
  }
});

test('getCdpEndpoint — honors OPENCLI_CDP_ENDPOINT env var', () => {
  const before = process.env.OPENCLI_CDP_ENDPOINT;
  process.env.OPENCLI_CDP_ENDPOINT = 'http://127.0.0.1:9333';
  try {
    assert.equal(getCdpEndpoint(), 'http://127.0.0.1:9333');
  } finally {
    if (before === undefined) delete process.env.OPENCLI_CDP_ENDPOINT;
    else process.env.OPENCLI_CDP_ENDPOINT = before;
  }
});

test('getCdpEndpoint — strips trailing slash', () => {
  const before = process.env.OPENCLI_CDP_ENDPOINT;
  process.env.OPENCLI_CDP_ENDPOINT = 'http://127.0.0.1:9222/';
  try {
    assert.equal(getCdpEndpoint(), 'http://127.0.0.1:9222');
  } finally {
    if (before === undefined) delete process.env.OPENCLI_CDP_ENDPOINT;
    else process.env.OPENCLI_CDP_ENDPOINT = before;
  }
});
