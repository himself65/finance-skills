# US Market Close Daily Email

Generate and email a Chinese US market close daily report with market performance, macro context, sector rotation, breadth, technical levels, key stock moves, earnings calendar, institutional views, risks, and next-day observation plans.

## Use this skill when

- The user asks for a daily 美股收盘日报.
- A scheduled cron job needs to generate and email a US market close report.
- The report needs both Markdown and email-readable HTML output.
- Market data should be sourced from yfinance plus reliable official fallbacks.
- The user wants unavailable data called out explicitly rather than invented.

## What it produces

- `/tmp/us_market_close_daily_YYYY-MM-DD.md`
- `/tmp/us_market_close_daily_YYYY-MM-DD.html`
- An SMTP email with Markdown plain text and HTML alternative body

## Data sources and fallbacks

The skill uses yfinance for prices, ETFs, indices, technical indicators, and focus stocks. For data that is often missing or delayed, read `references/reliable-data-fallbacks.md` before declaring `暂无可靠数据`.

Fallback coverage includes Treasury yields, FRED credit spreads, CBOE volatility/put-call data, Nasdaq breadth and earnings APIs, S&P 500/Nasdaq-100 breadth computation, and common yfinance ticker substitutions.

## Safety notes

- Never print SMTP passwords or raw env files.
- Do not invent Reuters/Bloomberg/CNBC facts if no source was fetched.
- Use the recipient requested by the user or cron prompt; ask if no recipient is provided.
- Treat index volume as not applicable where appropriate rather than as missing data.
