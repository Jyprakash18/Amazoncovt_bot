import re
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from config import BOT_TOKEN, AFFILIATE_TAG


# 🔗 Convert Amazon link
def convert_amazon_link(text):
    pattern = r"(https?://(?:www\.)?amazon\.[^\s]+)"
    match = re.search(pattern, text)

    if not match:
        return None

    url = match.group(1).split("?")[0]
    return f"{url}?tag={AFFILIATE_TAG}"


# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send Amazon product link\nI will convert it to your affiliate link 💰"
    )


# 📩 Handle message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    link = convert_amazon_link(text)

    if link:
        await update.message.reply_text(f"✅ Affiliate Link:\n\n{link}")
    else:
        await update.message.reply_text("❌ Send valid Amazon link")


# 🚀 Main
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
