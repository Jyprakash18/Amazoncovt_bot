import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# 🔐 Get env variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")


# ❌ Safety check
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")
if not AFFILIATE_TAG:
    raise ValueError("AFFILIATE_TAG missing")


# 🔗 Convert Amazon link → Affiliate
def convert_to_affiliate(text):
    try:
        pattern = r"(https?://(?:www\.)?amazon\.[a-z\.]+/[^\s]+)"
        match = re.search(pattern, text)

        if not match:
            return None

        clean_url = match.group(1).split("?")[0]

        # Remove existing tag if present
        if "tag=" in clean_url:
            clean_url = clean_url.split("?")[0]

        return f"{clean_url}?tag={AFFILIATE_TAG}"

    except Exception as e:
        print("Error:", e)
        return None


# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send any Amazon product link\nI will convert it into your affiliate link 💰"
    )


# 📩 Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    link = convert_to_affiliate(text)

    if link:
        await update.message.reply_text(f"✅ Affiliate Link:\n\n{link}")
    else:
        await update.message.reply_text("❌ Please send a valid Amazon link")


# 🚀 Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
