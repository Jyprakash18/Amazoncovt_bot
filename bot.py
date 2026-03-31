import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, AFFILIATE_TAG


# 🔗 Function to convert Amazon link → affiliate link
def convert_to_affiliate(url):
    try:
        # Extract Amazon product URL
        match = re.search(r"(https?://(?:www\.)?amazon\.[a-z\.]+/[^ ]+)", url)
        if match:
            clean_url = match.group(1).split("?")[0]
            return f"{clean_url}?tag={AFFILIATE_TAG}"
        return None
    except:
        return None


# 📩 Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    affiliate_link = convert_to_affiliate(text)

    if affiliate_link:
        await update.message.reply_text(
            f"✅ Affiliate Link Generated:\n\n{affiliate_link}"
        )
    else:
        await update.message.reply_text(
            "❌ Send a valid Amazon product link"
        )


# 🚀 Start bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
