import os

BOT_TOKEN = os.getenv("8655630907:AAF34iEzf3h8PO6RhgtHuDBmrFXZhtRARVk")
AFFILIATE_TAG = os.getenv("sumandealsx-21")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

if not AFFILIATE_TAG:
    raise ValueError("AFFILIATE_TAG not set")
