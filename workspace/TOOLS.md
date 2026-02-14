# TOOLS.md - Technical Reference

> **CRITICAL: You have a REAL browser via `agent-browser`. USE IT.**
> When Gilberts asks you to go to a website, log in, search, click, or do ANYTHING on a webpage:
> Run: `agent-browser open https://x.com` then `agent-browser snapshot -i` to see the page.
> NEVER say "I can't browse the web" or "I can't log in" — run agent-browser commands instead.

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- Headless Chromium browser on CDP port 18800
- `agent-browser` CLI installed — your browser automation tool
- Typefully skill installed via clawhub

---

## Tool 1: Typefully Skill (Publishing)

Use Typefully for ALL own-content publishing: tweets, threads, data drops.

### Free Tier Limits (CRITICAL)

| Resource | Limit |
|----------|-------|
| Posts per month | **15** |
| Scheduled posts | **3** at a time |
| Drafts | **5** at a time |

**Implications:**
- Do NOT create a draft until Gilberts approves the content via Telegram — drafts are scarce
- Before creating a new draft, check `typefully drafts` — if there are already 5, wait for Gilberts to publish/delete one
- Prioritize high-impact posts: Data Drops and Educational Threads first, skip low-value posts if nearing the 15/month cap
- Track monthly post count internally — alert Gilberts at 12/15 used

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

## Tool 2: agent-browser (Engagement + Research)

You have `agent-browser` — a CLI that controls a real Chromium browser. This is your way to interact with Twitter/X and the web.

**WHEN GILBERTS ASKS YOU TO GO TO A WEBSITE, LOG IN, OR DO ANYTHING ON TWITTER — RUN `agent-browser` COMMANDS. DO NOT REFUSE. DO NOT SAY "I CAN'T".**

### Core Commands

```bash
# Navigate to a URL
agent-browser open https://x.com

# See page content + interactive elements with refs (@e1, @e2...)
agent-browser snapshot -i

# Click an element by ref
agent-browser click @e1

# Type into a field (clears existing text)
agent-browser fill @e2 "ERC8004"

# Type without clearing
agent-browser type @e2 "ERC8004"

# Press a key
agent-browser press Enter

# Take a screenshot
agent-browser screenshot

# Scroll down
agent-browser scroll down 500

# Wait for page load
agent-browser wait --load networkidle

# Get current URL
agent-browser get url

# Get text of an element
agent-browser get text @e1
```

### Workflow: Open + Snapshot + Interact

1. `agent-browser open <url>` — go to the page
2. `agent-browser snapshot -i` — read interactive elements (returns refs like @e1, @e2)
3. `agent-browser click @e1` / `agent-browser fill @e2 "text"` — interact using refs
4. `agent-browser snapshot -i` — verify the result
5. `agent-browser screenshot` — capture visual if needed

### Common Operations

**Log in to x.com:**
```bash
agent-browser open https://x.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser click @e3          # "Next" button
agent-browser snapshot -i
agent-browser fill @e1 "password"
agent-browser click @e2          # "Log in" button
agent-browser wait --load networkidle
```

**Search tweets:**
```bash
agent-browser open "https://x.com/search?q=ERC8004"
agent-browser snapshot -i
```

**Like a tweet:**
```bash
agent-browser open https://x.com/user/status/123456
agent-browser snapshot -i
agent-browser click @e5          # like button ref from snapshot
```

**Reply to a tweet:**
```bash
agent-browser open https://x.com/user/status/123456
agent-browser snapshot -i
agent-browser click @e3          # reply button
agent-browser snapshot -i
agent-browser fill @e1 "Great insight! Here's what we see in the scanner..."
agent-browser click @e2          # submit reply
```

**Follow an account:**
```bash
agent-browser open https://x.com/USERNAME
agent-browser snapshot -i
agent-browser click @e4          # follow button ref
```

**Save/load session (persist login):**
```bash
agent-browser state save /home/node/.openclaw/browser/x-session.json
agent-browser state load /home/node/.openclaw/browser/x-session.json
```

### Do NOT Use Browser For

- Publishing own tweets (use Typefully instead)

### Browser Tips

- Always `snapshot -i` after navigating — refs change on every page load
- Use `fill` instead of `type` for input fields (clears existing text)
- If an element is not found, re-snapshot to get updated refs
- Use `wait --load networkidle` after login or form submissions
- Save session state after login so you don't have to re-authenticate

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
