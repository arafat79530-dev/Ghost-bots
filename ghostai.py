import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN_1")

QUOTEX_LINK_1 = "https://broker-qx.pro/sign-up/?lid=2384783"
QUOTEX_LINK_2 = "https://broker-qx.pro/sign-up/?lid=2384784"
SUPPORT_BOT = "https://t.me/ghostfuturebot"
SUPPORT_LINK = "https://t.me/ghostsupportbd"
CHANNEL_LINK = "https://t.me/premierghos"
YOUTUBE_LINK = "https://www.youtube.com/@PREMIERGHOST"
TIKTOK_LINK = "https://www.tiktok.com/@premier.ghost"
FACEBOOK_LINK = "https://www.facebook.com/PREMIERGHOST"

logging.basicConfig(level=logging.INFO)

def make_keyboard():
    buttons = [
        [InlineKeyboardButton("Quotex Registration — Link 1", url=QUOTEX_LINK_1)],
        [InlineKeyboardButton("Quotex Registration — Link 2", url=QUOTEX_LINK_2)],
        [InlineKeyboardButton("সাপোর্ট", url=SUPPORT_LINK), InlineKeyboardButton("সাপোর্ট বট", url=SUPPORT_BOT)],
        [InlineKeyboardButton("টেলিগ্রাম চ্যানেল", url=CHANNEL_LINK), InlineKeyboardButton("ইউটিউব", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("টিকটক", url=TIKTOK_LINK), InlineKeyboardButton("ফেসবুক", url=FACEBOOK_LINK)],
    ]
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "👋 প্রিমিয়ার ঘোস্ট (PREMIER GHOST)-এ স্বাগতম!\n\n🎯 প্রফেশনাল ডিজিটাল লিংক সেন্টার\n\n👇 নিচের বাটন থেকে লিংক খুলুন:\n\n⚠️ ট্রেডিংয়ে আর্থিক ঝুঁকি রয়েছে।"
    await update.effective_message.reply_text(msg, reply_markup=make_keyboard())

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("🔗 প্রয়োজনীয় লিংকগুলো:", reply_markup=make_keyboard())

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("👻 PREMIER GHOST - প্রফেশনাল ডিজিটাল লিংক সেন্টার।")

async def disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("⚠️ ট্রেডিংয়ে ঝুঁকি রয়েছে, লাভ নিশ্চিত নয়।")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("/start - শুরু\n/links - সব লিংক")

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN_1 missing!")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("disclaimer", disclaimer))
    app.add_handler(CommandHandler("help", help_command))
    print("Bot1 Live...")
    app.run_polling()
