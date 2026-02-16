# HEARTBEAT.md - Scheduled Tasks

## Every Heartbeat Check

1. **Check for pending Gilberts approvals** — if engagement proposals were sent and Gilberts replied, execute approved actions [twclaw API]
2. **Reply to Fix My Agent submissions** [twclaw API] → Log: `data/audits/YYYY-MM-DD_CHAINID-ID.md`
   Reply only after Gilberts approval

## Morning Routine (8:00-10:00 AM ET)

- [ ] (Monday) **Data cleanup**: Delete `data/daily/` folders older than 14 days, `data/weekly/` older than 8 weeks, audits older than 30 days
- [ ] (Monday) Generate weekly analytics report [twclaw API] → Log: `data/weekly/YYYY-WNN/analytics_report.md` → Send to Gilberts via Telegram
- [ ] Prepare Daily Data Drop with latest 24h stats [twclaw search + trust8004 data] → Log: `data/daily/YYYY-MM-DD/data_drop_draft.md`
- [ ] Send Data Drop preview to Gilberts via Telegram → On approval, create Typefully draft [Typefully]
- [ ] (Monday) Prepare educational thread [twclaw search for research] → Log: `data/weekly/YYYY-WNN/educational_thread.md` → Create Typefully draft [Typefully]

## Midday Routine (10:00 AM Chile, America/Santiago — DAILY ENGAGEMENT SEARCH)

**One search pass per day. Propose to Gilberts. Wait for approval. Execute.**

- [ ] Run twclaw search once with `--popular` and `-n 10`:
  - `(ERC8004 OR ERC-8004) lang:en -is:retweet`
- [ ] Log results → `data/daily/YYYY-MM-DD/engagement_search.md`
- [ ] Keep exactly 10 posts and draft one interaction per post (in English), then send proposal to Gilberts via Telegram (in Spanish)
- [ ] **WAIT for Gilberts approval** — do NOT execute before approval
- [ ] Execute approved actions only [twclaw API] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Confirm to Gilberts: "Listo — 10 posts procesados, una interacción por post"

## Afternoon/Evening Routine (4:00-7:00 PM ET)

- [ ] (Friday) Prepare weekly product update [twclaw search for context] → Log: `data/weekly/YYYY-WNN/product_update.md` → Create Typefully draft [Typefully]
- [ ] Prepare Fix My Agent tweet → Log: `data/daily/YYYY-MM-DD/data_drop_draft.md` → Create Typefully draft [Typefully]
- [ ] Report daily follower delta to Gilberts via Telegram

## End of Day

- [ ] Note top performing tweet of the day → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Flag any notable new followers to Gilberts via Telegram
