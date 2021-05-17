from mystic import app
from datetime import datetime
from pyrogram import filters
__MODULE__ = "Ping"
__HELP__ = "Pong."


@app.on_message(filters.command("ping"))
async def ping(_, message):
    start = datetime.now()
    response = await app.send_message(message.chat.id, "Ping!")
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_message(message.chat.id, f"**Pong!**\n`{resp} ms`")  
