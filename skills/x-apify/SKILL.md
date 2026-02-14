---
name: x-apify
description: Fetch X/Twitter data via Apify API (search tweets, user profiles, specific tweets).
homepage: https://apify.com/
metadata:
  {
    "openclaw":
      {
        "emoji": "X",
        "requires": { "bins": ["python3"], "env": ["APIFY_API_TOKEN"] },
        "optionalEnv": ["APIFY_ACTOR_ID", "X_APIFY_CACHE_DIR"],
      },
  }
---

# x-apify

Fetch public X/Twitter data through Apify actors.

## Why Apify

X/Twitter's official API is expensive and restrictive. Apify provides reliable
access to public tweet data through its actor ecosystem, including residential
proxy support.

## Free tier

- $5/month free credits (no credit card required)
- Cost varies by actor usage
- Good for personal usage and prototyping

## Links

- Apify Pricing: https://apify.com/pricing
- API token: https://console.apify.com/account/integrations
- Twitter Scraper actor: https://apify.com/quacker/twitter-scraper

## Setup

1. Create a free Apify account.
2. Create an API token.
3. Set env vars:

```bash
# ~/.bashrc or ~/.zshrc
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN_HERE"

# Optional: custom actor (default: quacker/twitter-scraper)
export APIFY_ACTOR_ID="quacker/twitter-scraper"

# Optional: custom cache dir
export X_APIFY_CACHE_DIR="/path/to/cache"
```

## Usage

Run from this skill directory:

```bash
python3 {baseDir}/scripts/fetch_tweets.py --search "artificial intelligence"
```

### Search tweets

```bash
python3 {baseDir}/scripts/fetch_tweets.py --search "OpenAI"
python3 {baseDir}/scripts/fetch_tweets.py --search "#AI #MachineLearning"
python3 {baseDir}/scripts/fetch_tweets.py --search "OpenAI" --max-results 10
```

### User profiles

```bash
python3 {baseDir}/scripts/fetch_tweets.py --user "elonmusk"
python3 {baseDir}/scripts/fetch_tweets.py --user "OpenAI,AnthropicAI"
```

### Specific tweet

```bash
python3 {baseDir}/scripts/fetch_tweets.py --url "https://x.com/user/status/123456789"
python3 {baseDir}/scripts/fetch_tweets.py --url "https://twitter.com/user/status/123456789"
```

### Output formats

```bash
python3 {baseDir}/scripts/fetch_tweets.py --search "query" --format json
python3 {baseDir}/scripts/fetch_tweets.py --search "query" --format summary
python3 {baseDir}/scripts/fetch_tweets.py --search "query" --output results.json
```

## Caching

Results are cached locally by default to save Apify credits.

```bash
# Uses cache when available
python3 {baseDir}/scripts/fetch_tweets.py --search "OpenAI"

# Bypass cache
python3 {baseDir}/scripts/fetch_tweets.py --search "OpenAI" --no-cache

# Cache stats
python3 {baseDir}/scripts/fetch_tweets.py --cache-stats

# Clear cache
python3 {baseDir}/scripts/fetch_tweets.py --clear-cache
```

TTL defaults:

- Search results: 1 hour
- User profiles: 24 hours
- Specific tweet lookups: 24 hours
- Default cache dir: `~/.cache/openclaw/x-apify` (fallback to `/tmp/openclaw-x-apify-cache` if needed)

## Notes

- Keep `APIFY_API_TOKEN` secret.
- If you hit a quota/rate limit, retry later or reduce `--max-results`.
- Prefer cache-friendly queries for repeated monitoring tasks.
