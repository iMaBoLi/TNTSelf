from FidoSelf.functions.BaseClient import FidoClient
from telethon.sessions import StringSession
from FidoSelf import config
import time

START_TIME = time.time()

client = FidoClient(
    session=StringSession(str(config.SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    device_model="FidoSelf",
    app_version="0.4.1",
)

client.bot = FidoClient(
    session=None,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)
