import re
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN missing")
if not AFFILIATE_TAG:
    raise Exception("AFFILIATE_TAG missing")


def convert_link(text):
    pattern = r"(https?://(?:www\.)?amazon\.[^\s]+)"
    match = re.search(pattern, text)

    if not match:
        return None

    url = match.group(1).split("?")[0]
    return f"{url}?tag={AFFILIATE_TAG}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Amazon link 🔗")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    link = convert_link(text)

    if link:
        await update.message.reply_text(f"✅ {link}")
    else:
        await update.message.reply_text("❌ Invalid link")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
