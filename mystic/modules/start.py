from mystic import app
from pyrogram import filters
que = {}
__MODULE__ = "Start"
__HELP__ = "•Anime uwu•\n\n/anime - search anime on AniList\n /manga - search manga on Anilist\n /char - search character on Anilist\n /nhentai ID - returns the nhentai in telegraph instant preview format."


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hi Vro")
    
    
@app.on_message(filters.sticker)
async def start(_, message):
    global que
    user_id = message.from_user.id
    queue = que.get(message.from_user.id)
    if not queue:
        que[user_id] = []
        qeue = que.get(message.from_user.id)
        mid = message.message_id            
        appendable = [mid]      
        qeue.append(appendable)
    else:    
        qeue = que.get(message.from_user.id)
        mid = message.message_id 
        appendable = [mid]
        qeue.append(appendable)  
        queue = que.get(message.from_user.id)
        temp = []
        for t in queue:
            temp.append(t)
        now = temp[0][0]
        now += 1
        if now == message.message_id:
            await message.reply_text("HAAN BHAI BHOSDIKE")
        else:
            await message.reply_text("NAHI BHAI BHOSDIKE")
    
@app.on_message(filters.command("c"))
async def start(_, message):
    await message.reply_text("Hi Vro")
    global que
    queue = que.get(message.from_user.id)
    if not queue:
        await message.reply_text("NIKAL TERI MAA KA CHUT")
    temp = []
    for t in queue:
        temp.append(t)
    now = temp[0][0]
    msg = "**DEKH TERI MAA KA CHUT**"
    msg += f'\n{now}' 
    temp.pop(0)
    if temp:
        for song in temp:
            name = song[0]
            msg += f'\n{name}'     
    await message.reply_text(msg) 
    
   
