from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import time
is_config = path.exists('config.py')
if is_config:
    from config import *
else:
    from sample_config import *
    
bot_start_time = time.time()
MOD_LOAD = []
MOD_NOLOAD = []
app = Client(
    "yukki",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

app.start()
