import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Ekhane "PASTE_YOUR_BOT_TOKEN_HERE"-er bodole apnar ashol bot token ti boshaben
BOT_TOKEN = "8734584455:AAFHqfjtXbetrdBgC4zMNwGVBdua33VBIFM"

# Apnar shothik link-gulo ebong info
QUOTEX_LINK_1 = "https://broker-qx.pro/sign-up/?lid=2384783"
QUOTEX_LINK_2 = "https://broker-qx.pro/sign-up/?lid=2384784"
SUPPORT_BOT = "https://t.me/ghostfuturebot"
SUPPORT_LINK = "https://t.me/ghostsupportbd"
CHANNEL_LINK = "https://t.me/premierghos"
YOUTUBE_LINK = "https://www.youtube.com/@PREMIERGHOST"
TIKTOK_LINK = "https://www.tiktok.com/@premier.ghost"
FACEBOOK_LINK = "https://www.facebook.com/PREMIERGHOST"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def make_keyboard():
    buttons = [
        [InlineKeyboardButton("Quotex Registration — Link 1", url=QUOTEX_LINK_1)],
        [InlineKeyboardButton("Quotex Registration — Link 2", url=QUOTEX_LINK_2)],
        [
            InlineKeyboardButton("সাপোর্ট", url=SUPPORT_LINK),
            InlineKeyboardButton("সাপোর্ট বট", url=SUPPORT_BOT),
        ],
        [
            InlineKeyboardButton("টেলিগ্রাম চ্যানেল", url=CHANNEL_LINK),
            InlineKeyboardButton("ইউটিউব", url=YOUTUBE_LINK),
        ],
        [
            InlineKeyboardButton("টিকটক", url=TIKTOK_LINK),
            InlineKeyboardButton("ফেসবুক", url=FACEBOOK_LINK),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 প্রিমিয়ার ঘোস্ট (PREMIER GHOST)-এ আপনাকে স্বাগতম!\n\n"
        "🎯 আমি একটি প্রফেশনাল ডিজিটাল লিংক সেন্টার এবং ট্রেডিং সাপোর্ট হাব।\n\n"
        "👇 নিচের বাটন থেকে প্রয়োজনীয় লিংক খুলুন:\n\n"
        "⚠️ ট্রেডিংয়ে আর্থিক ঝুঁকি রয়েছে। লাভের কোনো নিশ্চয়তা নেই। "
        "নিজের যাচাই ছাড়া কোনো সিদ্ধান্ত নেবেন না।"
    )
    await update.effective_message.reply_text(
        message,
        reply_markup=make_keyboard(),
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🔗 প্রয়োজনীয় লিংকগুলো:",
        reply_markup=make_keyboard(),
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👻 𝗡𝗮𝗺𝗲: PREMIER GHOST\n\n"
        "🎯 আমি কে/কী করি:\n"
        "আমি একটি প্রফেশনাল ডিজিটাল লিংক সেন্টার এবং ট্রেডিং সাপোর্ট হাব। "
        "আমার কাজ হলো আপনার প্রয়োজনীয় সমস্ত অফিসিয়াল লিংক, এফিলিয়েট প্ল্যাটফর্ম "
        "এবং সোশ্যাল মিডিয়া পেজগুলোকে এক ক্লিকে এক জায়গায় সাজিয়ে দেওয়া।\n\n"
        "💡 আমার সম্পর্কে গুরুত্বপূর্ণ তথ্য:\n"
        "• এই প্ল্যাটফর্মটি ট্রেডিং সম্পর্কিত সঠিক তথ্য ও অফিসিয়াল লিংকের জন্য তৈরি।\n"
        "• ট্রেডিংয়ে আর্থিক ঝুঁকি রয়েছে এবং এখানে কোনো লাভের শতভাগ নিশ্চয়তা দেওয়া হয় না।\n"
        "• যেকোনো লিংকে যুক্ত হওয়ার বা অ্যাকাউন্ট খোলার আগে নিজের ঝুঁকি নিজে যাচাই করুন।"
    )
    await update.effective_message.reply_text(message)


async def disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "⚠️ ঝুঁকি-সংক্রান্ত ঘোষণা\n\n"
        "ট্রেডিংয়ে আপনার কিছু বা সমস্ত অর্থ হারানোর ঝুঁকি থাকতে পারে। "
        "কোনো লাভ বা নির্দিষ্ট ফলাফলের নিশ্চয়তা দেওয়া হচ্ছে না।\n\n"
        "কোনো প্ল্যাটফর্মে অ্যাকাউন্ট খোলা বা অর্থ জমা দেওয়ার আগে "
        "তার শর্তাবলি ও ঝুঁকি নিজে যাচাই করুন। এই বট কোনো আর্থিক পরামর্শ দেয় না।"
    )
    await update.effective_message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "বটের কমান্ডসমূহ:\n\n"
        "/start — বট শুরু করুন ও লিংক দেখুন\n"
        "/links — সব লিংক দেখুন\n"
        "/about — আমাদের সম্পর্কে জানতে\n"
        "/disclaimer — ঝুঁকি-সংক্রান্ত ঘোষণা\n"
        "/help — সাহায্য"
    )
    await update.effective_message.reply_text(message)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Bot error: %s", context.error)


def main():
    if BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise ValueError("কোডে BOT_TOKEN-এর জায়গায় BotFather token বসান।")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("disclaimer", disclaimer))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)

    print("বট চালু হয়েছে। বন্ধ করতে Ctrl+C চাপুন।")
    app.run_polling()


if __name__ == "__main__":
    main()
