from 69 import app

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hi Vro")
