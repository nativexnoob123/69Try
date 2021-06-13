from mystic import app, db
from datetime import datetime
import time
import asyncio
from asyncio import Queue, QueueEmpty as Empty, QueueEmpty
from typing import Dict, Union, List
from pyrogram import filters, Client
__MODULE__ = "Ping"
__HELP__ = "Pong."

notesdb = db.notes

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

async def get_notes_count() -> dict:
    chats = notesdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    notes_count = 0
    for chat in await chats.to_list(length=1000000000):
        notes_name = await get_note_names(chat["chat_id"])
        notes_count += len(notes_name)
        chats_count += 1
    return {"chats_count": chats_count, "notes_count": notes_count}


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
    name = "Hello"
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



chat_watcher_group = 5  
@app.on_message(group=chat_watcher_group)
async def afk_check(_, message):
    user_id = message.from_user.id
    name = "Hello"
    if message.reply_to_message:
        print("Reply")
        _note = await get_note(message.reply_to_message.from_user.id, name)
        if not _note:
            print("None Found")
            pass
        else:
            print("Found")
            timeafk = _note["time"]
            print(timeafk)
            finaltime = int(time.time() - timeafk)
            seenago =  f"{get_readable_time((finaltime))}"
            reasonafk = _note["data"]
            user = _note["user"]
            if int(user) == int(message.reply_to_message.from_user.id):
                await delete_afk_user(message.reply_to_message.from_user.id, name)
                if reasonafk != "None":
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is back online__**\n\n__Was AFK For:__ {seenago} ago\n__Reason:__ {reasonafk}", disable_web_page_preview=True)
            if _note["type"] == "text":
                if reasonafk != "None":
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasonafk}", disable_web_page_preview=True)
                else:
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago", disable_web_page_preview=True)                             
            elif _note["type"] == "animation":
                reasongif = _note["reason"]
                if reasongif == "None":
                    await message.reply_animation(_note["data"], caption = f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago")
                    disable_web_page_preview=True
                else:
                    await message.reply_animation(_note["data"], caption = f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasongif}")
                    disable_web_page_preview=True
            else:
                reasonsticker = _note["reason"]
                if reasonsticker == "None":
                    await message.reply_sticker(_note["data"])
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago", disable_web_page_preview=True)
                else:
                    await message.reply_sticker(_note["data"])
                    await message.reply_text(f"**__{message.reply_to_message.from_user.first_name} is AFK__**\n\n__Last Seen:__ {seenago} ago\n__Reason:__ {reasonsticker}", disable_web_page_preview=True)
                    









































@app.on_message(filters.command("afk"))
async def afk(_, message):
    _time = time.time() 
    name = "Hello"
    _user = message.from_user.id
    from_user_mention = message.from_user.mention
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
