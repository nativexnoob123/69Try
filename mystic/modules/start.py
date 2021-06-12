from mystic import app
from pyrogram import filters
import time
import asyncio
from asyncio import Queue, QueueEmpty as Empty, QueueEmpty
from typing import Dict, Union


__MODULE__ = "Start"
__HELP__ = "•Anime uwu•\n\n/anime - search anime on AniList\n /manga - search manga on Anilist\n /char - search character on Anilist\n /nhentai ID - returns the nhentai in telegraph instant preview format."



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

def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass
        
def task_doneft(chat_id: int):
    if chat_id in ft:
        try:
            ft[chat_id].task_done()
        except ValueError:
            pass

def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].queue = []
    raise Empty
 
def clearft(chat_id: int):
    if chat_id in ft:
        if ft[chat_id].empty():
            raise Empty
        else:
            ft[chat_id].queue = []
    raise Empty
    
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
        afk = getft(message.from_user.id)["file_path"]
        afk = getft(message.from_user.id)["file_path"]
        afk = getft(message.from_user.id)["file_path"]
        afk = getft(message.from_user.id)["file_path"]
        print("done")
    except QueueEmpty:
        print("Empty")
    except Exception as e:
        print("error")
        print(e)
    
    
@app.on_message(filters.command("play"))
async def start(_, message):
    file_path = time.time()
    if is_emptyft(message.from_user.id):
        await putft(message.from_user.id, file_path=file_path)
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
                print("Position 1 Blocked")
                task_done(message.from_user.id)
                task_doneft(message.from_user.id)
                task_doneft(message.from_user.id)
                task_doneft(message.from_user.id)
            print(file_1)
        if position == 2:
            print("Position 2 Check")
            afk = getft(message.from_user.id)["file_path"]
            bot_uptime = int(time.time() - afk)
            file_1 =  f"{get_readable_time((bot_uptime))}"
            if (file_1.isnumeric()) == False:
                print("Position 2 Blocked")
                task_done(message.from_user.id)
                task_done(message.from_user.id)
                task_doneft(message.from_user.id)
                task_doneft(message.from_user.id)
                task_doneft(message.from_user.id)
            print(file_1)  
        if position == 3:
            print("Position 3 Check")
            afk = getft(message.from_user.id)["file_path"]
            bot_uptime = int(time.time() - afk)
            file_1 =  f"{get_readable_time((bot_uptime))}"
            if (file_1.isnumeric()) == False:
                print("Position 3 Blocked")
                task_done(message.from_user.id)
                task_done(message.from_user.id)
                task_done(message.from_user.id)
                task_doneft(message.from_user.id)
                task_doneft(message.from_user.id)
                task_doneft(message.from_user.id)
            print(file_1)
        if position == 4:
            task_done(message.from_user.id)
            task_done(message.from_user.id)
            task_done(message.from_user.id)
            task_done(message.from_user.id)
            task_doneft(message.from_user.id)
            task_doneft(message.from_user.id)
            task_doneft(message.from_user.id)
            print("Position 4 Check")
            await message.reply_text("Too Fast Blocked")
   
   
