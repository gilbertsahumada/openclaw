#!/usr/bin/env node
/**
 * telegram-channel-post.mjs
 * Posts a message to a Telegram channel/group.
 *
 * Usage:
 *   node scripts/telegram-channel-post.mjs "message text here"
 *
 * Env:
 *   TELEGRAM_BOT_TOKEN — the bot token (already configured for OpenClaw)
 *   TELEGRAM_CHANNEL_ID — the channel/group ID (e.g. @channel_name or -100123456789)
 */

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN?.trim();
const TELEGRAM_CHANNEL_ID = process.env.TELEGRAM_CHANNEL_ID?.trim();

if (!TELEGRAM_BOT_TOKEN) {
  console.error("TELEGRAM_BOT_TOKEN is required");
  process.exit(1);
}

if (!TELEGRAM_CHANNEL_ID) {
  console.error("TELEGRAM_CHANNEL_ID is required");
  process.exit(1);
}

const message = process.argv.slice(2).join(" ").trim().replace(/\\n/g, "\n");

if (!message) {
  console.error('Usage: node scripts/telegram-channel-post.mjs "message text"');
  process.exit(1);
}

async function sendMessage() {
  const res = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: TELEGRAM_CHANNEL_ID,
      text: message,
      parse_mode: "HTML",
      disable_web_page_preview: false,
    }),
  });

  const data = await res.json();

  if (!data.ok) {
    console.error(`Telegram API error: ${JSON.stringify(data)}`);
    process.exit(1);
  }

  console.log(JSON.stringify({ ok: true, message_id: data.result.message_id }));
}

sendMessage().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
