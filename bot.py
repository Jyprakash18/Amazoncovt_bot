import re
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

# Flask app (for Render port)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

# 🔗 Convert link
def convert_link(text):
    pattern = r"(https?://(?:www\.)?amazon\.[^\s]+)"
    match = re.search(pattern, text)

    if not match:
        return None

    url = match.group(1).split("?")[0]
    return f"{url}?tag={AFFILIATE_TAG}"

# Telegram start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Amazon link 🔗")

# Handle msg
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    link = convert_link(text)

    if link:
        await update.message.reply_text(f"✅ {link}")
    else:
        await update.message.reply_text("❌ Invalid link")

# Run bot
def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot running...")
    app.run_polling()

# MAIN
if __name__ == "__main__":
    # Run bot in thread
    t = threading.Thread(target=run_bot)
    t.start()

    # Run flask (IMPORTANT for Render)
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
