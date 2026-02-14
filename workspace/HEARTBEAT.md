# HEARTBEAT.md - Scheduled Tasks

## Every Heartbeat Check

1. **Mentions scan** [Browser] → Log: `data/daily/YYYY-MM-DD/mentions.md`
   Check for new @trust8004 mentions. Reply within 30 min
2. **Keyword monitor** [Browser] → Log: `data/daily/YYYY-MM-DD/engagement_search.md`
   Quick scan for "ERC8004", "ERC-8004" mentions
3. **Reply to Fix My Agent submissions** [Browser] → Log: `data/audits/YYYY-MM-DD_CHAINID-ID.md`
   Audit any pending CHAINID:ID replies

## Morning Routine (8:00-10:00 AM ET)

- [ ] (Monday) **Data cleanup**: Delete `data/daily/` folders older than 14 days, `data/weekly/` older than 8 weeks, audits older than 30 days
- [ ] (Monday) Generate weekly analytics report [Browser] → Log: `data/weekly/YYYY-WNN/analytics_report.md` → Send to Gilberts via Telegram
- [ ] Prepare Daily Data Drop with latest 24h stats [Browser for data] → Log: `data/daily/YYYY-MM-DD/data_drop_draft.md`
- [ ] Send Data Drop preview to Gilberts via Telegram → On approval, create Typefully draft [Typefully]
- [ ] (Monday) Prepare educational thread [Browser for research] → Log: `data/weekly/YYYY-WNN/educational_thread.md` → Create Typefully draft [Typefully]

## Midday Routine (11:00 AM - 1:00 PM ET)

- [ ] Run keyword/hashtag search (ERC8004, AI agents, chain names) [Browser] → Log: `data/daily/YYYY-MM-DD/engagement_search.md`
- [ ] Engage: like, reply, follow relevant accounts [Browser] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Check for trending topics related to on-chain AI [Browser]

## Afternoon/Evening Routine (4:00-7:00 PM ET)

- [ ] (Friday) Prepare weekly product update [Browser for data] → Log: `data/weekly/YYYY-WNN/product_update.md` → Create Typefully draft [Typefully]
- [ ] Prepare Fix My Agent tweet → Log: `data/daily/YYYY-MM-DD/data_drop_draft.md` → Create Typefully draft [Typefully]
- [ ] 7:00 PM: Micro-influencer outreach (identify 2-3, engage thoughtfully) [Browser] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Review day's engagement metrics [Browser]
- [ ] Report daily follower delta to Gilberts via Telegram

## End of Day

- [ ] Respond to any pending replies/mentions [Browser] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Note top performing tweet of the day → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Flag any notable new followers to Gilberts via Telegram
