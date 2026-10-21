import os
import sys
import asyncio
import threading
from flask import Flask, render_template, request, jsonify

# ইভেন্ট লুপ পলিসি সেটআপ
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# ফ্লাস্ক অ্যাপ ইনিশিয়ালাইজেশন (templates ফোল্ডার ব্যবহারের জন্য)
app_web = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    # রেন্ডার সার্ভার বা ব্রাউজারে হোমপেজ দেখানোর জন্য
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    
    # এখানে আপনার py-tgcalls এর মিউট/আনমিউট লজিক হ্যান্ডেল হবে
    if command == 'mute':
        print("Action: Audio Muted via Mini App")
        # pytgcalls.mute_stream() কোড এখানে যুক্ত হবে
        return jsonify({"status": "success", "message": "Muted 🔇"})
    
    elif command == 'unmute':
        print("Action: Audio Unmuted via Mini App")
        # pytgcalls.unmute_stream() কোড এখানে যুক্ত হবে
        return jsonify({"status": "success", "message": "Unmuted 🔊"})
        
    elif command == 'stop':
        print("Action: Stream Stopped via Mini App")
        # pytgcalls.leave_group_call() কোড এখানে যুক্ত হবে
        return jsonify({"status": "success", "message": "Stopped ⏹️"})
        
    return jsonify({"status": "error", "message": "Unknown command"})

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port, use_reloader=False)

# Pyrogram ও অন্যান্য মডিউল ইমপোর্ট
from pyrogram import Client, idle

async def main():
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN_2")
    
    print("Telegram client / Py-tgcalls loop started successfully...")
    await idle()

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ফ্লাস্ক ওয়েব সার্ভার রান করা
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # মেইন থ্রেডে অ্যাসিনক্রোনাস লুপ রান করা
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process stopped.")
