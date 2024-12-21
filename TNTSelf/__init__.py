from telethon import TelegramClient
from TNTSelf import MultiClient
from telethon.sessions import StringSession
from logging import INFO, getLogger, basicConfig, FileHandler, StreamHandler
from TNTSelf import config
from traceback import format_exc
import time
import sys

__version__ = "2.10.6"

LOGS = getLogger("TNTSelf")
basicConfig(
    format="%(asctime)s | %(message)s",
    level=INFO,
    datefmt="%H:%M",
    handlers=[FileHandler("TNT.log"), StreamHandler()],
)

LOGS.info("• Login Account ...")
try:
    sessions = [config.SESSION]
    client = MultiClient(api_id=config.API_ID, api_hash=config.API_HASH, sessions=sessions)
except Exception as error:
    LOGS.error("• Login To Account Was Unsuccessful!")
    LOGS.error(format_exc())

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
