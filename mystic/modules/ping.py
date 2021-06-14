from mystic import app, db
from datetime import datetime
import time
import asyncio
import re
from asyncio import Queue, QueueEmpty as Empty, QueueEmpty
from typing import Dict, Union, List
from pyrogram import filters, Client
__MODULE__ = "Ping"
__HELP__ = "Pong."

notesdb = db.notes
ffdb = db.ff
blackdb = db.black

def obj_to_str(object):
    if not object:
        return False
    string = codecs.encode(pickle.dumps(object), "base64").decode()
    return string


def str_to_obj(string: str):
    object = pickle.loads(codecs.decode(string.encode(), "base64"))
    return object


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
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

async def is_afk_user(user_id: int) -> bool:
    user = await ffdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True
  
async def add_afk_user(user_id: int):
    is_gbanned = await is_afk_user(user_id)
    if is_gbanned:
        return
    return await ffdb.insert_one({"user_id": user_id})
  
async def remove_afk_user(user_id: int):
    is_gbanned = await is_afk_user(user_id)
    if not is_gbanned:
        return
    return await ffdb.delete_one({"user_id": user_id})  



async def _get_notes(chat_id: int) -> Dict[str, int]:
    _notes = await notesdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]


async def get_note_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_notes(chat_id):
        _notes.append(note)
    return _notes


async def get_note(chat_id: int, name: str) -> Union[bool, dict]:
    name = "Hello"
    _notes = await _get_notes(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_user_afk(chat_id: int, name: str, note: dict):
    name ="Hello"
    _notes = await _get_notes(chat_id)
    _notes[name] = note
    await notesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )

    
async def delete_afk_user(chat_id: int, name: str) -> bool:
    notesd = await _get_notes(chat_id)
    name = "Hello"
    if name in notesd:
        del notesd[name]
        await notesdb.update_one(
            {"chat_id": chat_id}, {"$set": {"notes": notesd}}, upsert=True
        )
        return True
    return False

async def get_allafk_users(chat_id: int) -> List[str]:
    _filters = await blackdb.find_one({"chat_id": chat_id})
    if not _filters:
        return []
    return _filters["filters"]

async def save_blacklist_filter(chat_id: int, word: str):
    word = word.lower().strip()
    _filters = await get_allafk_users(chat_id)
    _filters.append(word)
    await blackdb.update_one(
        {"chat_id": chat_id}, {"$set": {"filters": _filters}}, upsert=True
    )
async def delete_blacklist_filter(chat_id: int, word: str) -> bool:
    filtersd = await get_allafk_users(chat_id)
    word = word
    if word in filtersd:
        filtersd.remove(word)
        await blackdb.update_one(
            {"chat_id": chat_id}, {"$set": {"filters": filtersd}}, upsert=True
        )
        return True
    return False

chat_watcher_group = 5  
@app.on_message(group=chat_watcher_group)
async def afk_check(_, message):
    user_id = message.from_user.id
    a = 1
    name = "Hello"
    if message.text:    
        input = message.text
    else:
        input = "None"
    if "@" in input:
        print("@ input")
        input = message.text.lower().strip()
        afkusers = await get_allafk_users(200)
        for word in afkusers:
            print("I am Here")
            pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
            if re.search(pattern, input, flags=re.IGNORECASE):

                _note = await get_note(MNO, name)
            else:
                print("MNO NHI MILA MADARCHOD")
            if not _note:
                print("None FOUND USER AFK IN @")
                pass
            else:
                if await is_afk_user(MNO):
                    await remove_afk_user(MNO)  
                    return
                print("Found @ user")
                timeafk = _note["time"]
                print(timeafk)
                finaltime = int(time.time() - timeafk)
                seenago =  f"{get_readable_time((finaltime))}"
                reasonafk = _note["data"]
                user = _note["user"]
                if int(user) == int(message.from_user.id):
                    await delete_afk_user(H.id, name)
                if _note["type"] == "text":
                    if reasonafk != "None":
                        await message.reply_text(f"**__{MN} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasonafk}", disable_web_page_preview=True)
                        return
                    else:
                        await message.reply_text(f"**__{MN} is AFK__**\n\n__Last Seen:__ {seenago} ago", disable_web_page_preview=True)   
                        return
                elif _note["type"] == "animation":
                    reasongif = _note["reason"]
                    if reasongif == "None":
                        await message.reply_animation(_note["data"], caption = f"**__{MN} is AFK__**\n\n__Last Seen:__ {seenago} ago")
                        return
                        disable_web_page_preview=True
                    else:
                        await message.reply_animation(_note["data"], caption = f"**__{MN} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasongif}")
                        return
                        disable_web_page_preview=True
                else:
                    reasonsticker = _note["reason"]
                    if reasonsticker == "None":
                        await message.reply_sticker(_note["data"])
                        await message.reply_text(f"**__{MN} is AFK__**\n\n__Last Seen:__ {seenago} ago", disable_web_page_preview=True)
                        return
                    else:
                        await message.reply_sticker(_note["data"])
                        await message.reply_text(f"**__{MN} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasonsticker}", disable_web_page_preview=True)
                        return
                    

    if a == 1:
        _note = await get_note(message.from_user.id, name)
        if not _note:
            print("None Found reply")
            pass
        else:
            if await is_afk_user(message.from_user.id):
                await remove_afk_user(user_id)  
                return
            print("Found direct")
            timeafk = _note["time"]
            print(timeafk)
            finaltime = int(time.time() - timeafk)
            seenago =  f"{get_readable_time((finaltime))}"
            reasonafk = _note["data"]
            user = _note["user"]
            if int(user) == int(message.from_user.id):
                await delete_afk_user(message.from_user.id, name)
                if _note["type"] == "text":
                    if reasonafk != "None":
                        await message.reply_text(f"**__{message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}\n__Reason:__ {reasonafk}", disable_web_page_preview=True)
                        return
                    else:
                        await message.reply_text(f"**__{message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}", disable_web_page_preview=True)  
                        return
                elif _note["type"] == "animation":
                    reasongif = _note["reason"]
                    if reasongif == "None":
                        await message.reply_animation(_note["data"], caption = f"**__{message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}")
                        return
                        disable_web_page_preview=True
                    else:
                        await message.reply_animation(_note["data"], caption = f"**__{message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}\n__Reason:__ {reasongif}")
                        return
                        disable_web_page_preview=True        
                else:
                    reasonsticker = _note["reason"]
                    if reasonsticker == "None":
                        await message.reply_text(f"**__{message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}", disable_web_page_preview=True)
                        return
                    else:
                        await message.reply_text(f"**__{message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}\n__Reason:__ {reasonsticker}", disable_web_page_preview=True)  
                        return   
    if message.reply_to_message:
        print("Reply")
        _note = await get_note(message.reply_to_message.from_user.id, name)
        if not _note:
            print("None Found reply")
            pass
        else:
            print("Found reply")
            timeafk = _note["time"]
            print(timeafk)
            finaltime = int(time.time() - timeafk)
            seenago =  f"{get_readable_time((finaltime))}"
            reasonafk = _note["data"]
            user = _note["user"]
            print(user)
            if int(user) == int(message.from_user.id):
                await delete_afk_user(message.reply_to_message.from_user.id, name)
                if _note["type"] == "text":
                    if reasonafk != "None":
                        await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}\n__Reason:__ {reasonafk}", disable_web_page_preview=True)
                        return
                    else:
                        await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}", disable_web_page_preview=True)  
                        return
                elif _note["type"] == "animation":
                    reasongif = _note["reason"]
                    if reasongif == "None":
                        await message.reply_animation(_note["data"], caption = f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}")
                        return
                        disable_web_page_preview=True
                    else:
                        await message.reply_animation(_note["data"], caption = f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}\n__Reason:__ {reasongif}")
                        return
                        disable_web_page_preview=True        
                else:
                    reasonsticker = _note["reason"]
                    if reasonsticker == "None":
                        await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}", disable_web_page_preview=True)
                        return
                    else:
                        await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago}\n__Reason:__ {reasonsticker}", disable_web_page_preview=True)  
                        return   
            if _note["type"] == "text":
                if reasonafk != "None":
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasonafk}", disable_web_page_preview=True)
                    return
                else:
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago", disable_web_page_preview=True)   
                    return
            elif _note["type"] == "animation":
                reasongif = _note["reason"]
                if reasongif == "None":
                    await message.reply_animation(_note["data"], caption = f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago")
                    return
                    disable_web_page_preview=True
                else:
                    await message.reply_animation(_note["data"], caption = f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasongif}")
                    return
                    disable_web_page_preview=True
            else:
                reasonsticker = _note["reason"]
                if reasonsticker == "None":
                    await message.reply_sticker(_note["data"])
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago", disable_web_page_preview=True)
                    return
                else:
                    await message.reply_sticker(_note["data"])
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasonsticker}", disable_web_page_preview=True)
                    return
                    


















@app.on_message(
    filters.command("afkusers") & ~filters.edited & ~filters.private
)
async def get_filterss(_, message):
    _notes = await get_note_names(200)
    if not _notes:
        await message.reply_text("**No AFK**")
    else:
        msg = f"AFK\n"
        for note in _notes:
            msg += f"**-** `{note}`\n"
        await message.reply_text(msg)


@app.on_message(
    filters.command("del") & ~filters.edited & ~filters.private
)
async def del_filter(_, message):
    word = message.text.split(None, 1)[1].strip()
    chat_id = message.chat.id
    deleted = await delete_blacklist_filter(200, word)
    if deleted:
        return await message.reply_text(f"**done {word}.**")
    await message.reply_text("**No**")



















@app.on_message(filters.command("afk"))
async def afk(_, message):
    _time = time.time() 
    _user = message.from_user.id
    from_user_mention = message.from_user.mention
    if message.from_user.username:
        name = message.from_user.username
        note = {
            "name": name,
            "user": _user,
        }
        await save_user_afk(200, name, note)
    await add_afk_user(_user)
    name = "Hello"
    if len(message.command) == 1 and not message.reply_to_message:
        print("None Pasted No reply")
        _type = "text"
        _data = "None"
        note = {
            "type": _type,
            "time": _time,
            "data": _data,
            "user": _user,
        }
        await save_user_afk(message.from_user.id, name, note)
        await message.reply_text(f"{from_user_mention} is now afk!")  
        return
    if len(message.command) > 1 and not message.reply_to_message:
        print("Message Pasted No reply")
        _data = message.text.split(None, 1)[1].strip()
        _type = "text"
        note = {
            "type": _type,
            "time": _time,
            "data": _data,
            "user": _user,
        }
        await save_user_afk(message.from_user.id, name, note)
        await message.reply_text(f"{from_user_mention} is now afk!")  
        return   
    if message.reply_to_message:
        print("reply")
        if (message.reply_to_message.animation or message.reply_to_message.sticker): 
            if message.reply_to_message.animation:
                print("gif reply")
                _data = message.reply_to_message.animation.file_id
                _type = "animation"
                if len(message.command) == 1:
                    _reason = "None"
                    note = {
                        "type": _type,
                        "time": _time,
                        "data": _data,
                        "reason": _reason,
                        "user": _user,
                    }
                if len(message.command) > 1:
                    _reason = message.text.split(None, 1)[1].strip()
                    note = {
                        "type": _type,
                        "time": _time,
                        "data": _data,
                        "reason": _reason,
                        "user": _user,
                    }
                await save_user_afk(message.from_user.id, name, note)
                await message.reply_text(f"{from_user_mention} is now afk!")  
                return
            if message.reply_to_message.sticker:
                print("sticker reply")
                _data = message.reply_to_message.sticker.file_id
                _type = "sticker"
                if len(message.command) == 1:
                    _reason = "None"
                    note = {
                        "type": _type,
                        "time": _time,
                        "data": _data,
                        "reason": _reason,
                        "user": _user,
                    }
                if len(message.command) > 1:
                    _reason = message.text.split(None, 1)[1].strip()
                    note = {
                        "type": _type,
                        "time": _time,
                        "data": _data,
                        "reason": _reason,
                        "user": _user,
                    }   
                await save_user_afk(message.from_user.id, name, note)
                await message.reply_text(f"{from_user_mention} is now afk!")  
                return
        else:
            if len(message.command) == 1:
                print("none Pasted reply")
                _type = "text"
                _data = "None"
                note = {
                    "type": _type,
                    "time": _time,
                    "data": _data,
                    "user": _user,
                 }
                await save_user_afk(message.from_user.id, name, note)
                await message.reply_text(f"{from_user_mention} is now afk!")  
                return
            if len(message.command) > 1 :
                print("Message Pasted reply")
                _data = message.text.split(None, 1)[1].strip()
                _type = "text"
                note = {
                    "type": _type,
                    "time": _time,
                    "data": _data,
                    "user": _user,
                }
                await save_user_afk(message.from_user.id, name, note)
                await message.reply_text(f"{from_user_mention} is now afk!")  
                return          
