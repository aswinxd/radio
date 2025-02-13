import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import StreamAudio

API_ID = 12799559
API_HASH = "077254e69d93d08357f25bb5f4504580"
CHAT_ID = -1002351120556  # Replace with your group ID

if not os.path.exists("music_stream.session"):
    phone_number = input("Enter your phone number (with country code, e.g., +1234567890): ")
    app = Client("music_stream", api_id=API_ID, api_hash=API_HASH, phone_number=phone_number)
else:
    app = Client("music_stream", api_id=API_ID, api_hash=API_HASH)

call = PyTgCalls(app)

MUSIC_STREAM_URL = "https://www.youtube.com/live/jfKfPfyJRdk?si=L1JqDef8Pwdfcsna"

async def start_stream(url):
    await call.start()
    ffmpeg_process = subprocess.Popen(
        ["yt-dlp", "-f", "bestaudio", "-o", "-", url],
        stdout=subprocess.PIPE
    )
    await call.join_group_call(
        CHAT_ID,
        StreamAudio(ffmpeg_process.stdout)
    )
    print("Streaming started!")

@app.on_message(filters.command("restart"))
async def restart_stream(client, message):
    await call.leave_group_call(CHAT_ID)
    await start_stream(MUSIC_STREAM_URL)
    await message.reply("Stream restarted!")

@app.on_message(filters.command("stop"))
async def stop_stream(client, message):
    await call.leave_group_call(CHAT_ID)
    await message.reply("Streaming stopped!")

@app.on_message(filters.command("play"))
async def play_new_url(client, message):
    new_url = message.text.split(maxsplit=1)[1]
    await call.leave_group_call(CHAT_ID)
    await start_stream(new_url)
    await message.reply(f"Now streaming: {new_url}")

app.run()
