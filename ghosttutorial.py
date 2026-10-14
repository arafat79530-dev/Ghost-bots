
import os
import html
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# BOT SETTINGS
# =========================
BOT_TOKEN = "8854135653:AAEd7HnsYve5zM4Ri5Cd5Ln0n199Xubj_a4"

# নিজের বটের username @ ছাড়া লিখবে
BOT_USERNAME = "ghostfuturebot"

# তোমার Gemini API Key
GEMINI_API_KEY = "AQ.Ab8RN6LNTKOU155-SH-u0ouQyFO0lbpsaUJJgO_hBF2Hrxhrq"

bot = telebot.TeleBot(BOT_TOKEN)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# নোটগুলো আপাতত মেমোরিতে থাকবে
notes = {}


# =========================
# INLINE KEYBOARD BUTTONS
# =========================
def main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(
            "📝 Save a Note",
            callback_data="save_note"
        ),
        InlineKeyboardButton(
            "📚 My Notes",
            callback_data="notes"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "👻 VIP Benefits",
            callback_data="vipbenefits"
        ),
        InlineKeyboardButton(
            "🎁 Free VIP",
            callback_data="freevip"
        )
    )

    return keyboard


# =========================
# WELCOME MESSAGE + BLUE LINKS
# =========================


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 হ্যালো ট্রেডার! স্বাগতম 🖤📈\n\n"
        "🎁 /freevip — Free VIP-এর বিস্তারিত ও Tutorial Video দেখতে ক্লিক করুন।\n\n"
        "👑 /vipbenefits — VIP-এর সুবিধাগুলো জানতে ক্লিক করুন।\n\n"
        "📝 /save — আপনার নোট সেভ করতে।\n"
        "📚 /notes — সেভ করা নোট দেখতে।\n\n"
        "💬 Support: @ghostsupportbd\n\n"
        "⚠️ Trading involves risk. লাভ নিশ্চিত নয়।"
    )

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🎁 Free VIP", callback_data="freevip"),
        InlineKeyboardButton("👑 VIP Benefits", callback_data="vipbenefits")
    )
    keyboard.add(
        InlineKeyboardButton("📝 Save Note", callback_data="save_note"),
        InlineKeyboardButton("📚 My Notes", callback_data="notes")
    )
    keyboard.add(
        InlineKeyboardButton(
            "💬 Contact Support",
            url="https://t.me/ghostsupportbd"
        )
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


# =========================
# START / HELP
# =========================
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    parts = message.text.split(maxsplit=1)
    payload = parts[1].strip().lower() if len(parts) > 1 else ""

    # Blue link থেকে আসা নির্দেশনা
    if payload == "save":
        send_save_instruction(message.chat.id)
    elif payload == "notes":
        show_notes(message.chat.id, message.from_user.id)
    elif payload == "vipbenefits":
        send_vipbenefits(message.chat.id)
    elif payload == "freevip":
        send_freevip(message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            welcome_text(),
            parse_mode="HTML",
            reply_markup=main_keyboard(),
            disable_web_page_preview=True
        )


# =========================
# SAVE NOTE
# =========================
def send_save_instruction(chat_id):
    bot.send_message(
        chat_id,
        "📝 <b>বস, আপনার নোটটি এভাবে পাঠান:</b>\n\n"
        "<code>/save আগামীকাল ভিডিও আপলোড করব</code>\n\n"
        "আপনার নিজের নোটের লেখা উদাহরণের জায়গায় বসিয়ে দিন।",
        parse_mode="HTML"
    )


@bot.message_handler(commands=["save"])
def save_note(message):
    parts = message.text.split(maxsplit=1)
    note_text = parts[1].strip() if len(parts) > 1 else ""

    if note_text:
        user_id = message.from_user.id
        notes.setdefault(user_id, [])
        notes[user_id].append(note_text)

        bot.reply_to(
            message,
            "✅ বস, আপনার নোটটি ডায়েরিতে সেভ করে রেখেছি!"
        )
    else:
        send_save_instruction(message.chat.id)


# =========================
# SHOW NOTES
# =========================
def show_notes(chat_id, user_id):
    user_notes = notes.get(user_id, [])

    if user_notes:
        reply = "📚 <b>বস, আপনার সেভ করা নোটগুলো:</b>\n\n"

        for i, note in enumerate(user_notes, 1):
            reply += f"{i}. {html.escape(note)}\n"

        bot.send_message(
            chat_id,
            reply,
            parse_mode="HTML"
        )
    else:
        bot.send_message(
            chat_id,
            "📭 বস, আপনার কোনো নোট সেভ করা নেই।\n\n"
            "📝 নোট সেভ করতে লিখুন:\n"
            "<code>/save আপনার নোট</code>",
            parse_mode="HTML"
        )


@bot.message_handler(commands=["notes"])
def notes_command(message):
    show_notes(message.chat.id, message.from_user.id)


# =========================
# VIP BENEFITS
# =========================
VIP_TEXT = """<b>👻 𝙂𝙃𝙊𝙎𝙏 𝙑𝙄𝙋 👻</b>

<b>Benefits of Our VIP You'll Get:-</b>
<blockquote>🤔 <i>Daily Sureshot Live Signal</i> ☠️
🤔 <i>HIGH Accurcay Future Signal</i> 😓
🤔 <i>Daily Bot Signal (Quotex)</i> 😊
🤔 <i>Event Impact 99% Signal</i> 📈
🤔 <i>Lifetime Live Support</i> 🔖</blockquote>

➡️ <b>CREATE ACCOUNT OUR LINK</b> 🔽

📌 <b>DEPOSIT MINIMUM 20$</b> 💵

🔗 <b>LINK</b> ☠️
➡️ https://broker-qx.pro/sign-up/?lid=2384783 ( BD )🇧🇩🌐

💬 <b>SEND TRADER ID/ANY INQUIRES</b> 👉😎
<a href="https://t.me/ghostsupportbd">@ghostsupportbd</a> ✅"""


def send_vipbenefits(chat_id):
    bot.send_message(
        chat_id,
        VIP_TEXT,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@bot.message_handler(commands=["vipbenefits"])
def vipbenefits_command(message):
    send_vipbenefits(message.chat.id)


# =========================
# FREE VIP VIDEO + MESSAGE
# =========================
FREEVIP_TEXT = """😏 আপনি কি ট্রেডিং এ নতুন? আপনি কি ঘরে বসে ট্রেডিং করে টাকা ইনকাম করতে চান? 💰✔️

📌 কিভাবে আমাদের VIP গ্রুপে ফ্রী জয়েন হবেন Step-by-Step নির্দেশনা:

🥇 প্রথমেই আপনাকে <a href="https://broker-qx.pro/sign-up/?lid=2384783">এই লিংক দিয়ে একাউন্ট খুলতে হবে</a> 🇧🇩

✅ তথ্য প্রদান:
👉 আপনার QUOTEX একাউন্টের UID নিচের আইডিতে SEND করবেন ⬇️
✉️ <a href="https://t.me/ghostsupportbd">@ghostsupportbd</a> ✅

💱 কনফার্মেশন পাওয়ার পর আপনার একাউন্টে মিনিমাম 20$ ডিপোজিট করার শর্ত ও অন্যান্য নিয়ম সাপোর্ট থেকে নিশ্চিত করে নিন।

📱 OWNER: <a href="https://t.me/ghostsupportbd">@ghostsupportbd</a> ✅

📱 <a href="https://www.tiktok.com/@premier.ghost">TikTok Channel</a>

আমরা আপনার জন্য একটি আনন্দদায়ক ট্রেডিং যাত্রা কামনা করি 🥰"""


def send_freevip(chat_id):
    video_path = "premieraccountcreate.mp4"

    try:
        bot.send_chat_action(chat_id, "upload_video")

        with open(video_path, "rb") as video:
            bot.send_video(
                chat_id,
                video,
                caption=FREEVIP_TEXT,
                parse_mode="HTML",
                timeout=120
            )

    except FileNotFoundError:
        bot.send_message(
            chat_id,
            "⚠️ বস, 'premieraccountcreate.mp4' ফাইলটি পাওয়া যায়নি।\n\n"
            + FREEVIP_TEXT,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as error:
        print("Video error:", error)

        bot.send_message(
            chat_id,
            "⚠️ ভিডিও পাঠাতে সমস্যা হয়েছে। নিচে নির্দেশনাটি দেওয়া হলো:\n\n"
            + FREEVIP_TEXT,
            parse_mode="HTML",
            disable_web_page_preview=True
        )


@bot.message_handler(commands=["freevip"])
def freevip_command(message):
    send_freevip(message.chat.id)


# =========================
# INLINE BUTTON ACTIONS
# =========================
@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    bot.answer_callback_query(call.id)

    chat_id = call.message.chat.id
    user_id = call.from_user.id
    action = call.data

    if action == "save_note":
        send_save_instruction(chat_id)

    elif action == "notes":
        show_notes(chat_id, user_id)

    elif action == "vipbenefits":
        send_vipbenefits(chat_id)

    elif action == "freevip":
        send_freevip(chat_id)


# =========================
# GEMINI AI REPLY
# =========================
@bot.message_handler(
    func=lambda message: bool(message.text)
    and not message.text.startswith("/")
)
def ai_reply(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")

        prompt = (
            "তুমি একজন প্রফেশনাল, বিনয়ী এবং স্মার্ট সেক্রেটারি। "
            f"তোমার বসের মেসেজ: '{message.text}'। "
            "একজন দক্ষ সেক্রেটারির মতো বাংলায় উত্তর দাও।"
        )

        response = model.generate_content(prompt)

        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(
                message,
                "বস, আমি ঠিক বুঝতে পারিনি। আবার বলবেন?"
            )

    except Exception as error:
        print("Gemini error:", error)
        bot.reply_to(
            message,
            "দুঃখিত বস, AI উত্তর দিতে সমস্যা হয়েছে। একটু পরে চেষ্টা করুন।"
        )


# =========================
# RUN BOT
# =========================
print("✅ Personal Secretary Bot চালু হচ্ছে...")
bot.infinity_polling(skip_pending=True)
