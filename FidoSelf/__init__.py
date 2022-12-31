from telethon import TelegramClient
from telethon.sessions import StringSession
from FidoSelf import config
from FidoSelf.database import DB
import time

START_TIME = time.time()

client = TelegramClient(
    session=StringSession(str(config.SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    device_model="FidoSelf",
    app_version="0.4.1",
)

client.bot = TelegramClient(
    session=StringSession(str(config.BOT_SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
)
