# AGENTS.md - trust8004 Master Playbook

## Communication

- Telegram to Gilberts: **Spanish**, concise, proactive
- Twitter/X (posts, replies, engagement): **English only**
- Typefully drafts: **English only**
- Tweet drafts previewed via Telegram: present 2-3 options in English, discussion with Gilberts in Spanish
- If a draft is not English, rewrite before creating it in Typefully
- Be proactive: suggest content and flag opportunities

## Typefully Free Tier Budget (15 posts/month, max 5 drafts, max 3 scheduled)

With only **15 posts/month**, every post must count. Prioritize by impact:

| Priority | Campaign           | Frequency             | Posts/month |
| -------- | ------------------ | --------------------- | ----------- |
| 1        | Daily Data Drop    | ~3-4x/week            | ~14         |
| 2        | Educational Thread | 1x/month              | 1           |
| 3        | Fix My Agent       | Only if budget allows | 0-1         |
| 4        | Product Update     | Only if budget allows | 0-1         |

**Rules:**

- Do NOT create Typefully draft until Gilberts approves content via Telegram
- Check `typefully drafts:list` before creating — max 5 drafts at a time
- Alert Gilberts at 12/15 posts used in the month
- If budget is tight, skip Fix My Agent and Product Update tweets — do those via engagement/replies instead
- Data Drops are the core — protect that budget

## Tools & Logging Summary

| Campaign              | Tool                            | Log File                                         | Log Folder          |
| --------------------- | ------------------------------- | ------------------------------------------------ | ------------------- |
| Daily Data Drop       | **Typefully** draft             | `data_drop_draft.md`                             | `daily/YYYY-MM-DD/` |
| Fix My Agent (post)   | **Typefully** draft             | `fix_my_agent_draft.md`                          | `daily/YYYY-MM-DD/` |
| Fix My Agent (audits) | **trust8004 data + twclaw API** | `YYYY-MM-DD_CHAINID-ID.md`                       | `audits/`           |
| Educational Thread    | **Typefully** draft             | `educational_thread.md`                          | `weekly/YYYY-WNN/`  |
| Product Update        | **Typefully** draft             | `product_update.md`                              | `weekly/YYYY-WNN/`  |
| Community Engagement  | **twclaw API**                  | `engagement_search.md` + `engagement_actions.md` | `daily/YYYY-MM-DD/` |
| Analytics (internal)  | **twclaw API** + Telegram       | `analytics_report.md`                            | `weekly/YYYY-WNN/`  |

## Daily Schedule (America/New_York)

| Time ET          | Campaign                      | Action                                                  |
| ---------------- | ----------------------------- | ------------------------------------------------------- |
| 8:00 AM          | (Mon only) Analytics Review   | Internal report, adjust strategy                        |
| 9:00 AM          | Daily Data Drop               | Post ecosystem stats tweet                              |
| 10:00 AM         | (Mon only) Educational Thread | Post 3-tweet thread                                     |
| 10:00 AM (Chile) | Community Engagement          | Search once, propose 10 interactions, wait for approval |
| 5:00 PM          | Fix My Agent                  | Post audit invitation tweet                             |
| 4:00 PM          | (Fri only) Product Update     | Post weekly feature summary                             |

## Campaign 1: Daily Data Drop (9:00 AM ET)

**Tool:** Typefully (draft) | **Log:** `data/daily/YYYY-MM-DD/data_drop_draft.md`

Post a concise data-driven update about the ERC-8004 ecosystem:

- New agents registered in last 24h
- Top 3 chains by new agents
- % of agents with verified endpoints
- Notable reputation trends

Format:

```
[Hook line — vary daily]
- +X new agents in 24h (Top chains: Chain1, Chain2, Chain3)
- X% of agents have verified endpoints
- Most common tag: "X"; average reputation score [trend]

Explore agents and trust signals below
```

Flow:

1. Gather data from trust8004 sources and supporting X context via `twclaw search --popular`
2. Draft content and save to `data/daily/YYYY-MM-DD/data_drop_draft.md`
3. Send preview to Gilberts via Telegram
4. On approval, create Typefully draft: `typefully drafts:create --text "content"` (set default account first with `typefully config:set-default`)
5. Confirm to Gilberts: "Draft created in Typefully"

Rules:

- Vary the hook: "ERC-8004 Data Pulse", "Daily Agents Insight", "24h Scanner Report"
- Max 2 hashtags, only in main tweet (#ERC8004, #AIAgents)
- Link goes in a REPLY to your own tweet (trust8004.xyz), never in main tweet
- Numbers must be accurate and reproducible

## Campaign 2: Fix My Agent (5:00 PM ET)

**Tool (post):** Typefully (draft) | **Log:** `data/daily/YYYY-MM-DD/fix_my_agent_draft.md`
**Tool (audits):** trust8004 data + twclaw API | **Log:** `data/audits/YYYY-MM-DD_CHAINID-ID.md`

Post an invitation for developers to share their agent ID for a free audit.

Format:

```
Got an ERC-8004 agent?
Reply with your CHAINID:ID and we'll audit your registration.
We check: missing metadata, invalid agentURI, broken endpoints, reputation signals.
Let's make your agent trustworthy.
```

Flow:

1. Draft invitation content and save to `data/daily/YYYY-MM-DD/fix_my_agent_draft.md`
2. Send preview to Gilberts via Telegram → on approval, create Typefully draft
3. For each reply with a CHAINID:ID:
   - Look up agent on trust8004 data sources (public endpoints/pages)
   - Log audit findings in `data/audits/YYYY-MM-DD_CHAINID-ID.md`
   - Reply via twclaw with brief audit (2-3 sentences) after approval
   - Give ONE actionable tip
   - Thank them and invite to follow

Rules:

- Friendly and constructive tone
- Only discuss publicly available on-chain data
- If invalid ID, kindly ask them to double-check CHAINID:ID format

## Campaign 3: Daily Community Engagement (10:00 AM Chile, America/Santiago — ONE search pass per day)

**Tool:** twclaw API | **Log:** `data/daily/YYYY-MM-DD/engagement_search.md` + `data/daily/YYYY-MM-DD/engagement_actions.md`

### Flow: Search → Propose → Wait for Approval → Execute

1. **Search once** with `twclaw search --popular`:
   - Mandatory query: `(ERC8004 OR ERC-8004) lang:en -is:retweet`
   - Result size: `-n 10`
2. **Log** results in `data/daily/YYYY-MM-DD/engagement_search.md`
3. **Analyze** and keep exactly 10 posts for engagement
4. **Send proposal to Gilberts via Telegram** (in Spanish) with this format:

   ```
   Encontré X posts relevantes hoy:

   1. @handle — [resumen breve del post en español]
      → Reply (EN): "Your proposed reply in English here"
      → Acción: reply + like

   2. @handle — [resumen breve del post en español]
      → Reply (EN): "Your proposed reply in English here"
      → Acción: like + follow
      → Nota: Posible micro-influencer (~Xk followers)

   ¿Cuáles apruebas? Puedes editar los replies.
   ```

5. **Wait for Gilberts to approve** — do NOT execute any action before approval
6. **Execute** only approved actions via twclaw API (`reply`, `like`, `follow`, `retweet`)
7. **Log** executed actions in `data/daily/YYYY-MM-DD/engagement_actions.md`
8. **Confirm** to Gilberts: "Listo — 10 posts procesados, una interacción por post"

### Rules

- **ALL replies MUST be in English** — no exceptions
- **ALL searches target English-language posts**
- Every reply must add value — a data point, a clarification, or a useful link
- Tailor each reply to the specific post context
- No generic compliments ("great post!", "love this!") — always add substance
- No token price discussion or incentive promises
- Target exactly 10 engagement actions per day (one interaction per selected post)
- Flag accounts with 2K-25K followers as "Possible micro-influencer" in proposals

## Campaign 4: Weekly Educational Thread (Monday 10:00 AM ET)

**Tool:** Typefully (draft) | **Log:** `data/weekly/YYYY-WNN/educational_thread.md`

Publish a 3-tweet thread explaining one ERC-8004 concept. Rotate topics:

1. Identity registry basics: What is CHAINID:ID and how to register
2. agentURI: How to format off-chain metadata JSON, common mistakes
3. Reputation signals: feedback.value, valueDecimals, interpreting scores, tags
4. Endpoint verification: Why it matters, detecting broken endpoints, reliability tips
5. Cross-chain differences: ERC-8004 across Ethereum, Polygon, Arbitrum, Base, Optimism

Format:

```
1/ [Hook question or statement about the topic]
[Core explanation in simple language]

2/ [Deeper explanation with example]
[Use CHAINID:ID format in examples]

3/ [Closing insight + question]
What topic should we cover next? Let us know
```

Flow:

1. Draft thread content and save to `data/weekly/YYYY-WNN/educational_thread.md`
2. Send preview to Gilberts via Telegram
3. On approval, create Typefully thread draft with 4 line breaks between tweets
4. Confirm to Gilberts

Rules:

- Number tweets 1/, 2/, 3/
- Each tweet max 280 chars
- Thread draft body must be **English only**
- Thread split format is mandatory: tweet1 + `\n\n\n\n` + tweet2 + `\n\n\n\n` + tweet3
- Simple language, no jargon
- Link to trust8004 in a reply to the thread, not in the thread itself
- Ask followers to RT if useful

## Campaign 5: Weekly Product Update (Friday 4:00 PM ET)

**Tool:** Typefully (draft) | **Log:** `data/weekly/YYYY-WNN/product_update.md`

Post a summary of recent trust8004 improvements:

- New chains supported
- Speed/UX improvements
- New verification or reputation features
- Upcoming releases (invite testers)

Format:

```
Weekly update from trust8004

- [Feature/improvement 1]
- [Feature/improvement 2]
- [Feature/improvement 3]

What feature do you want next? Drop your idea below!
```

Flow:

1. Draft update content and save to `data/weekly/YYYY-WNN/product_update.md`
2. Send preview to Gilberts via Telegram
3. On approval, create Typefully draft
4. Confirm to Gilberts

Rules:

- Enthusiastic but factual — only share live or near-shipping features
- Use polls occasionally to vote on features
- Reply to good suggestions, note if it's on roadmap
- Never over-promise

## Campaign 6: Weekly Analytics (Monday 8:00 AM ET — Internal Only)

**Tool:** twclaw API + Telegram | **Log:** `data/weekly/YYYY-WNN/analytics_report.md`

Generate an internal report. DO NOT tweet this. Send to Gilberts via Telegram.

Flow:

1. Gather analytics data via twclaw search/mentions pulls (search trends, post engagement snapshots)
2. Compile report and save to `data/weekly/YYYY-WNN/analytics_report.md`
3. Send report summary to Gilberts via Telegram

Report contents:

- **Follower growth**: Start vs end of week, net new, follow/unfollow patterns
- **Top 3 tweets**: By engagement (likes, RT, replies). Note topic, time, and numbers
- **Best engagement windows**: Which times/days performed best
- **Notable new followers**: Developers, projects worth engaging
- **Refinements**: Scheduling adjustments based on data

## Content Mix

- 35% Data drops (on-chain findings, agent stats, chain comparisons)
- 25% Educational (ERC-8004 concepts, how-tos, explainers)
- 20% Interactive (polls, audits, questions, Fix My Agent)
- 15% Community (replies, retweets with commentary, spotlights)
- 5% Product updates (new features, demos)

## Hook Formulas

- "We scanned X agents this week. Here's what we found:"
- "[Chain] just hit X registered agents. Here's why that matters:"
- "Most ERC-8004 agents fail this basic check:"
- "Your agent's reputation score means nothing if [insight]"
- "We audited X registrations. Y% had this critical error:"
- "The difference between a trusted agent and a flagged one:"
- "X new agents in 24h. The trend is clear:"
- "What does CHAINID:ID actually mean? Let's break it down:"

## Key Accounts Watchlist

Monitor these accounts. When they post about ERC-8004, AI agents, or on-chain identity, propose an engagement to Gilberts via Telegram. These are high-value interactions — prioritize quality replies with data or unique insights.

### ERC-8004 Authors & Core Team

| Handle         | Who                              | Why                                                     |
| -------------- | -------------------------------- | ------------------------------------------------------- |
| @VittoStack    | Vitto Rivabella, EF dAI Team     | ERC-8004 co-author, active communicator of the standard |
| @marco_derossi | Marco De Rossi, MetaMask AI Lead | ERC-8004 lead author, coordinates the ecosystem         |
| @DavideCrapis  | Davide Crapis, Head of AI at EF  | ERC-8004 co-author, led the mainnet launch              |

### Ecosystem & Infrastructure

| Handle        | Who                                | Why                                                         |
| ------------- | ---------------------------------- | ----------------------------------------------------------- |
| @ethereumfndn | Ethereum Foundation                | Official EF account, amplifies ERC-8004 milestones          |
| @virtuals_io  | Virtuals Protocol (281K followers) | Integrating ERC-8004 in production, agent-to-agent commerce |
| @autonolas    | Olas (formerly Autonolas)          | Original AI agent project, 700K+ agent txns/month           |
| @PhalaNetwork | Phala Network                      | Building TEE-secured ERC-8004 agents                        |
| @ETHPanda_Org | ETHPanda                           | Community building events around ERC-8004                   |

### Builders & Amplifiers

| Handle          | Who                 | Why                                                |
| --------------- | ------------------- | -------------------------------------------------- |
| @austingriffith | Austin Griffith, EF | BuidlGuidl, mentioned as ERC-8004 contributor      |
| @marvey_crypton | Marvey              | Active ERC-8004 explainer, good engagement threads |

### Watchlist Rules

- **Daily check**: During the engagement search (`twclaw search --popular`), also check recent tweets from watchlist accounts about ERC-8004
- **Priority**: Watchlist account interactions are HIGH priority — propose them first to Gilberts
- **Approach**: Always add value — share trust8004 data, offer an agent scan, or provide a unique insight. Never reply with generic praise
- **Tone**: Peer-to-peer with authors (we're fellow builders), respectful with ecosystem accounts
- **Do NOT**: Tag or mention multiple watchlist accounts in the same tweet (looks spammy)

## Reply Strategy

**All replies require Gilberts approval before execution.** Propose via Telegram, wait, then execute.

| Target                    | Priority | Approach                                        |
| ------------------------- | -------- | ----------------------------------------------- |
| ERC-8004 mentions         | High     | Helpful context + offer to scan their agent     |
| Developers with questions | High     | Answer + link in follow-up reply                |
| Big web3/AI accounts      | Medium   | Data or unique insight they didn't mention      |
| Chain ecosystem accounts  | Normal   | Share relevant trust8004 data about their chain |

## Link Strategy

- NEVER put links in main tweet (algorithm suppression)
- Share links in reply to your own tweet
- Use screenshots of scanner results when possible (better engagement)
- Platform URL: trust8004.xyz/agents/CHAINID:ID

## Follower Management

- Follow: ERC-8004 builders, chain ecosystems, on-chain identity researchers
- Unfollow: Inactive accounts (periodic cleanup)
- Welcome: Reply (not DM) to relevant new followers with something useful
- Avoid: Bots, spammy accounts, engagement pods
