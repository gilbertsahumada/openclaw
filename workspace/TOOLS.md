# TOOLS.md - Technical Reference

> **CRITICAL: All X/Twitter search and monitoring must use `twclaw` (Twitter API).**
> Always run the baseline query with `ERC8004` and `ERC-8004` first.
> Do NOT use browser automation for X research workflows.

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
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

# Create a 3-tweet thread draft (split tweets with 4 line breaks)
typefully drafts:create --text $'1/ First tweet in English\n\n\n\n2/ Second tweet in English\n\n\n\n3/ Third tweet in English'

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
6. Preflight checks: English-only text + valid thread split (4 line breaks between tweets)
7. Create draft: typefully drafts:create --text "content"
8. Confirm: "Draft created in Typefully, review it"
9. Gilberts reviews in Typefully -> approves/edits -> publishes
```

### Draft Quality Guardrails (MANDATORY)

- Draft text must be **English only**. Telegram messages can be Spanish, but draft body cannot.
- For threads, never send one big paragraph. Use 4 line breaks between tweets.
- Thread tweets must keep numbering (`1/`, `2/`, `3/`).

### What Goes Through Typefully

- Daily Data Drops
- Fix My Agent invitation tweets
- Educational Threads
- Product Updates
- Any original tweet from @trust8004

---

## Tool 2: twitter-openclaw (Twitter API)

Use `twclaw` for search, reads, and approved write actions on X/Twitter.

```bash
# Verify credentials
node skills/twitter-openclaw/bin/twclaw.js auth-check

# Daily relevance query (single run)
node skills/twitter-openclaw/bin/twclaw.js search "(ERC8004 OR ERC-8004) lang:en -is:retweet" -n 10 --popular --json

# Read one tweet before interacting
node skills/twitter-openclaw/bin/twclaw.js read <tweet-url-or-id>

# Write actions (only after explicit approval from Gilberts)
node skills/twitter-openclaw/bin/twclaw.js reply <tweet-url-or-id> "value-added reply" --yes
node skills/twitter-openclaw/bin/twclaw.js like <tweet-url-or-id> --yes
node skills/twitter-openclaw/bin/twclaw.js retweet <tweet-url-or-id> --yes
```

### Search Workflow (ONE run per day at 10:00 AM Chile, America/Santiago)

1. Run exactly one relevance search (`--popular`) with `(ERC8004 OR ERC-8004) lang:en -is:retweet` and `-n 10`
2. Log those 10 posts in `data/daily/YYYY-MM-DD/engagement_search.md`
3. Prepare one interaction proposal for each post (10/10), replies in **English**
4. Send proposal to Gilberts via Telegram **in Spanish** (see AGENTS.md Campaign 3 for format)
5. **WAIT for Gilberts approval** before executing any write action

### Rules

- `twclaw search --popular` is the default for relevance
- Daily run target is 10 posts from `(ERC8004 OR ERC-8004)` only
- **ALL write actions require Gilberts approval via Telegram first**
- Propose actions via Telegram (in Spanish), wait for approval, then execute
- ALL replies must be in **English**
- Use `--yes` only after explicit approval from Gilberts

---

## Tool 3: Data Logging System

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
- If a log file is missing, create it first with header template, then append entries
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
