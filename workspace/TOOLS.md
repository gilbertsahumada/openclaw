# TOOLS.md - Technical Reference

> **CRITICAL: All X/Twitter search and monitoring must use `twclaw` (Twitter API).**
> Do NOT use browser automation for X research workflows.

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- `twitter-openclaw` skill installed — Twitter API read/write
- Typefully skill installed via clawhub

## Tool 1: Typefully (Publishing)

### Free Tier Limits

| Resource    | Limit           |
| ----------- | --------------- |
| Posts/month | **15**          |
| Scheduled   | **3** at a time |
| Drafts      | **5** at a time |

- Do NOT create draft until Gilberts approves via Telegram
- Check `typefully drafts:list` before creating — max 5
- Alert Gilberts at 12/15 posts used
- ALWAYS draft, NEVER publish directly. NEVER use `--now`

### Commands

```bash
typefully config:show
typefully social-sets:list
typefully config:set-default <social_set_id>
typefully drafts:create --text "Tweet content"
typefully drafts:create --text $'1/ First\n\n\n\n2/ Second\n\n\n\n3/ Third'
typefully drafts:list
typefully drafts:list --status scheduled
```

### Draft Rules

- Draft text must be **English only**
- Threads: 4 line breaks between tweets, numbered `1/`, `2/`, `3/`
- Save locally in `data/daily/YYYY-MM-DD/` or `data/weekly/YYYY-WNN/` before creating draft

## Tool 2: twclaw (Twitter API)

```bash
# Auth check
node skills/twitter-openclaw/bin/twclaw.js auth-check

# Daily search (ONE run at 10:00 AM Chile)
node skills/twitter-openclaw/bin/twclaw.js search "(ERC8004 OR ERC-8004) lang:en -is:retweet" -n 10 --popular --json

# Read a tweet
node skills/twitter-openclaw/bin/twclaw.js read <tweet-url-or-id>

# Write actions (ONLY after Gilberts approval)
node skills/twitter-openclaw/bin/twclaw.js reply <id> "reply text" --yes
node skills/twitter-openclaw/bin/twclaw.js like <id> --yes
node skills/twitter-openclaw/bin/twclaw.js retweet <id> --yes
```

- `--popular` is default for relevance
- **ALL writes require Gilberts approval first**
- ALL replies in **English**, proposals to Gilberts in **Spanish**

## Tool 3: Data Logging

All data saved in `data/` — see `data/README.md` for full structure.

| Activity       | File                       | Folder              |
| -------------- | -------------------------- | ------------------- |
| Search results | `engagement_search.md`     | `daily/YYYY-MM-DD/` |
| Actions done   | `engagement_actions.md`    | `daily/YYYY-MM-DD/` |
| Data Drop      | `data_drop_draft.md`       | `daily/YYYY-MM-DD/` |
| Fix My Agent   | `fix_my_agent_draft.md`    | `daily/YYYY-MM-DD/` |
| Analytics      | `analytics_report.md`      | `weekly/YYYY-WNN/`  |
| Edu thread     | `educational_thread.md`    | `weekly/YYYY-WNN/`  |
| Product update | `product_update.md`        | `weekly/YYYY-WNN/`  |
| Audit          | `YYYY-MM-DD_CHAINID-ID.md` | `audits/`           |

Every file starts with `# [Type] — [Date]` header. Keep files lean: bullets, not paragraphs.

**Retention (Monday mornings):** daily >14 days, weekly >8 weeks, audits >30 days — delete.
**X Policy:** Do NOT store full tweet text. Log only: tweet ID/URL, author handle, 1-line summary. If notified a tweet was deleted, remove its reference from logs within 24h.

## Agent Format

**`CHAINID:ID`** — e.g., `8453:42`. URL: `https://www.trust8004.xyz/agents/CHAINID:ID`

| Chain    | ID    | Chain    | ID   |
| -------- | ----- | -------- | ---- |
| Ethereum | 1     | Base     | 8453 |
| Polygon  | 137   | Optimism | 10   |
| Arbitrum | 42161 |          |      |

## ERC-8004 Key Concepts

- **Identity Registry**: On-chain registration per chain, points to agentURI
- **agentURI**: Off-chain JSON with services, endpoints, capabilities
- **Reputation**: feedback.value/valueDecimals scores + tags
- **Endpoint Verification**: trust8004 checks if endpoints respond
- **Trust Signals**: Identity verification, endpoint health, reputation, cross-chain presence

## Content Tips

- Screenshots > raw links for engagement
- Links in replies, never in main tweets
- Use CHAINID:ID format consistently
