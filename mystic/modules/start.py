from mystic import app
from pyrogram import filters

__MODULE__ = "Start"
__HELP__ = "•Anime uwu•\n\n/anime - search anime on AniList\n /manga - search manga on Anilist\n /char - search character on Anilist\n /nhentai ID - returns the nhentai in telegraph instant preview format."


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hi Vro")
    
    
@app.on_message(filters.sticker)
async def start(_, message):
    await message.reply_text(f"{message.message_id}")
    await message.reply_text("Hi Vro")
