from telethon import TelegramClient
from telethon.sessions import StringSession
from logging import INFO, getLogger, basicConfig, FileHandler, StreamHandler
from FidoSelf import config
import time
import sys

__version__ = "2.10.3"

LOGS = getLogger("TNTSelf")
basicConfig(
    format="%(asctime)s | %(message)s",
    level=INFO,
    datefmt="%H:%M",
    handlers=[FileHandler("TNT.log"), StreamHandler()],
)

LOGS.info("• Login Account ...")
try:
    client = TelegramClient(
        session=StringSession(config.SESSION),
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        app_version=__version__,
    ).start()
except Exception as error:
    LOGS.error("• Login To Account Was Unsuccessful!")
    LOGS.error(error)

LOGS.info("• Login Bot ...")
try:
    client.bot = TelegramClient(
        session=StringSession(config.BOT_SESSION),
        api_id=config.API_ID,
        api_hash=config.API_HASH,
    ).start()
except Exception as error:
    LOGS.error("• Login To Bot Was Unsuccessful!")
    LOGS.error(error)

LOGS.info("• Logins Was Completed!")

client.LOGS = LOGS
client.__version__ = __version__
client.START_TIME = time.time()
