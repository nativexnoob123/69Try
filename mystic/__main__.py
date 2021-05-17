import asyncio
import importlib
import re

import uvloop
from pyrogram import filters, idle
from mystic.modules import ALL_MODULES

loop = asyncio.get_event_loop()
HELPABLE = {}
async def start_bot():
    global COMMANDS_COUNT
    for module in ALL_MODULES:
        imported_module = importlib.import_module("mystic.modules." + module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                              WBB                              |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print(f"BOT STARTED")
    await idle()

    
    
if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())    
