import os
import sys
import asyncio
import threading
from flask import Flask

# ১. সবার আগে ইভেন্ট লুপ নিশ্চিত করা যাতে Pyrogram কোনো এরর না দেয়
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# ২. ফ্লাস্ক ওয়েব সার্ভার (Render পোর্ট বাইন্ডিংয়ের জন্য)
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot and Audio Streamer are running successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port, use_reloader=False)

# ৩. Pyrogram ও অন্যান্য মডিউল ইভেন্ট লুপ সেটআপ হওয়ার পর সেফলি ইমপোর্ট করা
from pyrogram import Client, idle

async def main():
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    print("Telegram client / Py-tgcalls loop started successfully...")
    await idle()

if __name__ == "__main__":
    # ফ্লাস্ক সার্ভার ব্যাকগ্রাউন্ড থ্রেডে রান করানো
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # মেইন থ্রেডে অ্যাসিনক্রোনাস মেইন ফাংশন রান করা
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process stopped.")
