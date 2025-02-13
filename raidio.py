from pyrogram import Client
from pytgcalls import PyTgCalls, Stream
import os

API_ID = 12799559
API_HASH = "077254e69d93d08357f25bb5f4504580"

if not os.path.exists("music_stream.session"):
    phone_number = input("Enter your phone number (with country code, e.g., +1234567890): ")
    app = Client("music_stream", api_id=API_ID, api_hash=API_HASH, phone_number=phone_number)
else:
    app = Client("music_stream", api_id=API_ID, api_hash=API_HASH)

call = PyTgCalls(app)

CHAT_ID = -1002351120556


MUSIC_STREAM_URL = "https://www.youtube.com/live/jfKfPfyJRdk?si=L1JqDef8Pwdfcsna" 

async def start_stream():
    await call.start()
    await call.join_group_call(
        CHAT_ID,
        Stream(
            MUSIC_STREAM_URL,
            repeat=True 
        )
    )
    print("Streaming started!")

@app.on_message()
async def restart_stream(client, message):
    if message.text == "/restart":
        await call.leave_group_call(CHAT_ID)
        await start_stream()
        await message.reply("Stream restarted!")

@app.on_message()
async def stop_stream(client, message):
    if message.text == "/stop":
        await call.leave_group_call(CHAT_ID)
        await message.reply("Streaming stopped!")

@app.on_message()
async def play_new_url(client, message):
    if message.text.startswith("/play "):
        new_url = message.text.split("/play ", 1)[1]
        await call.leave_group_call(CHAT_ID)
        await call.join_group_call(CHAT_ID, Stream(new_url, repeat=True))
        await message.reply(f"Now streaming: {new_url}")

app.run()
