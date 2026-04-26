# opencli Command Discovery

When an agent needs to drive a site through opencli, it should treat the **registry** as the source of truth — not a hand-maintained list. This file explains how to query the registry and what each field means.

---

## `opencli list`

Lists every registered command in the local opencli installation.

```bash
opencli list                    # Grouped, colorful, table format (for humans)
opencli list -f json            # Flat JSON array (for agents)
opencli list -f yaml            # YAML
opencli list | grep -i reddit   # Filter to a site by keyword
```

### JSON entry schema

Each entry in `opencli list -f json` has roughly this shape (some fields optional):

```json
{
  "site": "yahoo-finance",
  "name": "quote",
  "aliases": [],
  "description": "Yahoo Finance 股票行情",
  "strategy": "PUBLIC",
  "browser": false,
  "args": [
    { "name": "symbol", "type": "string", "required": true, "positional": true, "help": "Stock ticker (e.g. AAPL, MSFT, TSLA)" }
  ],
  "columns": ["symbol", "name", "price", "change", "changePercent", "open", "high", "low", "volume", "marketCap"]
}
```

**Field meanings:**

| Field | Meaning |
|---|---|
| `site` | Adapter namespace — used as the first argument to `opencli <site> <command>` |
| `name` | Subcommand name |
| `aliases` | Alternative names for the same command |
| `description` | Short human description — inspect before assuming read vs write |
| `strategy` | `PUBLIC` / `COOKIE` / `HEADER` / `INTERCEPT` / `UI` / `LOCAL` — determines whether a browser/login is required |
| `browser` | `true` if the command touches a browser target |
| `args` | Positional and flag arguments with types, defaults, and help text |
| `columns` | Canonical ordered list of output columns |

---

## `opencli <site> --help`

Shows all commands registered under a single site along with their one-line descriptions. Useful when you know the site but not the command name:

```bash
opencli eastmoney --help
opencli reddit --help
opencli xueqiu --help
```

## `opencli <site> <command> --help`

Shows positional args, flags, defaults, and examples for a specific command:

```bash
opencli yahoo-finance quote --help
opencli reddit subreddit --help
opencli hackernews top --help
```

Always run this before invoking a command you haven't used before in the current session.

---

## Read vs write — how to tell

There is no formal `readonly: true` flag on every registry entry. Distinguish read from write by:

1. **Command name heuristics** — action verbs that mutate state are writes. Never invoke: `post`, `reply`, `comment`, `like`, `unlike`, `upvote`, `downvote`, `save`, `unsave`, `subscribe`, `unsubscribe`, `follow`, `unfollow`, `block`, `unblock`, `delete`, `bookmark`, `unbookmark`, `send`, `create-draft`, `reply-dm`, `accept`, `hide-reply`.
2. **`description` field** — phrases like "fetch", "read", "get", "list", "search" → read. Phrases like "post", "send", "submit", "create" → write.
3. **When uncertain, don't run it.** Ask the user or skip.

Reading an adapter's source at `clis/<site>/<command>.js` in the opencli repo is the definitive answer, but for the purposes of this skill the name + description is usually enough.

---

## Strategies — what they need

| Strategy | Browser needed | Login needed | Typical latency |
|---|---|---|---|
| `PUBLIC` | No | No | Fast (HTTP) |
| `LOCAL` | No | No | Fast (local) |
| `COOKIE` | Yes, logged in | Yes | Fast (reuses session cookie) |
| `HEADER` | Yes, logged in | Yes | Fast (captures one header) |
| `INTERCEPT` | Yes, logged in | Yes | Slow (opens an automation window) |
| `UI` | Yes, logged in | Yes | Slowest (scripts the DOM) |

If the user has the site open in Chrome and the Browser Bridge extension loaded, the four auth-requiring strategies work transparently. Otherwise run `opencli doctor` to diagnose.

---

## Examples of "discover → run" flow

### User: "read the front page of hackernews"

```bash
opencli hackernews --help                 # Confirm the command name
opencli hackernews top --help             # Check args and flags
opencli hackernews top --limit 20 -f json
```

### User: "what's Xueqiu saying about BYD?"

```bash
opencli xueqiu --help                     # See all Xueqiu commands
opencli xueqiu stock --help               # Check positional arg format
opencli xueqiu stock SZ002594 -f json     # BYD is 002594 on Shenzhen
opencli xueqiu comments SZ002594 --limit 30 -f json
```

### User: "pull the Eastmoney hot rank list"

```bash
opencli eastmoney hot-rank --help
opencli eastmoney hot-rank -f json
```

### User: "search arXiv for mean-reversion papers"

```bash
opencli arxiv --help
opencli arxiv search "mean reversion" --limit 10 -f json
```

---

## Don'ts

- Don't paste a hand-maintained adapter list into the plan — it rots. Run `opencli list -f json` at task start.
- Don't assume every adapter needs a browser. `strategy: PUBLIC` doesn't.
- Don't silently fall back from a failing adapter to raw `curl` or `fetch`. Re-run with `OPENCLI_DIAGNOSTIC=1` to get a `RepairContext`, then fix the adapter or file an issue.
- Don't invoke any command whose name or description suggests mutation.
