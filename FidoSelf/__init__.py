from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from logging import INFO, getLogger, basicConfig, FileHandler, StreamHandler
from FidoSelf import config
import logging
import time
import sys

__version__ = "2.5.1"

LOGS = getLogger("FidoSelf")
basicConfig(
    format="%(asctime)s | %(name)s [%(funcName)s] : %(message)s",
    level=INFO,
    datefmt="%H:%M:%S",
    handlers=[FileHandler("Fido.log"), StreamHandler()],
)

LOGS.info("• Login Account ...")
try:
    client = TelegramClient(
        session=StringSession(config.SESSION),
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        loop=None,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
        base_logger=logging.getLogger(),
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
        loop=None,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
        base_logger=logging.getLogger(),
    ).start()
except Exception as error:
    LOGS.error("• Login To Bot Was Unsuccessful!")
    LOGS.error(error)

LOGS.info("• Logins Was Completed!")

client.LOGS = LOGS
client.__version__ = __version__
client.START_TIME = time.time()