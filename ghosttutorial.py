import os, html
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN_2")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
notes = {}

def main_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("📝 Save a Note", callback_data="save_note"), InlineKeyboardButton("📚 My Notes", callback_data="notes"))
    kb.add(InlineKeyboardButton("👻 VIP Benefits", callback_data="vipbenefits"), InlineKeyboardButton("🎁 Free VIP", callback_data="freevip"))
    return kb

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    txt = "👋 হ্যালো ট্রেডার! স্বাগতম 🖤📈\n\n🎁 /freevip - Free VIP Tutorial\n👑 /vipbenefits - VIP Benefits\n📝 /save - Note Save\n📚 /notes - My Notes\n\n💬 Support: @ghostsupportbd"
    bot.send_message(message.chat.id, txt, reply_markup=main_keyboard())

@bot.message_handler(commands=["save"])
def save_note(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        notes.setdefault(message.from_user.id, []).append(parts[1].strip())
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

@bot.message_handler(commands=["vipbenefits"])
def vipbenefits_command(message):
    bot.send_message(message.chat.id, "👻 GHOST VIP\nDaily Sureshot Live Signal\nHigh Accuracy Future Signal\nLink: https://broker-qx.pro/sign-up/?lid=2384783", parse_mode="HTML")

@bot.message_handler(commands=["freevip"])
def freevip_command(message):
    bot.send_message(message.chat.id, "Free VIP - Link diye account khulun: https://broker-qx.pro/sign-up/?lid=2384783\nSupport: @ghostsupportbd")

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    bot.answer_callback_query(call.id)
    if call.data == "save_note": bot.send_message(call.message.chat.id, "📝 /save লিখে নোট দিন।")
    elif call.data == "notes": notes_command(call)
    elif call.data == "vipbenefits": vipbenefits_command(call)
    elif call.data == "freevip": freevip_command(call)

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    if message.text.startswith("/"): return
    try:
        bot.send_chat_action(message.chat.id, "typing")
        res = model.generate_content(message.text)
        if res and res.text: bot.reply_to(message, res.text)
    except Exception as e: print(e)

def run():
    print("Bot2 Live...")
    bot.infinity_polling(skip_pending=True)
