import re
import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

# Flask app (for Render)
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running ✅"


# Convert Amazon link
def convert_link(text):
    match = re.search(r"(https?://(?:www\.)?amazon\.[^\s]+)", text)
    if not match:
        return None
    url = match.group(1).split("?")[0]
    return f"{url}?tag={AFFILIATE_TAG}"


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send Amazon product link")


# Handle message
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    link = convert_link(text)

    if link:
        await update.message.reply_text(f"✅ {link}")
    else:
        await update.message.reply_text("❌ Invalid Amazon link")


# Telegram bot run (MAIN THREAD)
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot running...")
    app.run_polling()


# Flask run (separate thread)
def run_web():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)


# MAIN
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()
