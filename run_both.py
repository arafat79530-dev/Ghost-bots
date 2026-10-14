import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from flask import Flask

# ফ্লাস্ক ওয়েব সার্ভার তৈরি (রেন্ডারের পোর্ট রিকোয়েস্ট সামলানোর জন্য)
app = Flask(__name__)


@app.route("/")
def home():
  return "PREMIER GHOST Bots are running 24/7!"


# সব বট একই ফোল্ডারে থাকবে
BASE_DIR = Path(__file__).resolve().parent

BOT_FILES = [
    "ghosttutorial.py",
    "ghostai.py",
]
processes = []
log_files = []

print("PREMIER GHOST - Two Bot Launcher")
print("=" * 35)

# আগে ফাইল আছে কি না যাচাই
for filename in BOT_FILES:
  path = BASE_DIR / filename

  if not path.is_file():
    print(f"ERROR: File not found: {path}")
    print("সব বটের ফাইল একই ফোল্ডারে রাখো।")
    sys.exit(1)

try:
  for filename in BOT_FILES:
    script_path = BASE_DIR / filename
    log_path = BASE_DIR / f"{filename}.log"

    log_file = open(log_path, "a", buffering=1)
    log_files.append(log_file)

    process = subprocess.Popen(
        [sys.executable, str(script_path)],
        cwd=str(BASE_DIR),
        stdin=subprocess.DEVNULL,
        stdout=log_file,
        stderr=subprocess.STDOUT,
    )

    processes.append(process)
    print(f"STARTED: {filename} | PID: {process.pid}")

  print("=" * 35)
  print("Both bot processes have been started.")
  print("Keep this launcher running.")


  # রেন্ডারের জন্য পোর্ট বাইন্ড করে ফ্লাস্ক অ্যাপ ব্যাকগ্রাউন্ডে চালু করা
  def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


  flask_thread = threading.Thread(target=run_flask)
  flask_thread.daemon = True
  flask_thread.start()

  while True:
    for i, process in enumerate(processes):
      if process.poll() is not None:
        print(f"WARNING: {BOT_FILES[i]} stopped. Check {BOT_FILES[i]}.log")
    time.sleep(2)

except KeyboardInterrupt:
  print("\nStopping both bots...")

finally:
  for process in processes:
    if process.poll() is None:
      process.terminate()

  for process in processes:
    try:
      process.wait(timeout=5)
    except subprocess.TimeoutExpired:
      process.kill()

  for log_file in log_files:
    log_file.close()

  print("Launcher stopped.")
