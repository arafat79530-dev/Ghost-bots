import asyncio
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioParameters

# ১. আপনার টেলিগ্রাম API Credentials (my.telegram.org থেকে সংগ্রহ করুন)
API_ID = 12345678  # আপনার api_id বসান
API_HASH = "your_api_hash_here"

# টেলিগ্রাম ক্লায়েন্ট এবং కాల్സ് ইনিশিয়ালাইজেশন
app = Client(
    "audio_streamer_session",
    api_id=API_ID,
    api_hash=API_HASH
)
call_py = PyTgCalls(app)

# গ্রুপ আইডি বা ইউজারনেম (মাইনাস চিহ্ন দিয়ে শুরু হয় সুপারগ্রুপ/চ্যানেলের ক্ষেত্রে)
MY_GROUP_ID = -1001234567890      # আপনার নিজের গ্রুপের আইডি
OTHER_GROUP_ID = -1009876543210   # অন্যের গ্রুপের আইডি

async def start_streaming():
    await app.start()
    await call_py.start()
    print("🚀 Telegram Audio Call Client Started Successfully!")

    try:
        # উদাহরণ ১: নিজের গ্রুপে মাইক্রোফোন/অডিও স্ট্রিম পাঠানো (Broadcasting)
        # এখানে আপনার ফোনের মাইক ইনপুট বা কোনো অডিও ফাইল স্ট্রিম করা যাবে
        print("Connecting to your group...")
        await call_py.join_group_call(
            MY_GROUP_ID,
            AudioPiped(
                "input_stream_or_mic", # এখানে আপনার অডিও সোর্স বা মাইক্রোফোন স্ট্রিম যুক্ত হবে
                audio_parameters=AudioParameters(
                    bitrate=48000,
                )
            )
        )
        print("✅ Successfully joined and streaming in YOUR group!")

        # উদাহরণ ২: অন্যের গ্রুপে শুধু লিসেনার (Listener) হিসেবে জয়েন করা
        # অন্যের গ্রুপে জয়েন করার সময় অডিও আউটপুট मিউট বা শুধু রিসিভ মোডে রাখা যায়
        print("Connecting to other group as listener...")
        await call_py.join_group_call(
            OTHER_GROUP_ID,
            AudioPiped(
                "silent_source.raw" # সাইলেন্ট বা ব্ল্যাক হোল অডিও, যাতে আপনার মাইক সেখানে না যায়
            )
        )
        print("✅ Successfully connected to OTHER group as listener!")

    except Exception as e:
        print(f"❌ Error during group call connection: {e}")

    # প্রসেস চালু রাখার জন্য ইনফিনিট লুপ
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_streaming())
