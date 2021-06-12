from mystic import app
from pyrogram import filters
import time
import asyncio
from asyncio import Queue, QueueEmpty as Empty
from typing import Dict, Union


__MODULE__ = "Start"
__HELP__ = "•Anime uwu•\n\n/anime - search anime on AniList\n /manga - search manga on Anilist\n /char - search character on Anilist\n /nhentai ID - returns the nhentai in telegraph instant preview format."



queues: Dict[int, Queue] = {}


async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()


def get(chat_id: int) -> Union[Dict[str, str], None]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return None


def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True


def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass


def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].queue = []
    raise Empty
    
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["", "", "", ""]
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
    await message.reply_text("Hi Vro")
    
    
@app.on_message(filters.command("play"))
async def start(_, message):
    if await get(message.from_user.id):
        print("OK")
    else:
        print("Not forund")
    return    
    file_path = timse.time()
    position = await put(message.from_user.id, file_path=file_path)
    print(position)
    await asyncio.sleep(5)
    if position == 1:
        afk = get(message.from_user.id)["file_path"]
        await queues[chat_id].pop(0)
        bot_uptime = int(time.time() - afk)
        file_1 =  f"{get_readable_time((bot_uptime))}"
        print(file_1)
    if position == 2:
        afk = get(message.from_user.id)["file_path"]
        bot_uptime = int(time.time() - afk)
        file_1 =  f"{get_readable_time((bot_uptime))}"
        print(file_1)   
   
