# Output Format Reference

opencli supports multiple output formats for all Twitter commands via the `-f` / `--format` flag.

## Formats

| Format | Flag | Description |
|---|---|---|
| Table | `-f table` | Default. Rich CLI table with bold headers, word wrapping, and a footer showing row count and elapsed time |
| JSON | `-f json` | Pretty-printed JSON array with 2-space indent |
| YAML | `-f yaml` | Structured YAML with 120-char line width |
| Markdown | `-f md` | Pipe-delimited markdown table |
| CSV | `-f csv` | Comma-separated values with proper quoting and escaping |

## Column Definitions

### Tweet columns (`timeline`, `search`, `bookmarks`)

| Column | Type | Description |
|---|---|---|
| `id` | string | Tweet ID |
| `author` | string | @handle of the tweet author |
| `text` | string | Tweet text content |
| `created_at` | string | Timestamp of the tweet |
| `likes` | number | Like count |
| `views` | number | View count |
| `url` | string | Direct URL to the tweet |

### Trending columns (`trending`)

| Column | Type | Description |
|---|---|---|
| `rank` | number | Trending rank position |
| `topic` | string | Trending topic or hashtag |
| `tweet_count` | number | Number of tweets about the topic |

### Profile columns (`profile`)

| Column | Type | Description |
|---|---|---|
| `username` | string | @handle |
| `name` | string | Display name |
| `bio` | string | Profile bio/description |
| `followers_count` | number | Follower count |
| `following_count` | number | Following count |
| `tweet_count` | number | Total tweets |

### User list columns (`followers`, `following`)

| Column | Type | Description |
|---|---|---|
| `username` | string | @handle |
| `name` | string | Display name |
| `bio` | string | Profile bio/description |
| `followers_count` | number | Follower count |

## JSON Example

```json
[
  {
    "id": "1234567890",
    "author": "@exampleuser",
    "text": "Breaking: $AAPL earnings beat expectations...",
    "created_at": "2026-03-26T14:30:00Z",
    "likes": 1523,
    "views": 89000,
    "url": "https://x.com/exampleuser/status/1234567890"
  }
]
```

## Notes

- Table format includes a footer with total row count and elapsed time
- JSON output is a flat array (no envelope wrapper)
- CSV properly escapes commas and quotes within fields
- Markdown format is suitable for pasting into documents or LLM context
