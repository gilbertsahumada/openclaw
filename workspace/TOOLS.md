# TOOLS.md - Technical Reference

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- Headless Chromium browser running locally (CDP on port 18800)
- Typefully skill installed via clawhub

---

## Tool 1: Typefully Skill (Publishing)

Use Typefully for ALL own-content publishing: tweets, threads, data drops.

### Key Rule: ALWAYS DRAFT, NEVER PUBLISH DIRECTLY

Every piece of content goes through Typefully as a **draft**. Gilberts approves and publishes from the Typefully UI. NEVER use `--now` flag.

### Commands

| Command | Purpose |
|---------|---------|
| `typefully create-draft "content"` | Create a new draft tweet |
| `typefully create-draft "content" --social-set-id ID` | Create draft for specific account |
| `typefully create-draft "content" --thread-of N` | Create a thread with N tweets |
| `typefully drafts` | List existing drafts |
| `typefully social-sets` | List connected social accounts (get social-set-id) |
| `typefully me` | Verify API authentication |

### Publishing Flow

```
1. Prepare content per campaign
2. Save draft locally in data/daily/YYYY-MM-DD/ or data/weekly/YYYY-WNN/
3. Send preview to Gilberts via Telegram
4. Gilberts approves via Telegram
5. Execute: typefully create-draft "content" --social-set-id ID
6. Confirm: "Draft created in Typefully, review it"
7. Gilberts reviews in Typefully -> approves/edits -> publishes
```

### What Goes Through Typefully

- Daily Data Drops
- Fix My Agent invitation tweets
- Educational Threads
- Product Updates
- Any original tweet from @trust8004

---

## Tool 2: Browser (Engagement + Research)

You have a **built-in browser tool** that controls a headless Chromium instance. Use it for engagement and research — NOT for publishing own tweets.

### Use For

1. **Search**: Navigate to `x.com/search?q=KEYWORD` to find relevant posts
2. **Engage**: Like, reply, retweet, follow — all via browser interactions on x.com
3. **Read timelines**: Scroll and read feed, mentions, notifications
4. **Take screenshots**: Capture scanner results or agent pages
5. **Research**: Navigate trust8004.xyz for agent data, scanner screenshots
6. **Audit agents**: Visit `trust8004.xyz/agents/CHAINID:ID` for Fix My Agent audits

### Common Operations

| Action | How |
|--------|-----|
| Search tweets | Navigate to `x.com/search?q=KEYWORD` |
| Check mentions | Navigate to `x.com/notifications/mentions` |
| Reply to a tweet | Navigate to tweet URL, click reply, type, submit |
| Like a tweet | Navigate to tweet, click like button |
| Follow an account | Navigate to profile, click follow |
| View profile | Navigate to `x.com/USERNAME` |
| Scanner data | Navigate to `trust8004.xyz/agents/CHAINID:ID` |

### Do NOT Use Browser For

- Publishing own tweets (use Typefully)
- Composing original posts on x.com

### Browser Tips

- Wait for pages to fully load before interacting
- Use CSS selectors or text content to find elements
- Take screenshots to verify page state when debugging
- If a page doesn't load, retry after a short wait

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
Generated: YYYY-MM-DD HH:MM ET
---
[content]
```

### What Gets Logged

| Activity | File | Folder |
|----------|------|--------|
| Keyword search results on X | `engagement_search.md` | `daily/YYYY-MM-DD/` |
| Likes, replies, follows | `engagement_actions.md` | `daily/YYYY-MM-DD/` |
| Data Drop content | `data_drop_draft.md` | `daily/YYYY-MM-DD/` |
| Mentions found | `mentions.md` | `daily/YYYY-MM-DD/` |
| Weekly analytics report | `analytics_report.md` | `weekly/YYYY-WNN/` |
| Educational thread content | `educational_thread.md` | `weekly/YYYY-WNN/` |
| Product update content | `product_update.md` | `weekly/YYYY-WNN/` |
| Fix My Agent audit | `YYYY-MM-DD_CHAINID-ID.md` | `audits/` |

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

| Chain | ID | Status |
|-------|-----|--------|
| Ethereum | 1 | Supported |
| Polygon | 137 | Supported |
| Arbitrum | 42161 | Supported |
| Base | 8453 | Supported |
| Optimism | 10 | Supported |

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
