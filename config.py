import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

if not AFFILIATE_TAG:
    raise ValueError("AFFILIATE_TAG not set")
