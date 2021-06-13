from mystic import app, db
from pyrogram import filters
import time
import asyncio
from asyncio import Queue, QueueEmpty as Empty, QueueEmpty
from typing import Dict, Union
warnsdb = db.warns
decdb = db.dec
que = []
__MODULE__ = "Start"
__HELP__ = "•Anime uwu•\n\n/anime - search anime on AniList\n /manga - search manga on Anilist\n /char - search character on Anilist\n /nhentai ID - returns the nhentai in telegraph instant preview format."



async def is_banned_user(user_id: int) -> bool:
    user = await decdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True
  
async def add_gban_user(user_id: int):
    is_gbanned = await is_banned_user(user_id)
    if is_gbanned:
        return
    return await decdb.insert_one({"user_id": user_id})
  
async def remove_gban_user(user_id: int):
    is_gbanned = await is_banned_user(user_id)
    if not is_gbanned:
        return
    return await decdb.delete_one({"user_id": user_id})  
  


queues: Dict[int, Queue] = {}
ft: Dict[int, Queue] = {}

async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()

async def putft(chat_id: int, **kwargs) -> int:
    if chat_id not in ft:
        ft[chat_id] = Queue()
    await ft[chat_id].put({**kwargs})
    return ft[chat_id].qsize()


def get(chat_id: int) -> Union[Dict[str, str], None]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return None

def getft(chat_id: int) -> Union[Dict[str, str], None]:
    if chat_id in ft:
        try:
            return ft[chat_id].get_nowait()
        except Empty:
            return None
        
def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True

def is_emptyft(chat_id: int) -> bool:
    if chat_id in ft:
        return ft[chat_id].empty()
    return True
async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id


async def get_warns_count() -> dict:
    chats = warnsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    warns_count = 0
    for chat in await chats.to_list(length=100000000):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id}, {"$set": {"warns": warnsd}}, upsert=True
        )
        return True
    return False



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time
    
@app.on_message(filters.command("start"))
async def start(_, message):
    try:
        print("done")
    except QueueEmpty:
        print("Empty")
    except Exception as e:
        print("error")
        print(e)
    
    
@app.on_message(filters.command("play"))
async def start(_, message):
    user_id = message.from_user.id
    if not await is_banned_user(message.from_user.id):
        pass
    else:
        await message.reply_text(f"You have been banned from Yukki due to Spam Activities.\n\n**Ban Unlocks In:** 3 Mins") 
        return
    file_path = time.time()
    if is_emptyft(message.from_user.id):
        await putft(message.from_user.id, file_path=file_path)
        await putft(message.from_user.id, file_path=file_path)
        p = await putft(message.from_user.id, file_path=file_path)
        print(p)
    else:    
        position = await put(message.from_user.id, file_path=file_path)
        if position == 1:
            print("Position 1 Check")
            afk = getft(message.from_user.id)["file_path"]
            bot_uptime = int(time.time() - afk)
            file_1 =  f"{get_readable_time((bot_uptime))}"
            if (file_1.isnumeric()) == False:
                print("Position 1 Removed")
                afk = getft(message.from_user.id)["file_path"]
                afk = getft(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
            print(file_1)
        if position == 2:
            print("Position 2 Check")
            afk = getft(message.from_user.id)["file_path"]
            bot_uptime = int(time.time() - afk)
            file_1 =  f"{get_readable_time((bot_uptime))}"
            if (file_1.isnumeric()) == False:
                print("Position 2 Removed")
                afk = getft(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
            print(file_1)    
        if position == 3:
            print("Position 3 Check")
            afk = getft(message.from_user.id)["file_path"]
            bot_uptime = int(time.time() - afk)
            file_1 =  f"{get_readable_time((bot_uptime))}"
            if (file_1.isnumeric()) == False:      
                afk = get(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
            else:
                afk = get(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
                afk = get(message.from_user.id)["file_path"]
                mention = message.from_user.mention
                warns = await get_warn(0, await int_to_alpha(user_id))
                if warns:
                    warns = warns["warns"]
                else:
                    warn = {"warns": 1}
                    await add_warn(0, await int_to_alpha(user_id), warn)
                    await add_gban_user(user_id)
                    await message.reply_text(f"**__Potential Spammer Detected__**\n\n{mention}! You have been detected as spammer by Yukki's spamwatch. You won't be able to use Yukki for next **3 mins**.\nYou have **1/5** detections now. Exceeding the Limit will lead to a **permanent** ban from Yukki.\n\n**Possible Reason:-**Gave more than 3 Queries to Yukki within 1 min")
                if warns >= 5:
                    await add_gban_user(user_id)
                    await message.reply_text(f"**__Potential Spammer Globally Taped__**\n\n{mention} ! You have tried to spam Yukki more than 5 times.\nYou are **globally banned** from using Yukki Now\n\n**Possible Reason:-**Reached 5/5 Spam Detections")
                else:
                    warn = {"warns": warns + 1}
                    await add_warn(0, await int_to_alpha(user_id), warn)
                    await add_gban_user(user_id)
                    await message.reply_text(f"**__Potential Spammer Detected__**\n\n{mention}! You have been detected as spammer by Yukki's spamwatch. You won't be able to use Yukki for next **3 mins**.\nYou have {warns+1}/5 detections now. Exceeding the Limit will lead to a permanent ban from Yukki.\n\n**Possible Reason:-**Gave more than 3 Queries to Yukki within 1 min")
                await asyncio.sleep(180)
                await remove_gban_user(user_id)     
