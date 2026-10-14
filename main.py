import os, logging, html, threading
from flask import Flask

# ========= BOT 1 & 2 LIBRARY =========
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup as TeleMarkup, InlineKeyboardButton as TeleButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ========= TOKENS - RENDER E BOSABEN =========
BOT_TOKEN_1 = os.getenv("BOT_TOKEN_1") # Link Bot
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2") # Future Bot
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ========= FLASK =========
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "BOTH BOTS LIVE IN ONE FILE - GHOST"

# ================= BOT 1: LINK BOT CODE =================
QUOTEX_LINK_1 = "https://broker-qx.pro/sign-up/?lid=2384783"
QUOTEX_LINK_2 = "https://broker-qx.pro/sign-up/?lid=2384784"

def make_keyboard1():
    buttons = [
        [InlineKeyboardButton("Quotex Link 1", url=QUOTEX_LINK_1)],
        [InlineKeyboardButton("Quotex Link 2", url=QUOTEX_LINK_2)],
        [InlineKeyboardButton("Support", url="https://t.me/ghostsupportbd")],
        [InlineKeyboardButton("Channel", url="https://t.me/premierghos")],
    ]
    return InlineKeyboardMarkup(buttons)

async def start1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("👋 PREMIER GHOST LINK BOT - Welcome!", reply_markup=make_keyboard1())
async def links1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("🔗 Links:", reply_markup=make_keyboard1())

def run_bot1():
    if not BOT_TOKEN_1:
        print("BOT_TOKEN_1 Missing!")
        return
    print("Starting BOT 1...")
    app = Application.builder().token(BOT_TOKEN_1).build()
    app.add_handler(CommandHandler("start", start1))
    app.add_handler(CommandHandler("links", links1))
    app.run_polling()

# ================= BOT 2: FUTURE BOT CODE =================
notes = {}
bot2 = telebot.TeleBot(BOT_TOKEN_2) if BOT_TOKEN_2 else None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

def main_keyboard2():
    kb = TeleMarkup(row_width=2)
    kb.add(TeleButton("📝 Save Note", callback_data="save_note"), TeleButton("📚 My Notes", callback_data="notes"))
    return kb

@bot2.message_handler(commands=['start', 'help'])
def welcome2(message):
    bot2.send_message(message.chat.id, "👋 GHOST FUTURE BOT\n📝 /save - note\n📚 /notes - my notes\n💬 @ghostsupportbd", reply_markup=main_keyboard2())

@bot2.message_handler(commands=['save'])
def save2(message):
    parts = message.text.split(maxsplit=1)
    if len(parts)>1:
        notes.setdefault(message.from_user.id, []).append(parts[1].strip())
        bot2.reply_to(message, "✅ Note saved!")
    else: bot2.send_message(message.chat.id, "Use: /save your note")

@bot2.message_handler(commands=['notes'])
def notes2(message):
    user_notes = notes.get(message.from_user.id, [])
    if user_notes:
        txt = "\n".join([f"{i}. {html.escape(n)}" for i,n in enumerate(user_notes,1)])
        bot2.send_message(message.chat.id, f"📚 Notes:\n{txt}", parse_mode="HTML")
    else: bot2.send_message(message.chat.id, "No notes!")

@bot2.message_handler(func=lambda m: True)
def ai2(message):
    if message.text.startswith("/"): return
    try:
        bot2.send_chat_action(message.chat.id, "typing")
        res = model.generate_content(message.text)
        if res and res.text: bot2.reply_to(message, res.text)
    except Exception as e: print(f"Bot2 AI Error: {e}")

def run_bot2():
    if not BOT_TOKEN_2:
        print("BOT_TOKEN_2 Missing!")
        return
    print("Starting BOT 2...")
    bot2.infinity_polling(skip_pending=True)

# ================= RUN BOTH IN ONE FILE =================
threading.Thread(target=run_bot1, daemon=True).start()
threading.Thread(target=run_bot2, daemon=True).start()

# Flask main thread e
flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
