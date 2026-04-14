# HEARTBEAT.md - Scheduled Tasks

## Every Heartbeat Check

1. **Check for pending Gilberts approvals** — if a draft was sent and Gilberts approved, post the tweet via twclaw and share URL in Telegram group (`-1003880361581`)

## Scheduled Tasks (America/Santiago)

**IMPORTANT: Before running any task, check if the corresponding file already exists for today in `data/daily/YYYY-MM-DD/`. If it exists, the task is DONE — do NOT re-run it.**

### 9:00 AM — Daily Data Drop (AUTO-PUBLISH, NO APPROVAL)

- [ ] (Monday) **Data cleanup**: Delete `data/daily/` folders older than 14 days
- [ ] Check if `data/daily/YYYY-MM-DD/data_drop_published.md` exists. If NOT: fetch metrics, draft tweet, save draft, POST IMMEDIATELY via twclaw, share URL in Telegram group, notify Gilberts with tweet URL. If exists, skip
- [ ] **On ANY failure** (fetch-metrics error, twclaw error, Telegram error): send full error message to Gilberts via Telegram in Spanish. Format: `❌ Data Drop falló en paso [X]: [error exacto]`. Do NOT retry until next day unless Gilberts asks

### 10:00 AM — Community Engagement

- [ ] Check if `data/daily/YYYY-MM-DD/engagement_actions.md` exists. If NOT, search for ERC-8004 tweets, propose interactions to Gilberts. If exists, skip

### 1:00 PM — Ecosystem Post #1

- [ ] Check if `data/daily/YYYY-MM-DD/ecosystem_post_1.md` exists. If NOT, draft an educational/insight tweet, save, send preview to Gilberts. If exists, skip

### 5:00 PM — Ecosystem Post #2

- [ ] Check if `data/daily/YYYY-MM-DD/ecosystem_post_2.md` exists. If NOT, draft an engagement/opinion tweet, save, send preview to Gilberts. If exists, skip

### After every approved tweet

- [ ] Post via twclaw
- [ ] Share tweet URL in Telegram group `-1003880361581` via `sendMessage` (in English)
- [ ] Confirm to Gilberts

## Anti-Repetition Rules

- Do NOT send the same message to Gilberts more than once per day
- Do NOT re-fetch metrics if you already fetched them today
- If you already sent a preview and are waiting for approval, just wait. Do not resend
- If a task failed and you reported the error, do not retry until the next day unless Gilberts asks
