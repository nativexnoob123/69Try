from mystic import app
from pyrogram import filters

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hi Vro")
