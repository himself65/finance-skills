"use client";

import { useState } from "react";

type Chapter = {
  id: string;
  num: string;
  title: string;
  content: React.ReactNode;
};

function ChevronIcon({ open }: { open: boolean }) {
  return (
    <svg
      className={`w-3.5 h-3.5 shrink-0 text-text-muted transition-transform duration-200 ${open ? "rotate-90" : ""}`}
      viewBox="0 0 16 16"
      fill="currentColor"
    >
      <path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z" />
    </svg>
  );
}

function Note({ children }: { children: React.ReactNode }) {
  return (
    <div className="border border-border rounded-lg px-4 py-3 text-sm text-text-secondary leading-relaxed bg-bg-elevated">
      {children}
    </div>
  );
}

function Label({ children, color }: { children: React.ReactNode; color?: "green" | "red" | "yellow" }) {
  const colorClass = color === "green" ? "text-green" : color === "red" ? "text-red-400" : color === "yellow" ? "text-yellow" : "text-text-muted";
  return (
    <span className={`text-[10px] font-semibold uppercase tracking-wider inline-block px-1.5 py-0.5 rounded bg-bg-hover border border-border shrink-0 ${colorClass}`}>
      {children}
    </span>
  );
}

function RuleItem({
  label,
  labelColor,
  title,
  desc,
}: {
  label: string;
  labelColor?: "green" | "red" | "yellow";
  title: string;
  desc: string;
}) {
  return (
    <div className="flex items-start gap-3 border border-border rounded-lg p-3 bg-bg">
      <Label color={labelColor}>{label}</Label>
      <div>
        <p className="font-medium text-sm text-text">{title}</p>
        <p className="text-xs text-text-muted mt-0.5 leading-relaxed">{desc}</p>
      </div>
    </div>
  );
}

function StageBox({
  num,
  title,
  accent,
  children,
}: {
  num: string;
  title: string;
  accent?: "green" | "yellow" | "red";
  children: React.ReactNode;
}) {
  const accentBorder = accent === "green" ? "border-green/40" : accent === "yellow" ? "border-yellow/40" : accent === "red" ? "border-red-400/40" : "border-border";
  const numColor = accent === "green" ? "text-green" : accent === "yellow" ? "text-yellow" : accent === "red" ? "text-red-400" : "text-text-muted";
  return (
    <div className={`border rounded-lg p-4 bg-bg ${accentBorder}`}>
      <div className={`text-lg font-bold font-mono ${numColor}`}>{num}</div>
      <div className="font-semibold text-sm mt-1 text-text-secondary">{title}</div>
      <div className="text-xs text-text-muted mt-2 leading-relaxed">{children}</div>
    </div>
  );
}

function CompareColumn({
  title,
  items,
  type,
}: {
  title: string;
  items: string[];
  type: "positive" | "negative";
}) {
  const symbol = type === "positive" ? "+" : "−";
  const symbolColor = type === "positive" ? "text-green" : "text-red-400";
  return (
    <div className="border border-border rounded-lg p-4 bg-bg">
      <p className="font-semibold text-sm mb-2 text-text">{title}</p>
      <ul className="space-y-1.5">
        {items.map((item, i) => (
          <li key={i} className="text-xs text-text-muted flex gap-2 leading-relaxed">
            <span className={`${symbolColor} shrink-0`}>{symbol}</span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function FormulaBox({ children }: { children: React.ReactNode }) {
  return (
    <div className="border border-border rounded-lg px-4 py-3 text-center font-mono text-sm text-text-secondary bg-bg-elevated">
      {children}
    </div>
  );
}

function CheckItem({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex items-start gap-2 text-xs text-text-muted bg-bg border border-border rounded px-3 py-2">
      <span className="text-text-muted shrink-0 mt-px">&#9744;</span>
      <span className="leading-relaxed">{children}</span>
    </li>
  );
}

function StatBox({ label, value, sub, valueColor }: { label: string; value: string; sub: string; valueColor?: "green" | "red" | "yellow" }) {
  const vc = valueColor === "green" ? "text-green" : valueColor === "red" ? "text-red-400" : valueColor === "yellow" ? "text-yellow" : "text-text";
  return (
    <div className="border border-border rounded-lg p-3 text-center bg-bg">
      <p className="text-[10px] text-text-muted uppercase tracking-wider">{label}</p>
      <p className={`text-lg font-bold mt-0.5 font-mono ${vc}`}>{value}</p>
      <p className="text-[10px] text-text-muted mt-0.5">{sub}</p>
    </div>
  );
}

// ─── Chapter Content ────────────────────────────────────────────

const chapters: Chapter[] = [
  {
    id: "overview",
    num: "1",
    title: "What Is SEPA?",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          <strong className="text-text">SEPA</strong> (Specific Entry Point Analysis) is a complete trading system developed by Mark Minervini over 37 years of active trading. His audited track record includes +220% average annual return over 5 years, +155% in the 1997 U.S. Investing Championship, and +334.8% in the 2021 Championship.
        </p>
        <Note>
          <strong className="text-text">One-sentence summary:</strong> Buy the right stock, in the right stage, at a precise entry point, with strict risk management.
        </Note>

        <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mt-6 mb-3">Five Pillars</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {[
            ["1. Stage 2 Uptrend", "Only buy stocks in their primary uptrend phase — skip basing and declining stocks entirely."],
            ["2. Trend Template", "8 technical conditions must all pass before considering entry. Fail one → skip the stock."],
            ["3. Fundamental Support", "Accelerating EPS, revenue growth, institutional buying. Real leaders have real earnings behind them."],
            ["4. Chart Patterns (VCP)", "Wait for volatility to contract to the breaking point, then enter at the precise moment supply is exhausted."],
          ].map(([title, desc]) => (
            <div key={title} className="border border-border rounded-lg p-3 bg-bg">
              <p className="font-semibold text-sm text-text">{title}</p>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
        <div className="border border-border rounded-lg p-3 bg-bg-elevated">
          <p className="font-semibold text-sm text-text">5. Strict Risk Control <span className="text-text-muted font-normal">(Most Important)</span></p>
          <p className="text-xs text-text-muted mt-1 leading-relaxed">Risk ≤1-2% per trade, stop loss set before entry, R:R ≥ 2:1. Win rate is only ~50% — profitability comes from losing small and winning big.</p>
        </div>

        <Note>
          <strong className="text-text">The casino analogy:</strong> A casino doesn&apos;t win every hand — it wins through mathematical edge over thousands of hands. SEPA works the same way. With 50% win rate: 5 wins × 15% − 5 losses × 6% = <strong className="text-green">+45% net</strong>. A trader with 55% win rate but no stop discipline: 5.5 × 5% − 4.5 × 12% = <strong className="text-red-400">−26.5% net</strong>.
        </Note>
      </div>
    ),
  },
  {
    id: "stages",
    num: "2",
    title: "The 4 Stages of Every Stock",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          Every stock cycles through four stages repeatedly (Weinstein, 1988). <strong className="text-text">Identifying the current stage is the starting point for all decisions.</strong>
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <StageBox num="01" title="Basing">
            Price near 200MA, MAs flat/tangled, low volume. Institutions quietly accumulate.
            <p className="mt-2 font-medium text-text-secondary">→ Do nothing. Wait.</p>
          </StageBox>
          <StageBox num="02" title="Advancing" accent="green">
            Higher highs/lows, bullish MA alignment, volume expands on up days. VCP patterns appear.
            <p className="mt-2 font-medium text-green">→ The ONLY stage to buy.</p>
          </StageBox>
          <StageBox num="03" title="Topping" accent="yellow">
            Wide swings at highs, false breakouts, heavy volume without progress. Media hype peaks.
            <p className="mt-2 font-medium text-yellow">→ Reduce. No new buys.</p>
          </StageBox>
          <StageBox num="04" title="Declining" accent="red">
            Below all MAs, bearish alignment. &quot;Down 60%&quot; can still go to zero.
            <p className="mt-2 font-medium text-red-400">→ Full cash. Stay away.</p>
          </StageBox>
        </div>

        <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mt-4 mb-2">Base Count — How Far Along Is Stage 2?</p>
        <div className="overflow-x-auto">
          <table className="w-full text-xs border border-border rounded-lg overflow-hidden">
            <thead>
              <tr>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Base #</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Safety</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Advice</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border"><td className="px-3 py-2">1–2</td><td className="px-3 py-2 text-green">Highest</td><td className="px-3 py-2 text-text-muted">Full position — early Stage 2, max upside</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2">3–4</td><td className="px-3 py-2 text-yellow">Moderate</td><td className="px-3 py-2 text-text-muted">Slightly smaller position</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2">5–6</td><td className="px-3 py-2 text-red-400">Low</td><td className="px-3 py-2 text-text-muted">Half position max — late stage</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2">7+</td><td className="px-3 py-2 text-red-400">Dangerous</td><td className="px-3 py-2 text-text-muted">Avoid — likely transitioning to Stage 3</td></tr>
            </tbody>
          </table>
        </div>

        <Note>
          <strong className="text-text">Stage 1→2 transition signals:</strong> (1) 200MA shifts from declining → flat → upward (2) Price breaks above consolidation with volume (3) 50MA crosses above 150MA/200MA (golden cross)
        </Note>
      </div>
    ),
  },
  {
    id: "trend-template",
    num: "3",
    title: "Trend Template — 8 Conditions",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          The trend template is a pre-entry qualification. <strong className="text-text">All 8 must pass simultaneously.</strong> If any fails, skip the stock entirely.
        </p>

        <div className="space-y-2">
          <RuleItem label="Must" labelColor="green" title="1. Price > 150MA AND Price > 200MA" desc="Stock is above long-term moving averages — confirmed uptrend." />
          <RuleItem label="Must" labelColor="green" title="2. 150MA > 200MA" desc="Intermediate MA leads the long-term MA — bullish hierarchy." />
          <RuleItem label="Must" labelColor="green" title="3. 200MA trending up ≥ 1 month (ideally 4-5 months)" desc="Long-term trend is healthy and sustained, not a temporary bounce." />
          <RuleItem label="Must" labelColor="green" title="4. 50MA > 150MA AND 50MA > 200MA" desc="Short-term MA leads all others — strong recent momentum." />
          <RuleItem label="Must" labelColor="green" title="5. Price > 50MA" desc="Near-term trend confirmed positive." />
          <RuleItem label="Must" labelColor="green" title="6. Price ≥ 30% above 52-week low" desc="Stock has truly left its bottom — not a minor bounce." />
          <RuleItem label="Must" labelColor="green" title="7. Price within 25% of 52-week high" desc="Trading near highs, not far off a peak. Closer = stronger." />
          <RuleItem label="Key" labelColor="yellow" title="8. Relative Strength > 70th percentile (prefer 85-90+)" desc="Only trade real market leaders. RS = how this stock's 12-month return ranks vs the entire market." />
        </div>

        <Note>
          <strong className="text-text">Memory aid — 3 sentences:</strong><br />
          Conditions 1-5 = <strong className="text-text">MA Staircase</strong> (Price {`>`} 50MA {`>`} 150MA {`>`} 200MA, 200MA rising)<br />
          Conditions 6-7 = <strong className="text-text">Price Position</strong> (far from low ≥30%, near high ≤25%)<br />
          Condition 8 = <strong className="text-text">Relative Strength</strong> (market leader, RS {`>`} 70)
        </Note>
      </div>
    ),
  },
  {
    id: "fundamentals",
    num: "4",
    title: "Fundamental Requirements",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          75% of superperformer stocks had quarterly EPS growth {`>`}20% before their biggest move. Fundamentals separate real leaders from hype.
        </p>

        <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2">EPS Growth Tiers</p>
        <div className="grid grid-cols-3 gap-3">
          <StatBox label="Minimum" value="≥ 20%" sub="Below = disqualify" valueColor="green" />
          <StatBox label="Preferred" value="25–50%" sub="Most winners here" valueColor="yellow" />
          <StatBox label="Super Stock" value="50%+" sub="Biggest movers" />
        </div>

        <Note>
          <strong className="text-text">Acceleration matters most.</strong> Growth must be speeding up: this quarter&apos;s EPS growth rate {`>`} last quarter&apos;s. If growth decelerates (30% → 22%), that&apos;s a warning even though 22% still looks decent.
        </Note>

        <div className="overflow-x-auto">
          <table className="w-full text-xs border border-border rounded-lg overflow-hidden">
            <thead>
              <tr>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Check</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Threshold</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Why</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Quarterly EPS</td><td className="px-3 py-2 text-text-secondary">≥ 20%, accelerating</td><td className="px-3 py-2 text-text-muted">Core growth driver</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Annual EPS</td><td className="px-3 py-2 text-text-secondary">≥ 25% each of past 3 years</td><td className="px-3 py-2 text-text-muted">Sustained competitive advantage</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Revenue</td><td className="px-3 py-2 text-text-secondary">≥ 15% annual, ≥ 20% quarterly</td><td className="px-3 py-2 text-text-muted">Real demand, not cost-cutting</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Margins</td><td className="px-3 py-2 text-text-secondary">Stable or expanding</td><td className="px-3 py-2 text-text-muted">Pricing power, moat</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Institutions</td><td className="px-3 py-2 text-text-secondary">Holdings increasing</td><td className="px-3 py-2 text-text-muted">Smart money fueling the move</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Catalyst</td><td className="px-3 py-2 text-text-secondary">New product, FDA, contract…</td><td className="px-3 py-2 text-text-muted">With: 50-100%+; without: 15-25%</td></tr>
            </tbody>
          </table>
        </div>

        <Note>
          <strong className="text-text">Red flag:</strong> EPS growing but revenue flat/declining = &quot;fake growth&quot; from cost-cutting, layoffs, or buybacks. Not sustainable.
        </Note>
      </div>
    ),
  },
  {
    id: "vcp",
    num: "5",
    title: "VCP — Volatility Contraction Pattern",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          VCP is the signature SEPA pattern. Think of price as a <strong className="text-text">spring being compressed</strong>: each pullback is tighter than the last. When compressed to the limit (all sellers exhausted), the spring releases — that&apos;s the breakout.
        </p>

        <div className="border border-border rounded-lg p-4 bg-bg-elevated">
          <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">Typical VCP Contraction Sequence</p>
          <div className="flex items-end gap-2 justify-center py-2">
            {[
              { depth: "−20%", h: 56, opacity: "opacity-40" },
              { depth: "−12%", h: 36, opacity: "opacity-30" },
              { depth: "−6%", h: 20, opacity: "opacity-25" },
              { depth: "−3%", h: 10, opacity: "opacity-20" },
            ].map((c, i) => (
              <div key={i} className="flex flex-col items-center gap-1.5">
                <div className={`w-14 bg-text-secondary ${c.opacity} rounded`} style={{ height: `${c.h}px` }} />
                <span className="text-[10px] text-text-muted font-mono">{c.depth}</span>
              </div>
            ))}
            <div className="text-text-muted px-1 self-center text-xs">→</div>
            <div className="flex flex-col items-center gap-1.5">
              <div className="w-14 bg-text-secondary opacity-50 rounded" style={{ height: "64px" }} />
              <span className="text-[10px] text-text-secondary font-mono font-semibold">Breakout</span>
            </div>
          </div>
          <p className="text-[10px] text-text-muted mt-2 text-center">Each contraction is smaller → volume dries up → breakout on heavy volume</p>
        </div>

        <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mt-4 mb-2">7 Identification Rules</p>
        <div className="space-y-2">
          <RuleItem label="Must" labelColor="green" title="1. Stock in Stage 2 uptrend" desc="No VCP exists in a downtrend — that's just a normal bounce." />
          <RuleItem label="Must" labelColor="green" title="2. Pullback depths decrease (e.g. 20% → 12% → 6% → 3%)" desc="Minimum 3 contractions, 4-5 ideal. If 2nd pullback is deeper than 1st, it's NOT a VCP." />
          <RuleItem label="Must" labelColor="green" title="3. Volume shrinks → Volume Dry-Up (VDU)" desc="The final contraction shows multi-week low volume — sellers are nearly depleted." />
          <RuleItem label="Must" labelColor="green" title="4. Higher lows on each pullback" desc="Buyers stepping in at progressively higher prices = institutional accumulation." />
          <RuleItem label="Must" labelColor="green" title="5. Clear pivot point (consolidation high)" desc="The entry target. VCP breakout = crossing this resistance level." />
          <RuleItem label="Key" labelColor="yellow" title="6. RS > 70 (prefer 85-90+)" desc="Leader VCPs succeed far more often than laggard VCPs." />
          <RuleItem label="Key" labelColor="yellow" title="7. Bull or neutral market environment" desc="Bear market VCP breakouts fail at much higher rates." />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
          <CompareColumn title="Quality VCP" type="positive" items={[
            "Pullback depths strictly decreasing",
            "Each low higher than the last",
            "Volume decreasing → VDU at the end",
            "Clear Stage 2 uptrend context",
            "Breakout with volume ≥ 1.5x average",
          ]} />
          <CompareColumn title="Fake VCP (Traps)" type="negative" items={[
            "Irregular pullback depths",
            "Lows not progressively higher",
            "Volume not shrinking on pullbacks",
            "Stock in a downtrend overall",
            "Breakout with weak volume → falls back",
          ]} />
        </div>
      </div>
    ),
  },
  {
    id: "other-patterns",
    num: "6",
    title: "Other Consolidation Patterns",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          Besides VCP, SEPA uses four more classic patterns. All share the same entry rule: <strong className="text-text">breakout above pivot + volume ≥ 1.5x average</strong>.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-xs border border-border rounded-lg overflow-hidden">
            <thead>
              <tr>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Pattern</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Depth</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Duration</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Key Feature</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Strength</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">VCP</td><td className="px-3 py-2">Decreasing → &lt;3%</td><td className="px-3 py-2">3–20 wk</td><td className="px-3 py-2 text-text-muted">Multi-contraction + higher lows</td><td className="px-3 py-2 font-mono text-text-secondary">5/5</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Cup &amp; Handle</td><td className="px-3 py-2">Cup 12-35%, handle ≤12%</td><td className="px-3 py-2">7–65 wk</td><td className="px-3 py-2 text-text-muted">U-shaped base + small handle</td><td className="px-3 py-2 font-mono text-text-secondary">4/5</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Flat Base</td><td className="px-3 py-2">≤ 15%</td><td className="px-3 py-2">5–10 wk</td><td className="px-3 py-2 text-text-muted">Tight range near prior high</td><td className="px-3 py-2 font-mono text-text-secondary">3/5</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">Bull Flag</td><td className="px-3 py-2">≤ 50% of pole</td><td className="px-3 py-2">1–5 wk</td><td className="px-3 py-2 text-text-muted">Sharp advance + tight pullback</td><td className="px-3 py-2 font-mono text-text-secondary">4/5</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">High Tight Flag</td><td className="px-3 py-2">≤ 25% after 100%+ run</td><td className="px-3 py-2">1–4 wk</td><td className="px-3 py-2 text-text-muted">Rarest — most powerful</td><td className="px-3 py-2 font-mono text-text-secondary">5/5</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    ),
  },
  {
    id: "entry",
    num: "7",
    title: "Precise Entry Points",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          &quot;Specific Entry Point&quot; is what SEPA stands for. Not &quot;looks about right&quot; — a very specific price level with defined risk.
        </p>

        <Note>
          <strong className="text-text">Pivot point =</strong> the highest price in the consolidation range. Below it, supply ≥ demand. Above it, demand overwhelms remaining supply.
        </Note>

        <div className="grid grid-cols-3 gap-3">
          <StatBox label="Buy Zone" value="0 – 5%" sub="above pivot" valueColor="green" />
          <StatBox label="Chase Zone" value="> 5%" sub="Don't enter — wait" valueColor="red" />
          <StatBox label="Breakout Vol." value="≥ 1.5x" sub="20-day average" valueColor="yellow" />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2">
          <CompareColumn title="True Breakout" type="positive" items={[
            "Volume ≥ 1.5x average — big spike",
            "Closes near the day's high",
            "Volume Dry-Up preceded it",
            "Continues higher next day",
          ]} />
          <CompareColumn title="False Breakout" type="negative" items={[
            "Volume below average — weak",
            "Falls back below pivot by close",
            "No VDU before the attempt",
            "Drops back into the range quickly",
          ]} />
        </div>

        <Note>
          <strong className="text-text">Avoid entering within 2 weeks of earnings.</strong> Earnings are binary events — even a perfect chart setup can gap down on a miss.
        </Note>
      </div>
    ),
  },
  {
    id: "position",
    num: "8",
    title: "Stop Loss & Position Sizing",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          <strong className="text-text">The most critical part of SEPA.</strong> Minervini: &quot;Not losing big is the only prerequisite for winning big.&quot;
        </p>

        <FormulaBox>
          Shares = (Account × Risk%) ÷ (Entry Price − Stop Price)
        </FormulaBox>

        <div className="border border-border rounded-lg p-4 bg-bg-elevated">
          <p className="text-xs font-semibold text-text-secondary mb-2">Example: $100,000 account, 1% risk per trade</p>
          <div className="space-y-1 text-xs text-text-muted leading-relaxed">
            <p>1. Max loss = $100,000 × 1% = <strong className="text-text">$1,000</strong></p>
            <p>2. Buy at $50, stop at −7% = $46.50 → distance = <strong className="text-text">$3.50/share</strong></p>
            <p>3. Shares = $1,000 ÷ $3.50 = <strong className="text-text">285 shares</strong> ($14,250 = 14.25% of account)</p>
            <p>4. Target 1: $54.00 (+8%) → sell half, move stop to breakeven</p>
            <p>5. Target 2: $57.50 (+15%) → R:R = $7.50/$3.50 = <strong className="text-green">2.14 : 1</strong></p>
          </div>
        </div>

        <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mt-4 mb-2">Stop Loss Evolution</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {[
            ["Phase 1: Entry", "Hard stop at entry −7-8%. Non-negotiable. Set it the moment you buy."],
            ["Phase 2: At +8%", "Sell half. Move stop → entry price (breakeven). Trade can no longer lose."],
            ["Phase 3: At +15%", "Sell 25% more. Trail remaining stop along 20MA. Close below 20MA = exit all."],
          ].map(([title, desc]) => (
            <div key={title} className="border border-border rounded-lg p-3 bg-bg">
              <p className="font-semibold text-sm text-text">{title}</p>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>

        <div className="space-y-2 mt-4">
          <RuleItem label="Never" labelColor="red" title="Never move stop DOWN" desc="Stops only move up. Moving down turns small losses into catastrophic ones." />
          <RuleItem label="Never" labelColor="red" title="Never average down" desc="Adding to a loser is the fastest path to account destruction." />
          <RuleItem label="Rule" labelColor="yellow" title="After 3-4 consecutive losses, reduce risk" desc="Cut risk to 0.5%, fewer positions. Diagnose: is it your execution or the market?" />
        </div>
      </div>
    ),
  },
  {
    id: "pyramiding",
    num: "9",
    title: "Pyramiding vs Averaging Down",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          Pyramiding = do more of what&apos;s working. Averaging down = do more of what&apos;s failing.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-xs border border-border rounded-lg overflow-hidden">
            <thead>
              <tr>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Tranche</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">When</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Size</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary">Example</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">1st (Main)</td><td className="px-3 py-2 text-text-muted">Pivot breakout</td><td className="px-3 py-2 text-text-secondary">50%</td><td className="px-3 py-2 text-text-muted font-mono">100 @ $50</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">2nd (Add)</td><td className="px-3 py-2 text-text-muted">+8%, pullback to 20MA</td><td className="px-3 py-2 text-text-secondary">30%</td><td className="px-3 py-2 text-text-muted font-mono">60 @ $54</td></tr>
              <tr className="border-t border-border"><td className="px-3 py-2 font-medium text-text">3rd (Add)</td><td className="px-3 py-2 text-text-muted">Next base breakout</td><td className="px-3 py-2 text-text-secondary">20%</td><td className="px-3 py-2 text-text-muted font-mono">35 @ $58</td></tr>
            </tbody>
          </table>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <CompareColumn title="Pyramid (Correct)" type="positive" items={[
            "Largest position at lowest cost — max cushion",
            "Only add when market proves you right",
            "Even if adds fail, main position covers losses",
            "Each add has a new confirming signal",
          ]} />
          <CompareColumn title="Average Down (Dangerous)" type="negative" items={[
            "Adding money where your thesis is proven wrong",
            "'Lower average cost' is an illusion — real loss grows",
            "$60 → $40 can still go to $5",
            "Fastest path to account destruction",
          ]} />
        </div>
      </div>
    ),
  },
  {
    id: "losses",
    num: "10",
    title: "Handling Losing Trades",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          ~50% of trades lose money. That&apos;s expected. What matters is <strong className="text-text">how</strong> you lose.
        </p>

        <Note>
          <strong className="text-text">Mindset:</strong> Minervini treats each loss as a &quot;business expense&quot; — like a restaurant buying ingredients. Not every dish sells, but the restaurant isn&apos;t failing. The key is keeping each expense small and controlled.
        </Note>

        <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mt-4 mb-2">Post-Loss Review — 3 Questions</p>
        <div className="space-y-2">
          <div className="border border-border rounded-lg p-3 bg-bg">
            <p className="font-medium text-sm text-text">Q1: Execution or strategy problem?</p>
            <p className="text-xs text-text-muted mt-1 leading-relaxed">Execution (chased, no stop, weak volume entry) → fix the habit. Strategy (misread pattern) → study more examples.</p>
          </div>
          <div className="border border-border rounded-lg p-3 bg-bg">
            <p className="font-medium text-sm text-text">Q2: &quot;Good loss&quot; or &quot;bad loss&quot;?</p>
            <p className="text-xs text-text-muted mt-1 leading-relaxed">Good: followed all rules, market didn&apos;t cooperate — <strong className="text-text-secondary">change nothing</strong>. Bad: broke rules — <strong className="text-text-secondary">must eliminate</strong>.</p>
          </div>
          <div className="border border-border rounded-lg p-3 bg-bg">
            <p className="font-medium text-sm text-text">Q3: Individual stock or overall market?</p>
            <p className="text-xs text-text-muted mt-1 leading-relaxed">If recent breakouts keep failing, check the market first. If environment deteriorated, pause — don&apos;t force it.</p>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "market",
    num: "11",
    title: "Market Environment",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary leading-relaxed">
          The market environment is the <strong className="text-text">master switch</strong>. Even the best setups fail in bear markets.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-xs border border-border rounded-lg overflow-hidden">
            <thead>
              <tr>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-text-secondary"></th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-green">Bull</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-yellow">Choppy</th>
                <th className="bg-bg-elevated px-3 py-2 text-left font-semibold text-red-400">Bear</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border">
                <td className="px-3 py-2 font-medium text-text">Signal</td>
                <td className="px-3 py-2 text-text-muted">Indices above 200MA, breadth expanding</td>
                <td className="px-3 py-2 text-text-muted">Sideways, failed breakouts</td>
                <td className="px-3 py-2 text-text-muted">Below 200MA, &gt;50% stocks below 200MA</td>
              </tr>
              <tr className="border-t border-border">
                <td className="px-3 py-2 font-medium text-text">Risk/Trade</td>
                <td className="px-3 py-2 text-text-secondary">1–2%</td>
                <td className="px-3 py-2 text-text-secondary">0.5–1%</td>
                <td className="px-3 py-2 text-text-secondary">0%</td>
              </tr>
              <tr className="border-t border-border">
                <td className="px-3 py-2 font-medium text-text">Max Positions</td>
                <td className="px-3 py-2 text-text-secondary">6–8</td>
                <td className="px-3 py-2 text-text-secondary">2–3</td>
                <td className="px-3 py-2 text-text-secondary">0 (all cash)</td>
              </tr>
              <tr className="border-t border-border">
                <td className="px-3 py-2 font-medium text-text">Strategy</td>
                <td className="px-3 py-2 text-text-secondary">Aggressive offense</td>
                <td className="px-3 py-2 text-text-secondary">Best setups only</td>
                <td className="px-3 py-2 text-text-secondary">100% cash</td>
              </tr>
            </tbody>
          </table>
        </div>

        <Note>
          <strong className="text-text">Key insight:</strong> Holding cash in a bear market IS a winning strategy. While others lose 30-50%, you preserve full ammunition for the next bull run.
        </Note>
      </div>
    ),
  },
  {
    id: "quick-ref",
    num: "QR",
    title: "Quick Reference Card",
    content: (
      <div className="space-y-4">
        <p className="text-sm text-text-secondary">Run through this checklist before every trade.</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="border border-border rounded-lg p-4 bg-bg">
            <p className="font-semibold text-sm text-text mb-3">Pre-Entry Checklist</p>
            <ul className="space-y-1.5">
              <CheckItem>Stock in Stage 2 (bullish MA alignment)</CheckItem>
              <CheckItem>Passes all 8 trend template conditions</CheckItem>
              <CheckItem>Quarterly EPS ≥ 20% and accelerating</CheckItem>
              <CheckItem>Revenue growth ≥ 15%</CheckItem>
              <CheckItem>RS &gt; 70th percentile (prefer 90+)</CheckItem>
              <CheckItem>Valid pattern identified (VCP, cup, flag…)</CheckItem>
              <CheckItem>Market environment: bull or neutral</CheckItem>
              <CheckItem>&gt; 2 weeks until earnings</CheckItem>
              <CheckItem>Buying within 0-5% of pivot point</CheckItem>
              <CheckItem>Breakout volume ≥ 1.5x average</CheckItem>
              <CheckItem>Stop loss set (entry −7-8%)</CheckItem>
            </ul>
          </div>

          <div className="space-y-4">
            <div className="border border-border rounded-lg p-4 bg-bg">
              <p className="font-semibold text-sm text-text mb-3">Iron Rules</p>
              <ul className="space-y-1.5">
                <CheckItem>Stop set at entry — non-negotiable</CheckItem>
                <CheckItem>Risk ≤ 1-2% per trade</CheckItem>
                <CheckItem>Stops only move UP, never down</CheckItem>
                <CheckItem>Never average down</CheckItem>
                <CheckItem>3 consecutive losses → reduce risk</CheckItem>
              </ul>
            </div>

            <div className="border border-border rounded-lg p-4 bg-bg">
              <p className="font-semibold text-sm text-text mb-3">Profit-Taking</p>
              <ul className="space-y-1.5">
                <CheckItem>+8%: sell half, stop → breakeven</CheckItem>
                <CheckItem>+15%: sell 25% more</CheckItem>
                <CheckItem>Remainder: trail with 20MA</CheckItem>
                <CheckItem>Below 20MA: exit all</CheckItem>
              </ul>
            </div>
          </div>
        </div>

        <FormulaBox>
          Shares = (Account × Risk%) ÷ (Buy Price − Stop Price)
        </FormulaBox>

        <div className="border border-border rounded-lg p-4 bg-bg-elevated text-center">
          <p className="text-sm font-medium text-text-secondary italic">&quot;Not losing big is the only prerequisite for winning big.&quot;</p>
          <p className="text-xs text-text-muted mt-1">— Mark Minervini</p>
        </div>
      </div>
    ),
  },
];

// ─── Main Component ─────────────────────────────────────────────

export function SepaStudyGuide() {
  const [openChapters, setOpenChapters] = useState<Set<string>>(new Set(["overview"]));

  function toggle(id: string) {
    setOpenChapters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function expandAll() {
    setOpenChapters(new Set(chapters.map((c) => c.id)));
  }

  function collapseAll() {
    setOpenChapters(new Set());
  }

  return (
    <div className="mt-8">
      <div className="border border-border rounded-lg overflow-hidden">
        {/* Header */}
        <div className="border-b border-border px-4 py-3 bg-bg-elevated flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-text-muted" viewBox="0 0 16 16" fill="currentColor">
              <path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501A3.743 3.743 0 0 1 11.006 1h4.245a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.507a2.25 2.25 0 0 0-1.591.659l-.622.621a.75.75 0 0 1-1.06 0l-.622-.621A2.25 2.25 0 0 0 5.258 13H.75a.75.75 0 0 1-.75-.75Zm7.251 10.324.004-5.073-.002-2.253A2.25 2.25 0 0 0 5.003 2.5H1.5v9h3.757a3.75 3.75 0 0 1 1.994.574ZM8.755 4.75l-.004 7.322a3.752 3.752 0 0 1 1.992-.572H14.5v-9h-3.495a2.25 2.25 0 0 0-2.25 2.25Z" />
            </svg>
            <span className="text-xs font-semibold text-text-muted uppercase tracking-wider">Study Guide</span>
          </div>
          <div className="flex gap-2">
            <button onClick={expandAll} className="text-[10px] text-text-muted hover:text-text-secondary transition-colors px-2 py-1 rounded hover:bg-bg-hover cursor-pointer">
              Expand all
            </button>
            <button onClick={collapseAll} className="text-[10px] text-text-muted hover:text-text-secondary transition-colors px-2 py-1 rounded hover:bg-bg-hover cursor-pointer">
              Collapse all
            </button>
          </div>
        </div>

        {/* Chapters */}
        <div className="divide-y divide-border">
          {chapters.map((ch) => {
            const isOpen = openChapters.has(ch.id);
            return (
              <div key={ch.id}>
                <button
                  onClick={() => toggle(ch.id)}
                  className="w-full flex items-center gap-3 px-4 py-3 hover:bg-bg-hover transition-colors text-left cursor-pointer"
                >
                  <ChevronIcon open={isOpen} />
                  <span className="text-[10px] font-mono text-text-muted w-5 text-right shrink-0">
                    {ch.num}
                  </span>
                  <span className="text-sm font-medium text-text-secondary">{ch.title}</span>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 pt-1 sm:ml-8">
                    {ch.content}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="border-t border-border px-4 py-3 bg-bg-elevated">
          <p className="text-[10px] text-text-muted text-center">
            Based on Mark Minervini&apos;s &quot;Trade Like a Stock Market Wizard&quot; and &quot;Think &amp; Trade Like a Champion.&quot; For educational purposes only — not investment advice.
          </p>
        </div>
      </div>
    </div>
  );
}
