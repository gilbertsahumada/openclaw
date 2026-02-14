# TOOLS.md - Technical Reference

> **CRITICAL: All X/Twitter search and monitoring must use scraper (`x-apify`).**
> Always search for `ERC8004` and `ERC-8004` via scraper first.
> Do NOT use browser automation for X research workflows.

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- `x-apify` skill installed — primary X/Twitter scraper
- `twitter-openclaw` skill installed — Twitter API read/write operations
- Typefully skill installed via clawhub

---

## Tool 1: Typefully Skill (Publishing)

Use Typefully for ALL own-content publishing: tweets, threads, data drops.

### Free Tier Limits (CRITICAL)

| Resource        | Limit           |
| --------------- | --------------- |
| Posts per month | **15**          |
| Scheduled posts | **3** at a time |
| Drafts          | **5** at a time |

**Implications:**

- Do NOT create a draft until Gilberts approves the content via Telegram — drafts are scarce
- Before creating a new draft, check `typefully drafts:list` — if there are already 5, wait for Gilberts to publish/delete one
- Prioritize high-impact posts: Data Drops and Educational Threads first, skip low-value posts if nearing the 15/month cap
- Track monthly post count internally — alert Gilberts at 12/15 used

### Key Rule: ALWAYS DRAFT, NEVER PUBLISH DIRECTLY

Every piece of content goes through Typefully as a **draft**. Gilberts approves and publishes from the Typefully UI. NEVER use `--now` flag.

### Commands

The CLI is `typefully`. It uses `:` syntax for subcommands.

```bash
# Verify API auth
typefully config:show

# List connected accounts (get social_set_id)
typefully social-sets:list

# Set default account (so you don't need --social-set-id every time)
typefully config:set-default <social_set_id>

# Create a draft post
typefully drafts:create --text "Your tweet content here"

# Create a draft for specific platform
typefully drafts:create --platform x --text "Your tweet content here"

# Create a draft with scheduling
typefully drafts:create --text "Content" --schedule next-free-slot

# List drafts (check how many exist — max 5 on free tier)
typefully drafts:list

# List scheduled drafts
typefully drafts:list --status scheduled
```

### Publishing Flow

```
1. Prepare content per campaign
2. Save draft locally in data/daily/YYYY-MM-DD/ or data/weekly/YYYY-WNN/
3. Send preview to Gilberts via Telegram
4. Gilberts approves via Telegram
5. Check draft count: typefully drafts:list (max 5 on free tier)
6. Create draft: typefully drafts:create --text "content"
7. Confirm: "Draft created in Typefully, review it"
8. Gilberts reviews in Typefully -> approves/edits -> publishes
```

### What Goes Through Typefully

- Daily Data Drops
- Fix My Agent invitation tweets
- Educational Threads
- Product Updates
- Any original tweet from @trust8004

---

## Tool 2: x-apify (Search Scraper)

Use `x-apify` for ALL keyword discovery and monitoring on X/Twitter.

### Mandatory Keyword Search

```bash
# Required baseline query for monitoring
python3 skills/x-apify/scripts/fetch_tweets.py --search "ERC8004 OR ERC-8004" --max-results 20 --format json
```

### Recommended Searches

```bash
# Extended discovery query
python3 skills/x-apify/scripts/fetch_tweets.py --search "ERC8004 OR ERC-8004 OR #ERC8004 OR \"AI agents\"" --max-results 30 --format summary

# Mention-style scan
python3 skills/x-apify/scripts/fetch_tweets.py --search "@trust8004 OR to:trust8004 OR \"trust8004\"" --max-results 20 --format json

# Inspect account output
python3 skills/x-apify/scripts/fetch_tweets.py --user "OpenAI,AnthropicAI"
```

### Scraper Workflow (ONE run per day at 11:00 AM ET)

1. Run baseline search: `ERC8004 OR ERC-8004`
2. Run extended query + mentions scan
3. Log relevant posts in `data/daily/YYYY-MM-DD/engagement_search.md`
4. Select top ~10 posts, draft replies **in English**
5. Send proposal to Gilberts via Telegram **in Spanish** (see AGENTS.md Campaign 3 for format)
6. **WAIT for Gilberts approval** — do NOT execute any twclaw action before approval

### Caching

```bash
# Cache stats
python3 skills/x-apify/scripts/fetch_tweets.py --cache-stats

# Force fresh pull
python3 skills/x-apify/scripts/fetch_tweets.py --search "ERC8004 OR ERC-8004" --no-cache
```

---

## Tool 3: twitter-openclaw (Twitter API)

Use `twclaw` for API-based reads/writes after scraper discovery.

```bash
# Verify credentials
node skills/twitter-openclaw/bin/twclaw.js auth-check

# Read one tweet before interacting
node skills/twitter-openclaw/bin/twclaw.js read <tweet-url-or-id>

# Write actions (only after explicit approval from Gilberts)
node skills/twitter-openclaw/bin/twclaw.js reply <tweet-url-or-id> "value-added reply" --yes
node skills/twitter-openclaw/bin/twclaw.js like <tweet-url-or-id> --yes
node skills/twitter-openclaw/bin/twclaw.js retweet <tweet-url-or-id> --yes
```

### Rules

- Search/discovery comes from `x-apify` scraper — NEVER use twclaw for search
- **ALL write actions require Gilberts approval via Telegram first**
- Propose actions via Telegram (in Spanish), wait for approval, then execute
- ALL replies must be in **English**
- Use `--yes` only after explicit approval from Gilberts

---

## Tool 4: Data Logging System

ALL searches, analysis, and reports are saved in the `data/` folder with a consistent structure.

### Folder Structure

```
data/
├── daily/
│   └── YYYY-MM-DD/
│       ├── engagement_search.md
│       ├── engagement_actions.md
│       ├── data_drop_draft.md
│       └── mentions.md
├── weekly/
│   └── YYYY-WNN/
│       ├── analytics_report.md
│       ├── educational_thread.md
│       └── product_update.md
├── audits/
│   └── YYYY-MM-DD_CHAINID-ID.md
└── README.md
```

### Naming Conventions

- **Daily folders**: `YYYY-MM-DD` (e.g., `2026-02-14`)
- **Weekly folders**: `YYYY-WNN` ISO week (e.g., `2026-W07`)
- **Files**: `type_subtype.md` in snake_case
- **Audits**: `YYYY-MM-DD_CHAINID-ID.md` (e.g., `2026-02-14_8453-42.md`)

### File Header Template

Every data file MUST start with:

```markdown
# [Type] — [Date]

## Generated: YYYY-MM-DD HH:MM ET

[content]
```

### What Gets Logged

| Activity                    | File                       | Folder              |
| --------------------------- | -------------------------- | ------------------- |
| Keyword search results on X | `engagement_search.md`     | `daily/YYYY-MM-DD/` |
| Likes, replies, follows     | `engagement_actions.md`    | `daily/YYYY-MM-DD/` |
| Data Drop content           | `data_drop_draft.md`       | `daily/YYYY-MM-DD/` |
| Mentions found              | `mentions.md`              | `daily/YYYY-MM-DD/` |
| Weekly analytics report     | `analytics_report.md`      | `weekly/YYYY-WNN/`  |
| Educational thread content  | `educational_thread.md`    | `weekly/YYYY-WNN/`  |
| Product update content      | `product_update.md`        | `weekly/YYYY-WNN/`  |
| Fix My Agent audit          | `YYYY-MM-DD_CHAINID-ID.md` | `audits/`           |

### Rules

- Create daily/weekly folders on demand (don't pre-create)
- Always use the header template
- Append to existing files if the same activity runs multiple times in a day
- Keep files **precise and concise** — bullet points over paragraphs, numbers over narrative

### Data Hygiene — Keep It Lean

- **Search logs**: Top 10 relevant results max — username, link, 1-line summary. Skip irrelevant/spam
- **Action logs**: One line per action: `[like/reply/follow] @user — reason`
- **Drafts**: Final text only — no brainstorming, no alternatives
- **Audits**: 10-15 lines max per file
- **NO** raw HTML, full page dumps, or embedded screenshots
- **NO** duplicate entries — check before appending

### Retention & Cleanup (Monday mornings)

- Delete `daily/` folders older than **14 days**
- Delete `weekly/` folders older than **8 weeks**
- Delete audit files older than **30 days**

---

## Agent Identifier Format

**Format: `CHAINID:ID`**

- `CHAINID` = numeric chain ID (e.g., 1 for Ethereum, 137 for Polygon, 42161 for Arbitrum)
- `ID` = numeric agent identifier within that chain's registry
- Example: `2741:615`

**Platform URL: `https://www.trust8004.xyz/agents/CHAINID:ID`**

## Common Chain IDs

| Chain    | ID    | Status    |
| -------- | ----- | --------- |
| Ethereum | 1     | Supported |
| Polygon  | 137   | Supported |
| Arbitrum | 42161 | Supported |
| Base     | 8453  | Supported |
| Optimism | 10    | Supported |

## ERC-8004 Key Concepts

### Identity Registry

- Each chain has a registry contract where agents register
- Registration includes on-chain metadata pointing to an agentURI

### agentURI

- Off-chain JSON metadata describing the agent
- Contains: services list, endpoints, description, capabilities
- Common issues: 404 errors, invalid JSON, missing fields

### Reputation Signals

- **feedback.value / valueDecimals**: Numeric reputation score
- **Tags**: Categorical labels (e.g., "ai-oracle", "defi-agent")
- Higher scores + more feedback entries = higher trust

### Endpoint Verification

- trust8004 checks if declared endpoints actually respond
- Verified endpoints = higher trust signal
- Common failures: timeouts, 404s, SSL errors

### Trust Signals (what trust8004 provides)

- Identity verification: Is the agent properly registered?
- Endpoint health: Are declared services reachable?
- Reputation aggregation: What does the community say?
- Cross-chain presence: Is the agent on multiple chains?

## Content Guidelines

- Screenshots of scanner results perform better than raw links
- Always link to trust8004.xyz in replies, not in main tweets
- When citing data, be prepared to explain methodology if asked
- Use CHAINID:ID format consistently in all content
