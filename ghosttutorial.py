import os, html, threading
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# Token ekhon code e na, Render e thakbe!
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    print("ERROR: BOT_TOKEN / GEMINI_API_KEY Environment e den!")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
notes = {}

# Flask - Render Live rakhar jonno
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "GHOST FUTURE BOT LIVE"

def main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📝 Save a Note", callback_data="save_note"),
        InlineKeyboardButton("📚 My Notes", callback_data="notes")
    )
    keyboard.add(
        InlineKeyboardButton("👻 VIP Benefits", callback_data="vipbenefits"),
        InlineKeyboardButton("🎁 Free VIP", callback_data="freevip")
    )
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 হ্যালো ট্রেডার! স্বাগতম 🖤📈\n\n"
        "🎁 /freevip — Free VIP Tutorial Video\n\n"
        "👑 /vipbenefits — VIP Benefits\n\n"
        "📝 /save — Note save\n"
        "📚 /notes — My Notes\n\n"
        "💬 Support: @ghostsupportbd"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_keyboard())

#... (apnar baki save, notes, vip, freevip er code same thakbe, change lagbe na)

@bot.message_handler(commands=["save"])
def save_note(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        user_id = message.from_user.id
        notes.setdefault(user_id, [])
        notes[user_id].append(parts[1].strip())
        bot.reply_to(message, "✅ বস, নোট সেভ করেছি!")
    else:
        bot.send_message(message.chat.id, "📝 /save লিখে নোট দিন।")

@bot.message_handler(commands=["notes"])
def notes_command(message):
    user_notes = notes.get(message.from_user.id, [])
    if user_notes:
        reply = "📚 আপনার নোট:\n\n" + "\n".join([f"{i}. {html.escape(n)}" for i,n in enumerate(user_notes,1)])
        bot.send_message(message.chat.id, reply, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "📭 কোনো নোট নেই।")

VIP_TEXT = """<b>👻 GHOST VIP Benefits</b>\nDaily Live Signal, Future Signal, Bot Signal"""

def send_vipbenefits(chat_id):
    bot.send_message(chat_id, VIP_TEXT, parse_mode="HTML")

@bot.message_handler(commands=["vipbenefits"])
def vipbenefits_command(message): send_vipbenefits(message.chat.id)

FREEVIP_TEXT = """Free VIP - Link diye account khulun: https://broker-qx.pro/sign-up/?lid=2384783"""

def send_freevip(chat_id):
    bot.send_message(chat_id, FREEVIP_TEXT, parse_mode="HTML")

@bot.message_handler(commands=["freevip"])
def freevip_command(message): send_freevip(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    bot.answer_callback_query(call.id)
    if call.data == "save_note": bot.send_message(call.message.chat.id, "📝 /save লিখে নোট দিন।")
    elif call.data == "notes": notes_command(call)
    elif call.data == "vipbenefits": send_vipbenefits(call.message.chat.id)
    elif call.data == "freevip": send_freevip(call.message.chat.id)

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    if message.text.startswith("/"): return
    try:
        bot.send_chat_action(message.chat.id, "typing")
        response = model.generate_content(message.text)
        if response and response.text:
            bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Gemini error: {e}")

# Flask ke alada thread e
threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000))), daemon=True).start()

print("✅ Bot চালু হচ্ছে...")
bot.infinity_polling(skip_pending=True)
