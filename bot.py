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
import requests
import urllib.parse

def convert_link(text):
    try:
        urls = re.findall(r"(https?://[^\s]+)", text)

        for original_url in urls:
            url = original_url

            # ✅ STEP 1: Handle redirect links (dealscrown etc.)
            if "url=" in url:
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                if "url" in parsed:
                    url = parsed["url"][0]

            # ✅ STEP 2: Handle ALL short links (amzn.to, amznn.in etc.)
            if any(x in url for x in ["amzn.to", "amznn.in"]):
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        url = response.url
    except:
        return None, None   # ✅ FIX

            # ✅ STEP 3: Check Amazon
            if "amazon." in url:
                clean = url.split("?")[0]
                return original_url, f"{clean}?tag={AFFILIATE_TAG}"

        return None, None

    except Exception as e:
        print("Error:", e)
        return None, None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send Amazon product link")


# Handle message
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    new_text = text
    urls = re.findall(r"(https?://[^\s]+)", text)

    found = False

    for url in urls:
        original_url = url

        # Handle short link
        if "amzn.to" in url:
            try:
                import requests
                response = requests.get(url, allow_redirects=True, timeout=5)
                url = response.url
            except:
                continue

        # Check Amazon link
        if "amazon." in url:
            clean_url = url.split("?")[0]
            affiliate_url = f"{clean_url}?tag={AFFILIATE_TAG}"

            # Replace in text
            new_text = new_text.replace(original_url, affiliate_url)
            found = True

    if found:
        await update.message.reply_text(new_text)
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
