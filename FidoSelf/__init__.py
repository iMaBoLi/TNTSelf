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
            get = await client.get_messages("me", ids=int(session))
            await get.download_media("MyTest.session")
        except:
            DB.del_key("BOT_SESSION")
            pass

client.loop.create_task(getsession())

client.bot = FidoClient(
    session=StringSession("1BJWap1sBu2mKaYy9jTv5C_1lbx0SziJBSDn7uSDEhs_ea8lRxCJy3jPHG3-92TQgk0jDwf7jU5X5L2KGeCtqMKncyKd85JUX1RXEgSQMYZHSMYTYZo0nfi4adjm3g1R2BICIWU0B4CaX7nfxbQjCqU8d58v9D6Jz8PlA8jIUNS6PHbbKhWGwy69O0CueiivXGplsXEitVsTWaCf7cqVZczAAJrq12MLePzqZ5aNDzGFnMmB-yicCixbTPfDgGvTSSQZUkbobeeRxu1ozTcEwqQ4RsQRBHtUXD458JyrSH9LhAMs0-Sbg_ayMpL1MgScm9tJamm0Oz8kA6qFK7N1n20of-tzMgKI="),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
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
