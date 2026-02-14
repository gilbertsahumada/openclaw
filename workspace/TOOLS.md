# TOOLS.md - Technical Reference

> **CRITICAL: You have a tool called `browser`. It is a REAL Chromium browser. USE IT.**
> When Gilberts asks you to go to a website, log in, search, click, or interact with ANY webpage — call the `browser` tool.
> Example: `browser({ "action": "navigate", "targetUrl": "https://x.com", "profile": "openclaw" })`
> NEVER say "I can't browse the web" or "I can't log in" — call the `browser` tool instead.

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- **Headless Chromium browser running locally (CDP on port 18800) — USE IT**
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

## Tool 2: Browser (Engagement + Research)

You have a tool called **`browser`**. It controls a real headless Chromium instance. This is your ONLY way to interact with Twitter/X and the web.

**WHEN GILBERTS ASKS YOU TO GO TO A WEBSITE, LOG IN, SEARCH, OR DO ANYTHING ON TWITTER — CALL THE `browser` TOOL. DO NOT REFUSE. DO NOT SAY "I CAN'T". JUST CALL IT.**

### How to Call the Browser Tool

The tool name is `browser`. Always use `profile: "openclaw"`.

**Go to a URL:**
```json
{ "action": "navigate", "targetUrl": "https://x.com", "profile": "openclaw" }
```

**See what's on the page (get page content):**
```json
{ "action": "snapshot", "profile": "openclaw" }
```

**Take a screenshot:**
```json
{ "action": "screenshot", "profile": "openclaw" }
```

**Click an element (use ref from snapshot):**
```json
{ "action": "act", "request": { "kind": "click", "ref": "e12" }, "profile": "openclaw" }
```

**Type text into a field:**
```json
{ "action": "act", "request": { "kind": "type", "text": "ERC8004", "ref": "e5" }, "profile": "openclaw" }
```

**Press a key (e.g. Enter):**
```json
{ "action": "act", "request": { "kind": "press", "key": "Enter" }, "profile": "openclaw" }
```

**List open tabs:**
```json
{ "action": "tabs", "profile": "openclaw" }
```

### Workflow: Navigate + Read + Interact

1. `navigate` to the URL
2. `snapshot` to read the page content and get element refs
3. `act` with `click`/`type`/`press` using refs from the snapshot
4. `snapshot` again to verify the result
5. `screenshot` if you need a visual capture

### Common Operations

| Task | Steps |
|------|-------|
| **Log in to x.com** | navigate to `https://x.com/login` → snapshot → type username → click next → type password → click login |
| **Search tweets** | navigate to `https://x.com/search?q=ERC8004` → snapshot to read results |
| **Like a tweet** | navigate to tweet URL → snapshot → click like button ref |
| **Reply to a tweet** | navigate to tweet URL → snapshot → click reply → type text → click submit |
| **Follow an account** | navigate to `https://x.com/USERNAME` → snapshot → click follow button ref |
| **Check mentions** | navigate to `https://x.com/notifications/mentions` → snapshot |
| **Scanner data** | navigate to `https://www.trust8004.xyz/agents/CHAINID:ID` → snapshot |
| **Take screenshot** | navigate to URL → screenshot |

### Do NOT Use Browser For

- Publishing own tweets (use Typefully instead)

### Browser Tips

- Always `snapshot` after navigating to read the page before interacting
- Use refs from snapshot output (e.g. `e12`, `e5`) to target elements in `act` calls
- If a page doesn't load, wait briefly and retry
- Take screenshots to verify visual state when debugging

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
