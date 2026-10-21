import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, idle

# ১. Render-এর পোর্ট সমস্যার সমাধানের জন্য ফ্লাস্ক ওয়েব সার্ভার
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot and Audio Streamer are running successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port, use_reloader=False)

# ২. আপনার টেলিগ্রাম ও স্ট্রিমিংয়ের মূল অ্যাসিনক্রোনাস লজিক
async def main():
    # Environment Variables থেকে কনফিগারেশন লোড করা
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    print("Telegram client / Py-tgcalls loop started...")
    # বট বা স্ট্রিম চালু রাখার জন্য idle ব্যবহার করা
    await idle()

if __name__ == "__main__":
    # ফ্লাস্ক সার্ভারটি ব্যাকগ্রাউন্ড থ্রেডে রান করানো হচ্ছে যাতে পোর্ট স্ক্যানিংয়ে কোনো টাইমআউট না আসে
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # পাইথনের মেইন থ্রেডে সঠিক ইভেন্ট লুপ বজায় রেখে মেইন ফাংশন রান করা
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process stopped by user.")
