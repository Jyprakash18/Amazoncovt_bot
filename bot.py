import re
import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running ✅"


# Convert link
def convert_link(text):
    match = re.search(r"(https?://(?:www\.)?amazon\.[^\s]+)", text)
    if not match:
        return None
    url = match.group(1).split("?")[0]
    return f"{url}?tag={AFFILIATE_TAG}"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send Amazon link")


# Handle message
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    link = convert_link(text)

    if link:
        await update.message.reply_text(f"✅ {link}")
    else:
        await update.message.reply_text("❌ Invalid link")


# Run bot (NO asyncio.run)
def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot started...")
    app_bot.run_polling()


# MAIN
if __name__ == "__main__":
    # Run bot in thread
    threading.Thread(target=run_bot).start()

    # Run Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
