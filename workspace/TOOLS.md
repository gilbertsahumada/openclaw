# TOOLS.md - Technical Reference

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- Connected to a Telegram channel for sharing tweet URLs
- All tweets published directly via twclaw

## Tool 1: twclaw (Twitter/X — Post, Engage, Search)

**Command:** `exec node skills/twitter-openclaw/bin/twclaw.js`

```bash
exec node skills/twitter-openclaw/bin/twclaw.js tweet "text" --yes                        # Post tweet
exec node skills/twitter-openclaw/bin/twclaw.js search "ERC-8004" -n 10 --recent --json   # Search
exec node skills/twitter-openclaw/bin/twclaw.js like <tweet-url> --yes                    # Like
exec node skills/twitter-openclaw/bin/twclaw.js retweet <tweet-url> --yes                 # Retweet
exec node skills/twitter-openclaw/bin/twclaw.js quote <tweet-url> "text" --yes            # Quote (only own tweets or mentions)
exec node skills/twitter-openclaw/bin/twclaw.js read <tweet-url>                          # Read (on-demand)
exec node skills/twitter-openclaw/bin/twclaw.js mentions -n 10 --json                     # Mentions (on-demand)
exec node skills/twitter-openclaw/bin/twclaw.js user-tweets @handle -n 10 --json          # Last N tweets from a specific account (on-demand)
```

Requires `TWITTER_BEARER_TOKEN` and `TWITTER_USER_ID`.
All write actions need `--yes` flag. ALL interactions require Gilberts approval first.

**Do NOT use `reply`** — Twitter API blocks replies to tweets that don't mention us (since Feb 2026). Use `quote` instead.

### Token Refresh

If you get a 401 Unauthorized error, refresh the token first:

```bash
exec node scripts/twitter-refresh-token.mjs
```

Then retry the original command. If refresh also fails, tell Gilberts to re-authorize.

### API Budget (automatic/heartbeat only — Gilberts requests override)

- **1 automatic search/day** (`"ERC-8004"`, `--popular -n 25`). No weekend searches
- **9 automatic actions/day max** (like + retweet combined, across all 3 engagement tiers)
- **NEVER call automatically**: mentions, home, user-tweets — only when Gilberts asks

## Tool 2: Telegram Group (share tweets)

Use the built-in `sendMessage` action to share tweet URLs in the Telegram group:

- `to`: `-1003880361581`
- `content`: the tweet URL + short caption **in English**

**Use after every tweet** to share it with the community.
When Gilberts says "publica en telegram" or "comparte en telegram", send to `-1003880361581`.
All messages to the Telegram group must be **in English** (same as Twitter).

## Tool 3: trust8004 API (Ecosystem Metrics)

```bash
exec node scripts/fetch-metrics.mjs
```

Outputs JSON to stdout. Uses headless Chromium to bypass Vercel bot-protection.

Response fields:

- `totals.registrations24h` / `registrationsDeltaPct` — new agents + % change vs previous day
- `totals.verifiedEndpointsTotal` / `verifiedEndpointsDeltaAbs` — verified endpoints + delta
- `chains[]` — per-chain breakdown: registrations, delta, trend (up/down/stable), verified endpoints
- `topChainsByRegistrations24h` — sorted ranking

Numbers must match the API exactly.

### Changelog

```bash
exec node scripts/fetch-changelog.mjs
```

Returns JSON array of `{ date, version, type, title, description, highlights }`. Use when Gilberts asks for platform updates or to tweet about new releases.

## Tool 4: Data Logging

All data saved in `data/`. Active log: `data/daily/YYYY-MM-DD/data_drop_draft.md`.

Every file starts with `# [Type] — [Date]` header. Keep files lean: bullets, not paragraphs.

**Retention (Monday mornings):** daily >14 days — delete.
**X Policy:** Do NOT store full tweet text. Log only: tweet ID/URL, author handle, 1-line summary.

## Agent Format

**`CHAINID:ID`** — e.g., `8453:42`. URL: `https://www.trust8004.xyz/agents/CHAINID:ID`

| Chain        | ID       | Chain     | ID    |
| ------------ | -------- | --------- | ----- |
| Ethereum     | 1        | BNB Chain | 56    |
| Polygon      | 137      | Optimism  | 10    |
| Arbitrum One | 42161    | Celo      | 42220 |
| Base Sepolia | 84532    | Gnosis    | 100   |
| Eth Sepolia  | 11155111 | Avalanche | 43114 |
| Abstract     | 2741     | Linea     | 59144 |

## ERC-8004 Key Concepts

- **Identity Registry**: On-chain registration per chain, points to agentURI
- **agentURI**: Off-chain JSON with services, endpoints, capabilities
- **Reputation**: feedback.value/valueDecimals scores + tags
- **Endpoint Verification**: trust8004 checks if endpoints respond
- **Trust Signals**: Identity verification, endpoint health, reputation, cross-chain presence

## Content Tips

- Screenshots > raw links for engagement
- Links via quote tweet of your own tweet, never in main tweets
- Use CHAINID:ID format consistently
