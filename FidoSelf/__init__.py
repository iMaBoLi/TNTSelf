from FidoSelf.functions.client import FidoClient
from telethon.sessions import StringSession
from FidoSelf import config
from FidoSelf.database import DB
import time

START_TIME = time.time()

client = FidoClient(
    session=StringSession(str(config.SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    device_model="FidoSelf",
    app_version="0.4.1",
)

async def getsession():
    session = DB.get_key("BOT_SESSION")
    if session:
        try:
            get = await client.get_messages("me", ids=int(session))
            await get.download_media("SelfBot.session")
        except:
            DB.del_key("BOT_SESSION")
            pass

client.loop.create_task(getsession())

client.bot = FidoClient(
    session="SelfBot.session",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

async def setsession():
    session = DB.get_key("BOT_SESSION")
    if not session:
        try:
            send = await client.send_file("me", "SelfBot.session")
            DB.set_key("BOT_SESSION", send.id)
        except:
            pass

client.loop.create_task(setsession())
