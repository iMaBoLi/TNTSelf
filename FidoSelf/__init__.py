from telethon import TelegramClient
from telethon.sessions import StringSession
from logging import INFO, getLogger, basicConfig, FileHandler, StreamHandler
from FidoSelf import config
from FidoSelf.database import DB
import time

START_TIME = time.time()
__version__ = "0.7.3"

LOGS = getLogger("FidoLogs")
basicConfig(
    format="%(asctime)s | %(name)s [%(levelname)s] : %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y - %H:%M:%S",
    handlers=[FileHandler("Fido.log"), StreamHandler()],
)

LOGS.info("• Login Account ...")
client = TelegramClient(
    session=StringSession(str(config.SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    device_model="FidoSelf",
    app_version=__version__,
).start()

LOGS.info("• Login Bot ...")
client.bot = TelegramClient(
    session=StringSession(str(config.BOT_SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
).start()

LOGS.info("• Logins Was Successful!")

client.LOGS = LOGS
