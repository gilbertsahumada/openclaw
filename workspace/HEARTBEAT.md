# HEARTBEAT.md - Scheduled Tasks

## Every Heartbeat Check

1. **Mentions scan** [x-apify scraper] → Log: `data/daily/YYYY-MM-DD/mentions.md`
   Search: `@trust8004 OR to:trust8004 OR "trust8004"`
2. **Keyword monitor** [x-apify scraper] → Log: `data/daily/YYYY-MM-DD/engagement_search.md`
   Mandatory baseline query: `ERC8004 OR ERC-8004`
3. **Reply to Fix My Agent submissions** [twclaw API] → Log: `data/audits/YYYY-MM-DD_CHAINID-ID.md`
   Reply only after Gilberts approval

## Morning Routine (8:00-10:00 AM ET)

- [ ] (Monday) **Data cleanup**: Delete `data/daily/` folders older than 14 days, `data/weekly/` older than 8 weeks, audits older than 30 days
- [ ] (Monday) Generate weekly analytics report [x-apify scraper + twclaw API] → Log: `data/weekly/YYYY-WNN/analytics_report.md` → Send to Gilberts via Telegram
- [ ] Prepare Daily Data Drop with latest 24h stats [x-apify scraper + trust8004 data] → Log: `data/daily/YYYY-MM-DD/data_drop_draft.md`
- [ ] Send Data Drop preview to Gilberts via Telegram → On approval, create Typefully draft [Typefully]
- [ ] (Monday) Prepare educational thread [x-apify scraper for research] → Log: `data/weekly/YYYY-WNN/educational_thread.md` → Create Typefully draft [Typefully]

## Midday Routine (11:00 AM - 1:00 PM ET)

- [ ] Run keyword/hashtag search [x-apify scraper] → Log: `data/daily/YYYY-MM-DD/engagement_search.md`
      Required query: `ERC8004 OR ERC-8004`
- [ ] Expand search [x-apify scraper]
      Recommended query: `ERC8004 OR ERC-8004 OR #ERC8004 OR "AI agents"`
- [ ] Propose engagement actions (reply/quote/like/retweet) based on results [twclaw API plan] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Execute approved actions only [twclaw API]

## Afternoon/Evening Routine (4:00-7:00 PM ET)

- [ ] (Friday) Prepare weekly product update [x-apify scraper for supporting context] → Log: `data/weekly/YYYY-WNN/product_update.md` → Create Typefully draft [Typefully]
- [ ] Prepare Fix My Agent tweet → Log: `data/daily/YYYY-MM-DD/data_drop_draft.md` → Create Typefully draft [Typefully]
- [ ] 7:00 PM: Micro-influencer outreach [x-apify scraper + twclaw API] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Review day's engagement metrics [x-apify scraper + twclaw API]
- [ ] Report daily follower delta to Gilberts via Telegram

## End of Day

- [ ] Respond to any pending replies/mentions [twclaw API] → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Note top performing tweet of the day → Log: `data/daily/YYYY-MM-DD/engagement_actions.md`
- [ ] Flag any notable new followers to Gilberts via Telegram
