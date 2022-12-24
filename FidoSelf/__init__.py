from telethon import TelegramClient
from telethon.sessions import StringSession
from FidoSelf import config
import time

START_TIME = time.time()

client = TelegramClient(
    session=StringSession(str(config.SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    device_model="FidoSelf",
    app_version="0.4.1",
).start()

client.bot = TelegramClient(
    session="FidoBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
).start(bot_token=config.BOT_TOKEN)
