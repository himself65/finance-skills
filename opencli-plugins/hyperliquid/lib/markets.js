/**
 * Market normalizers for Hyperliquid perp/spot metadata + asset contexts.
 *
 * `metaAndAssetCtxs` and `spotMetaAndAssetCtxs` each return a 2-tuple
 * [meta, ctxs] where `meta.universe[i]` and `ctxs[i]` are PARALLEL arrays in
 * the same order — zip by index.
 */

import { num, pctChange, fundingToApr } from './api.js';

/**
 * Zip perp `meta.universe[]` with `ctxs[]` into one normalized row per market.
 * @param {{universe: Array<{name:string,maxLeverage?:number,isDelisted?:boolean}>}} meta
 * @param {Array<object>} ctxs
 */
export function normalizePerpMarkets(meta, ctxs) {
  const universe = meta?.universe ?? [];
  return universe.map((u, i) => {
    const c = ctxs?.[i] ?? {};
    const markPx = num(c.markPx);
    const funding = num(c.funding);
    const oi = num(c.openInterest);
    const premium = num(c.premium);
    return {
      coin: u.name,
      markPx,
      midPx: num(c.midPx),
      oraclePx: num(c.oraclePx),
      prevDayPx: num(c.prevDayPx),
      change24hPct: pctChange(c.markPx, c.prevDayPx),
      fundingHrPct: funding == null ? null : funding * 100,
      fundingAprPct: fundingToApr(c.funding, 1),
      openInterest: oi,
      oiNotional: oi != null && markPx != null ? oi * markPx : null,
      dayNtlVlm: num(c.dayNtlVlm),
      premiumPct: premium == null ? null : premium * 100,
      maxLeverage: u.maxLeverage ?? null,
      delisted: u.isDelisted === true,
    };
  });
}

/**
 * Zip spot `meta.universe[]` with `ctxs[]` into one normalized row per pair.
 * Resolves the base-token name via `meta.tokens[]` (universe.tokens[0] = base).
 */
export function normalizeSpotMarkets(spotMeta, ctxs) {
  const universe = spotMeta?.universe ?? [];
  const tokens = spotMeta?.tokens ?? [];
  const tokenName = (idx) => tokens.find((t) => t.index === idx)?.name ?? `#${idx}`;
  return universe.map((u, i) => {
    const c = ctxs?.[i] ?? {};
    const markPx = num(c.markPx);
    const supply = num(c.circulatingSupply);
    return {
      pair: c.coin ?? u.name,
      base: Array.isArray(u.tokens) ? tokenName(u.tokens[0]) : null,
      markPx,
      midPx: num(c.midPx),
      prevDayPx: num(c.prevDayPx),
      change24hPct: pctChange(c.markPx, c.prevDayPx),
      dayNtlVlm: num(c.dayNtlVlm),
      circulatingSupply: supply,
      marketCap: markPx != null && supply != null ? markPx * supply : null,
      canonical: u.isCanonical === true,
    };
  });
}

/**
 * Resolve `allMids` keys to display names.
 *
 * allMids keys come in three forms:
 *   - perp coin name + canonical spot pair name → already friendly, passed through
 *   - "@<index>"  → a non-canonical spot pair; resolved to "BASE/QUOTE" via tokens
 *   - "#<n>"      → a builder-deployed perp-dex market; passed through as-is
 *
 * @param {Record<string,string>} allMids
 * @param {object} spotMeta  result of `spotMeta` (universe + tokens)
 * @param {string} [coinFilter]  case-insensitive substring filter
 */
export function resolveMids(allMids, spotMeta, coinFilter) {
  const tokens = spotMeta?.tokens ?? [];
  const tokenName = (idx) => tokens.find((t) => t.index === idx)?.name ?? `#${idx}`;
  const nameByKey = new Map();
  for (const u of spotMeta?.universe ?? []) {
    if (Array.isArray(u.tokens) && u.tokens.length === 2) {
      nameByKey.set(`@${u.index}`, `${tokenName(u.tokens[0])}/${tokenName(u.tokens[1])}`);
    }
  }
  const filter = coinFilter ? String(coinFilter).toUpperCase() : null;
  const rows = [];
  for (const [key, px] of Object.entries(allMids ?? {})) {
    const coin = nameByKey.get(key) ?? key;
    if (filter && !coin.toUpperCase().includes(filter)) continue;
    rows.push({ coin, mid: num(px) });
  }
  return rows;
}
