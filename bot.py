from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")


def convert_to_affiliate(url):
    match = re.search(r"(https?://(?:www\.)?amazon\.[^ ]+)", url)
    if match:
        clean_url = match.group(1).split("?")[0]
        return f"{clean_url}?tag={AFFILIATE_TAG}"
    return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    link = convert_to_affiliate(text)

    if link:
        await update.message.reply_text(f"✅ Affiliate Link:\n{link}")
    else:
        await update.message.reply_text("❌ Send valid Amazon link")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
