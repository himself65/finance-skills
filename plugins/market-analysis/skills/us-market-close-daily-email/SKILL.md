---
name: us-market-close-daily-email
description: >
  Generate and email a Chinese US market close daily report. Use for scheduled cron jobs,
  美股收盘日报, US market close recap, SMTP delivery, HTML market report email, yfinance-based
  market recaps, market breadth, sector rotation, technical levels, and next-day trading plans.
---

# US Market Close Daily Email

Generate a Chinese《美股收盘日报》, write Markdown/HTML artifacts, and send the report by SMTP email.

## Step 1: Detect Runtime and Dependencies

Run prerequisite checks before generating the report:

```bash
date
python3 -m pip show yfinance >/dev/null 2>&1 && echo YFINANCE_INSTALLED || echo YFINANCE_NOT_INSTALLED
test -f "$HOME/.hermes/config/email-ingest.env" && echo SMTP_ENV_OK || echo SMTP_ENV_MISSING
```

Decision tree:
- If `yfinance` is missing, install with `python3 -m pip install -q yfinance pandas numpy requests beautifulsoup4 lxml`.
- If the SMTP env file is missing or lacks `BRAIN_EMAIL_ADDRESS`/`BRAIN_EMAIL_PASSWORD`, generate report files but mark send failure. Never print the password.
- Use the recipient requested by the user or cron prompt. If no recipient is provided, ask before sending.
- Set `yf.set_tz_cache_location('/tmp/yfinance-cache')` in cron/sandbox runs.

## Step 2: Determine Report Date

Use the latest complete trading day from `SPY` daily history as the report date. If the job runs outside the intended schedule, still generate and send but add a run-time note at the top.

## Step 3: Fetch and Compute Market Data

Use `yfinance` for:
- Indices/ETFs: `SPY QQQ IWM SMH SOXX IGV XLK XLC XLY XLF XLI XLV XLP XLE XLU XLB XLRE DIA RSP SCHG VTV IWO IWN` plus `^DJI ^GSPC ^IXIC ^NDX ^RUT ^SOX ^VIX`.
- Macro proxies: `^TNX ^FVX ^TYX DX-Y.NYB GC=F CL=F BZ=F BTC-USD ETH-USD`.
- Focus stocks from the user's recurring list.

Compute daily/5-day/1-month performance, 20/50/100/200-day moving averages, RSI, MACD state, support/resistance, and volume versus 20-day average.

Before writing `暂无可靠数据`, check `references/reliable-data-fallbacks.md`. In particular:
- Use U.S. Treasury CSV / FRED for 2Y/10Y/30Y and curve spreads.
- Use FRED for HY/IG credit spreads.
- Use yfinance `^MOVE`, `^VVIX`, `^VIX3M` plus CBOE CSV fallbacks for volatility internals.
- Use CBOE CSV for put/call ratio.
- Use Nasdaq screener API for NYSE/Nasdaq advancers/decliners.
- Use Nasdaq earnings API for earnings calendar.
- Use S&P 500/Nasdaq-100 constituent lists plus yfinance to compute breadth above moving averages when feasible.

Only mark data unavailable after the relevant fallback has failed or is genuinely not applicable. For index volume (SOX/VIX), write `不适用（指数无成交量）` and optionally provide ETF proxies rather than `暂无可靠数据`.

## Step 4: Build Required Report Structure

The report must be Chinese and contain sections 0-15 exactly:
0. 今日一句话总结
1. 大盘表现总览
2. 盘中走势复盘
3. 宏观环境
4. 板块表现
5. 主题与风格
6. 市场宽度与参与度
7. 技术面分析
8. 重点个股新闻与异动
9. 财报日历与财报解读
10. 机构观点与资金流
11. 板块轮动判断
12. 我的重点关注股观察
13. 明日交易计划/观察清单
14. 风险提示
15. 最终结论

Write Markdown to `/tmp/us_market_close_daily_YYYY-MM-DD.md`.

## Step 5: Build Email-Readable HTML

Write HTML to `/tmp/us_market_close_daily_YYYY-MM-DD.html` with:
- `multipart/alternative` later: Markdown as `text/plain`, HTML as `text/html`.
- Top market snapshot cards for date/status/SPY/QQQ/IWM/SMH/VIX/10Y/DXY/WTI/BTC.
- **Gmail-safe snapshot layout:** do not use CSS Grid/Flex for `市场快照`; Gmail can render it incorrectly. Use a presentation-table layout with inline styles, fixed rows `SPY/QQQ/IWM`, `SMH/VIX/10Y`, `DXY/WTI/BTC`, and inline gain/loss colors.
- Cards for one-sentence summary and tomorrow's top 5 signals.
- A 15-section table of contents with anchors.
- Tables wrapped in scrollable table containers with sticky/dark headers, right-aligned numbers, and inline or embedded CSS only.
- Section 12 split into small tables by user-defined focus groups; include a one-line Chinese analysis next to each stock if requested.
- Risk matrix cards/tables with low/medium/medium-high/high visual distinction.

See `references/reliable-data-fallbacks.md` for the tested snapshot table pattern and source fallbacks.

## Step 6: Send via Python smtplib

Do not assume a specific mail CLI is installed. Send with Python SMTP unless the user requests another tool:

```python
from email.message import EmailMessage
import os, smtplib
# read ~/.hermes/config/email-ingest.env or another user-provided env file
msg = EmailMessage()
msg['From'] = BRAIN_EMAIL_ADDRESS
msg['To'] = recipient_email
msg['Subject'] = f'美股收盘日报｜{report_date}'
msg.set_content(markdown_report)
msg.add_alternative(html_report, subtype='html')
with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as smtp:
    smtp.login(BRAIN_EMAIL_ADDRESS, BRAIN_EMAIL_PASSWORD)
    smtp.send_message(msg)
```

Only treat delivery as successful if `smtp.send_message(msg)` returns and Python exits with code 0.

## Step 7: Final Cron Response

Do not paste the report. Reply only:
- whether sending succeeded,
- report date,
- Markdown path,
- HTML path,
- if failed, the failure reason.

If there is genuinely nothing new to report and the task explicitly allows suppression, return exactly `[SILENT]`.

## Pitfalls

- `SIVE` may fail in Yahoo Finance as possibly delisted; use `SIVE.ST` first, then `SIVEF`, and clearly label the substituted ticker/exchange.
- SOX and VIX are indexes: volume is `不适用（指数无成交量）`, not missing. Use SMH/SOXX or VXX/UVXY/term-structure proxies when needed.
- CME FedWatch may block automated access from some hosts. Do not fake probabilities; use CME only if reachable, otherwise label unavailable and lean on Treasury/Fed Funds proxies.
- In cron environments, yfinance may emit cache or OpenSSL warnings; warnings alone are not send failures.
- Never print SMTP passwords or raw env contents.
- Do not invent Reuters/Bloomberg/CNBC facts if no web/news source was fetched.
