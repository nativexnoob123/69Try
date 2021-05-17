from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import time

bot_start_time = time.time()

app = Client(
    "yukki",
    bot_token=1661608026:AAE0tqCI64fjYdPmVnDhNIbSUDo1KQJ6GU4,
    api_id=3277132,
    api_hash=50ad2ffad01bf10049638526009661a8
)

app.start()
