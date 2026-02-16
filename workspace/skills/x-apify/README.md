# x-apify

Fetch public X/Twitter data via Apify.

## Requirements

- `python3`
- `APIFY_API_TOKEN` environment variable

Optional:

- `APIFY_ACTOR_ID` (default: `quacker/twitter-scraper`)
- `X_APIFY_CACHE_DIR` (default: `~/.cache/openclaw/x-apify`, fallback: `/tmp/openclaw-x-apify-cache`)

## Quick Start

```bash
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN_HERE"
python3 scripts/fetch_tweets.py --search "OpenAI" --format summary
```

## Commands

- Search: `python3 scripts/fetch_tweets.py --search "query"`
- Search + language filter: `python3 scripts/fetch_tweets.py --search "ERC8004 OR ERC-8004" --lang en`
- User: `python3 scripts/fetch_tweets.py --user "OpenAI,AnthropicAI"`
- Tweet URL: `python3 scripts/fetch_tweets.py --url "https://x.com/user/status/123"`
- Cache stats: `python3 scripts/fetch_tweets.py --cache-stats`
- Clear cache: `python3 scripts/fetch_tweets.py --clear-cache`
