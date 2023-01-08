from telethon import TelegramClient
from telethon.sessions import StringSession
from logging import INFO, getLogger, basicConfig, FileHandler, StreamHandler
from FidoSelf import config
from FidoSelf.database import DB
import time

START_TIME = time.time()
__version__ = "0.7.3"

client = TelegramClient(
    session=StringSession(str(config.SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    device_model="FidoSelf",
    app_version=__version__,
).start()

client.bot = TelegramClient(
    session=StringSession(str(config.BOT_SESSION)),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
).start()

client.LOGS = getLogger("FidoLogs")

file = "Fido.log"
basicConfig(
    format="%(asctime)s | %(name)s [%(levelname)s] : %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y - %H:%M:%S",
    handlers=[FileHandler(file), StreamHandler()],
)
