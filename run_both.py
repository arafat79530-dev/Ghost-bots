import os, threading, time
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "BOTH BOTS LIVE - GHOST"

def start_bot1():
    try:
        import bot1
        bot1.main()
    except Exception as e:
        print(f"Bot1 Error: {e}")

def start_bot2():
    try:
        import bot2
        bot2.run()
    except Exception as e:
        print(f"Bot2 Error: {e}")

threading.Thread(target=start_bot1, daemon=True).start()
time.sleep(3)
threading.Thread(target=start_bot2, daemon=True).start()

app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
