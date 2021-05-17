from mystic import app
from datetime import datetime
from pyrogram import filters
__MODULE__ = "Ping"
__HELP__ = "Pong."


@app.on_message(filters.command("ping"))
async def ping(_, message):
    start = datetime.now()
    response = await message.reply_text("Ping!")
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(f"**Pong!**\n`{resp} ms`")  
