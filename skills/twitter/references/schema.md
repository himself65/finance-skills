# Structured Output Schema

`twitter-cli` uses a shared agent-friendly envelope for all `--yaml` and `--json` output.

## Success Envelope

```yaml
ok: true
schema_version: "1"
data: ...
```

## Error Envelope

```yaml
ok: false
schema_version: "1"
error:
  code: api_error
  message: User @foo not found
```

## Data Shapes by Command

| Command | `data` contains |
|---------|-----------------|
| `feed`, `bookmarks`, `search`, `user-posts`, `likes`, `list` | Array of tweet objects |
| `tweet`, `show` | Single tweet object + replies |
| `article` | Single tweet object with `articleTitle` and `articleText` fields |
| `user` | Single user object |
| `followers`, `following` | Array of user objects |
| `status` | `{ authenticated: bool, user: {...} }` |
| `whoami` | `{ user: {...} }` |
| Write commands (`post`, `like`, etc.) | Confirmation object |

## Article Fields

`twitter article <id> --json` returns the standard tweet object plus:

```yaml
data:
  id: "1234567890"
  articleTitle: "Article Title"
  articleText: |
    # Heading
    Body text...
```

## Common Error Codes

- `not_authenticated` — no valid credentials found
- `not_found` — tweet/user does not exist
- `invalid_input` — bad arguments
- `rate_limited` — HTTP 429, wait and retry
- `api_error` — general Twitter API error

## Notes

- Non-TTY stdout defaults to YAML automatically
- Tweet and user lists live under `.data`
- Compact mode (`-c`) uses a different minimal format, not this envelope
