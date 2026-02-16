#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

WITH_LIVE=0
WITH_DOCKER=0

usage() {
  cat <<'USAGE'
Smoke test for social workflow (x-apify + twclaw).

Usage:
  scripts/smoke-social.sh [--with-live] [--with-docker]

Options:
  --with-live    Run live API checks when tokens are present.
  --with-docker  Validate docker-compose interpolation/config for gateway.
  -h, --help     Show this help.

Environment (optional for --with-live):
  APIFY_API_TOKEN
  TWITTER_BEARER_TOKEN
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-live)
      WITH_LIVE=1
      ;;
    --with-docker)
      WITH_DOCKER=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

log() {
  printf '[smoke-social] %s\n' "$*"
}

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 2
  fi
}

need_file() {
  if [[ ! -f "$1" ]]; then
    echo "Missing required file: $1" >&2
    exit 2
  fi
}

parse_json_file() {
  node -e 'const fs=require("node:fs"); JSON.parse(fs.readFileSync(process.argv[1],"utf8"));' "$1"
}

need_cmd python3
need_cmd node

X_APIFY_ROOT="skills/x-apify"
X_APIFY_WS="workspace/skills/x-apify"
TWC_ROOT="skills/twitter-openclaw"
TWC_WS="workspace/skills/twitter-openclaw"

need_file "$X_APIFY_ROOT/scripts/fetch_tweets.py"
need_file "$X_APIFY_WS/scripts/fetch_tweets.py"
need_file "$TWC_ROOT/bin/twclaw.js"
need_file "$TWC_WS/bin/twclaw.js"

log "Checking x-apify CLI shape and Python syntax"
python3 "$X_APIFY_WS/scripts/fetch_tweets.py" --help >/tmp/smoke-social-x-apify-help.txt
grep -q -- '--lang' /tmp/smoke-social-x-apify-help.txt
python3 -m py_compile \
  "$X_APIFY_WS/scripts/fetch_tweets.py" \
  "$X_APIFY_WS/scripts/cache.py" \
  "$X_APIFY_WS/scripts/config.py"

log "Checking cache command in writable temp dir"
X_APIFY_CACHE_DIR="$(mktemp -d)/x-apify-cache" \
  python3 "$X_APIFY_WS/scripts/fetch_tweets.py" --cache-stats >/tmp/smoke-social-x-apify-cache.json
parse_json_file /tmp/smoke-social-x-apify-cache.json

log "Checking twclaw CLI shape and Node syntax"
node --check "$TWC_WS/bin/twclaw.js"
node "$TWC_WS/bin/twclaw.js" --help >/tmp/smoke-social-twclaw-help.txt
grep -q 'twclaw search "query"' /tmp/smoke-social-twclaw-help.txt

log "Checking write safety guard (non-interactive mode should block without --yes)"
if node "$TWC_WS/bin/twclaw.js" reply 123 "smoke check" >/tmp/smoke-social-write.out 2>/tmp/smoke-social-write.err; then
  echo "Write safety check failed: command unexpectedly succeeded" >&2
  exit 1
fi
grep -qi "non-interactive mode" /tmp/smoke-social-write.err

log "Checking workspace policy docs"
grep -q 'ERC8004 OR ERC-8004' workspace/TOOLS.md
grep -q 'x-apify' workspace/HEARTBEAT.md
grep -q 'x-apify scraper' workspace/AGENTS.md

if [[ "$WITH_LIVE" -eq 1 ]]; then
  log "Running live checks"

  if [[ -n "${APIFY_API_TOKEN:-}" ]]; then
    live_apify_out="$(mktemp)"
    X_APIFY_CACHE_DIR="$(mktemp -d)/x-apify-live-cache" \
      python3 "$X_APIFY_WS/scripts/fetch_tweets.py" \
        --search "ERC8004 OR ERC-8004" \
        --lang en \
        --max-results 5 \
        --format json \
        --output "$live_apify_out"
    parse_json_file "$live_apify_out"
    log "Live Apify check OK"
  else
    log "Skipping live Apify check (APIFY_API_TOKEN not set)"
  fi

  if [[ -n "${TWITTER_BEARER_TOKEN:-}" ]]; then
    node "$TWC_WS/bin/twclaw.js" auth-check >/tmp/smoke-social-tw-auth.json
    node "$TWC_WS/bin/twclaw.js" search "ERC8004 OR ERC-8004" -n 3 --json >/tmp/smoke-social-tw-search.json
    parse_json_file /tmp/smoke-social-tw-search.json
    log "Live Twitter check OK"
  else
    log "Skipping live Twitter check (TWITTER_BEARER_TOKEN not set)"
  fi
fi

if [[ "$WITH_DOCKER" -eq 1 ]]; then
  need_cmd docker
  log "Validating docker-compose config"
  OPENCLAW_GATEWAY_TOKEN=dummy \
  OPENAI_API_KEY=dummy \
  TELEGRAM_BOT_TOKEN=dummy \
  TYPEFULLY_API_KEY=dummy \
  TWITTER_BEARER_TOKEN=dummy \
  TWITTER_API_KEY=dummy \
  TWITTER_API_SECRET=dummy \
  APIFY_API_TOKEN=dummy \
  docker compose config >/tmp/smoke-social-compose.yaml

  grep -q 'X_APIFY_CACHE_DIR: /home/node/.openclaw/workspace/data/.cache/x-apify' /tmp/smoke-social-compose.yaml
  grep -q '\$\$daily_date' docker-compose.yml
  grep -q '\$\$daily_dir' docker-compose.yml
  log "Docker compose check OK"
fi

log "Smoke test passed"
