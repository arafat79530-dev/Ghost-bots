import os
import sys
import asyncio
import threading
from flask import Flask, render_template, request, jsonify

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# Flask app initialization
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    
    if command == 'mute':
        print("Action: Audio Muted via Mini App")
        return jsonify({"status": "success", "message": "Muted 🔇"})
    elif command == 'unmute':
        print("Action: Audio Unmuted via Mini App")
        return jsonify({"status": "success", "message": "Unmuted 🔊"})
    elif command == 'stop':
        print("Action: Stream Stopped via Mini App")
        return jsonify({"status": "success", "message": "Stopped ⏹️"})
        
    return jsonify({"status": "error", "message": "Unknown command"})

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

from pyrogram import Client, idle

async def main():
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN_2")
    
    print("Telegram client / Py-tgcalls loop started successfully...")
    await idle()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process stopped.")
