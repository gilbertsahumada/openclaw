# TOOLS.md - Technical Reference

## Environment

- Running on Dokploy (Docker container)
- Connected via Telegram for communication with Gilberts
- Twitter skill available for all Twitter operations
- Built-in browser automation (see skills/browser/SKILL.md)

## Browser Automation (Built-in)

OpenClaw's native browser tool for web scraping, screenshots, and interaction.

**Key use cases for trust8004:**
- Take screenshots of agent pages for tweets (better engagement than links)
- Scrape agent data from trust8004.xyz/agents/CHAINID:ID for data drops
- Verify agent endpoints by visiting agentURI URLs
- Record demos of scanner features for product update tweets

See `skills/browser/SKILL.md` for full command reference.

## Twitter Skill Capabilities

- Post and schedule tweets
- Read timelines and search tweets/conversations
- Search by keywords and hashtags
- Follow/unfollow accounts
- Fetch engagement metrics and analytics
- Monitor mentions and brand keywords
- Schedule posts (queue at least 12h ahead, adjust based on analytics)

## Agent Identifier Format

**Format: `CHAINID:ID`**

- `CHAINID` = numeric chain ID (e.g., 1 for Ethereum, 137 for Polygon, 42161 for Arbitrum)
- `ID` = numeric agent identifier within that chain's registry
- Example: `2741:615`

**Platform URL: `https://www.trust8004.xyz/agents/CHAINID:ID`**
- Example: `https://www.trust8004.xyz/agents/2741:615`

When users share agent IDs, always verify the CHAINID:ID format. If they use the old `agentRegistry:agentId` format, guide them to use CHAINID:ID instead.

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
