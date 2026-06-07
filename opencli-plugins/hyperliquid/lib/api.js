/**
 * Hyperliquid info API helpers.
 *
 * Hyperliquid exposes a fully public, read-only POST endpoint:
 *   POST https://api.hyperliquid.xyz/info   body { "type": "...", ... }  → JSON
 *
 * No API key, no auth, no cookies — every read this plugin makes works
 * unauthenticated, including reading any address's positions/orders/fills by
 * its public 0x address. Placing trades requires wallet-signed actions on the
 * separate /exchange endpoint, which this plugin intentionally NEVER touches.
 *
 * Funding rates come back per funding interval. Hyperliquid perps fund hourly,
 * so the hourly rate annualizes as rate * 24 * 365. Other venues surfaced via
 * `predictedFundings` may fund on a different interval (commonly 4h) — always
 * normalize with the per-row interval, not a hard-coded hour.
 */

const INFO_URL = 'https://api.hyperliquid.xyz/info';

/**
 * POST a request to the Hyperliquid info endpoint and return the parsed body.
 * @param {object} body  e.g. { type: 'metaAndAssetCtxs' }
 */
export async function infoFetch(body) {
  const res = await fetch(INFO_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`hyperliquid info ${res.status}: ${text.slice(0, 200)}`);
  }
  return res.json();
}

/** Coerce a value (often a numeric string from the API) to a finite Number, else null. */
export function num(v) {
  if (v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

/** Percent change of `now` vs `prev`; null if either is missing or prev is 0. */
export function pctChange(now, prev) {
  const a = num(now);
  const b = num(prev);
  if (a == null || b == null || b === 0) return null;
  return ((a - b) / b) * 100;
}

/**
 * Annualize a per-interval funding rate to a percentage APR.
 * @param {string|number} rate           funding rate for one interval
 * @param {string|number} [intervalHours=1]  length of that interval in hours
 */
export function fundingToApr(rate, intervalHours = 1) {
  const r = num(rate);
  const h = num(intervalHours) || 1;
  return r == null ? null : (r / h) * 24 * 365 * 100;
}

const ADDRESS_RE = /^0x[0-9a-fA-F]{40}$/;

/** Validate + lowercase an EVM address; throws a friendly error otherwise. */
export function normalizeAddress(user) {
  const addr = String(user || '').trim();
  if (!ADDRESS_RE.test(addr)) {
    throw new Error(`--user must be a 0x-prefixed 40-hex-char address, got: ${user}`);
  }
  return addr.toLowerCase();
}

/** Millisecond epoch → ISO string (null-safe). */
export function isoTime(ms) {
  const n = num(ms);
  if (n == null) return null;
  return new Date(n).toISOString();
}

export { INFO_URL };
