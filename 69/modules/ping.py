from 69 import app
from datetime import datetime


@app.on_message(filters.command("ping"))
async def ping(_, message):
    start = datetime.now()
    response = await message.reply_text("WAIT BRO")
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(f"**Pong!**\n`⚡{resp} ms`\n\n<b><u>Yukki System Stats:</u></b>{uptime}")   
