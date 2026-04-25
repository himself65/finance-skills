# Claude API Proxy (Bedrock) Reference

Proxy for the Anthropic Messages API via AWS Bedrock. Lets team members use Claude Code (and any Anthropic SDK) without individual AWS credentials.

## Endpoint

```
POST https://api.funda.ai/v1/claude/v1/messages
```

Base URL (for Anthropic SDK configuration): `https://api.funda.ai/v1/claude`

## Authentication

Standard Funda auth: `Authorization: Bearer <FUNDA_API_KEY>`. The Anthropic SDK's `x-api-key` header is automatically converted to `Authorization: Bearer` by the proxy middleware.

## Response format

Responses follow the **standard Anthropic Messages API format** — they are *not* wrapped in `{"code","message","data"}`. Streaming (SSE) is fully supported.

## Model mapping

| Anthropic model ID | Bedrock inference profile |
|---|---|
| `claude-opus-4-6` | `us.anthropic.claude-opus-4-6-v1` |
| `claude-sonnet-4-6` | `us.anthropic.claude-sonnet-4-6` |
| `claude-opus-4-5-20251101` | `us.anthropic.claude-opus-4-5-20251101-v1:0` |
| `claude-sonnet-4-5-20250929` | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| `claude-haiku-4-5-20251001` | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |

Unrecognized model IDs are rejected by Bedrock.

## SDK usage

```python
from anthropic import Anthropic

client = Anthropic(
    base_url="https://api.funda.ai/v1/claude",
    api_key="<FUNDA_API_KEY>",
)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

Streaming:

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

Refer to the [Anthropic Messages API docs](https://docs.anthropic.com/en/api/messages) for full request/response schemas.
