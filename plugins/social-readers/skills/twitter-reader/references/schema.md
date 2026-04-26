# Output Format Reference

opencli supports multiple output formats for all Twitter commands via the `-f` / `--format` flag.

## Formats

| Format | Flag | Description |
|---|---|---|
| Table | `-f table` | Default in a TTY. Rich CLI table with bold headers, word wrapping, and a footer showing row count and elapsed time |
| JSON | `-f json` | Pretty-printed JSON array with 2-space indent — preferred for agents |
| YAML | `-f yaml` | Default in non-TTY. Structured YAML with 120-char line width |
| Plain | `-f plain` | Prints a single primary field (for chat-style commands) |
| Markdown | `-f md` | Pipe-delimited markdown table |
| CSV | `-f csv` | Comma-separated values with proper quoting and escaping |

## Column Definitions

### Tweet list columns (`timeline`, `search`, `thread`)

| Column | Type | Description |
|---|---|---|
| `id` | string | Tweet ID |
| `author` | string | @handle of the tweet author |
| `text` | string | Tweet text content |
| `likes` | number | Like count |
| `retweets` | number | Retweet count |
| `replies` | number | Reply count |
| `views` | number | View count |
| `created_at` | string | Timestamp of the tweet |
| `url` | string | Direct URL to the tweet |
| `has_media` | boolean | Whether the tweet contains media (images/video) — added in 1.7.7 |
| `media_urls` | string[] | URLs of attached media — added in 1.7.7 |

### Per-user tweets columns (`tweets`)

Same as tweet-list columns above, plus:

| Column | Type | Description |
|---|---|---|
| `is_retweet` | boolean | Whether the post is a retweet of another author |

`tweets` command returns a user's most recent posts in chronological order, excluding the pinned tweet. Added in opencli 1.7.6.

### Bookmark columns (`bookmarks`)

| Column | Type | Description |
|---|---|---|
| `author` | string | @handle of the tweet author |
| `text` | string | Tweet text content |
| `likes` | number | Like count |
| `retweets` | number | Retweet count |
| `bookmarks` | number | Bookmark count |
| `url` | string | Direct URL to the tweet |

### Trending columns (`trending`)

| Column | Type | Description |
|---|---|---|
| `rank` | number | Trending rank position |
| `topic` | string | Trending topic or hashtag |
| `tweets` | number | Number of tweets about the topic |
| `category` | string | Category label from X (e.g., "Business", "Sports") |

### Profile columns (`profile`)

| Column | Type | Description |
|---|---|---|
| `screen_name` | string | @handle |
| `name` | string | Display name |
| `bio` | string | Profile bio/description |
| `location` | string | User-provided location |
| `url` | string | User's linked website |
| `followers` | number | Follower count |
| `following` | number | Following count |
| `tweets` | number | Total tweets |
| `likes` | number | Total likes |
| `verified` | boolean | Verification status |
| `created_at` | string | Account creation timestamp |

### User list columns (`followers`, `following`)

| Column | Type | Description |
|---|---|---|
| `screen_name` | string | @handle |
| `name` | string | Display name |
| `bio` | string | Profile bio/description |
| `followers` | number | Follower count |

### Notification columns (`notifications`)

| Column | Type | Description |
|---|---|---|
| `id` | string | Notification ID |
| `action` | string | Action type (like, retweet, follow, reply, mention, etc.) |
| `author` | string | @handle of the account that triggered the notification |
| `text` | string | Notification text / related tweet text |
| `url` | string | Direct URL to the notification's source |

## JSON Example

```json
[
  {
    "id": "1234567890",
    "author": "@exampleuser",
    "text": "Breaking: $AAPL earnings beat expectations...",
    "likes": 1523,
    "retweets": 240,
    "replies": 88,
    "views": 89000,
    "created_at": "2026-03-26T14:30:00Z",
    "url": "https://x.com/exampleuser/status/1234567890",
    "has_media": true,
    "media_urls": ["https://pbs.twimg.com/media/abc123.jpg"]
  }
]
```

## Notes

- Table format includes a footer with total row count and elapsed time
- JSON output is a flat array (no envelope wrapper)
- CSV properly escapes commas and quotes within fields
- Markdown format is suitable for pasting into documents or LLM context
- For programmatic use by agents, prefer `-f json`
