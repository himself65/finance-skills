/**
 * OPRA symbol parsing + expiry helpers.
 *
 * TradingView's options scanner returns symbols in OCC-style form:
 *   OPRA:<ROOT><YY><MM><DD><C|P><STRIKE>
 * For example: OPRA:SNDK260522C2090.0
 *   root: SNDK, expiry: 2026-05-22, type: call, strike: 2090
 */

/**
 * Parse an OPRA-style options symbol.
 * @param {string} symbol e.g. "OPRA:SNDK260522C2090.0"
 * @returns {{root: string, expiry: string, type: 'call'|'put', strike: number}}
 */
export function parseOpraSymbol(symbol) {
  const m = String(symbol).match(/^OPRA:([A-Z.]+?)(\d{2})(\d{2})(\d{2})([CP])([\d.]+)$/);
  if (!m) {
    throw new Error(`Not an OPRA symbol: ${symbol}`);
  }
  const [, root, yy, mm, dd, cp, strikeRaw] = m;
  return {
    root,
    expiry: `20${yy}-${mm}-${dd}`,
    type: cp === 'C' ? 'call' : 'put',
    strike: Number(strikeRaw),
  };
}

/**
 * Convert TradingView's integer expiration (YYYYMMDD) to ISO date.
 * @param {number|string} value e.g. 20260522
 * @returns {string} "2026-05-22"
 */
export function expirationToIso(value) {
  const s = String(value);
  if (!/^\d{8}$/.test(s)) {
    throw new Error(`Bad expiration: ${value}`);
  }
  return `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;
}

/**
 * Days-to-expiry from today (UTC) to the given ISO date.
 * @param {string} iso "YYYY-MM-DD"
 * @param {Date} [now]
 * @returns {number} integer days
 */
export function daysToExpiry(iso, now = new Date()) {
  const target = new Date(`${iso}T00:00:00Z`).getTime();
  const today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  return Math.round((target - today) / 86_400_000);
}

/**
 * Build a full TradingView symbol from exchange + ticker.
 * @param {string} exchange e.g. "NASDAQ"
 * @param {string} ticker e.g. "AAPL"
 * @returns {string} "NASDAQ:AAPL"
 */
export function buildTvSymbol(exchange, ticker) {
  return `${String(exchange).toUpperCase()}:${String(ticker).toUpperCase()}`;
}
