from telethon import TelegramClient
from TNTSelf.client import TelClients
from telethon.sessions import StringSession
from logging import INFO, getLogger, basicConfig, FileHandler, StreamHandler
from traceback import format_exc
import time
import sys

__version__ = "3.10.6"

LOGS = getLogger("TNTSelf")
basicConfig(
    format="%(asctime)s | %(message)s",
    level=INFO,
    datefmt="%H:%M",
    handlers=[FileHandler("TNT.log"), StreamHandler()],
)

LOGS.info("• Login To Accounts And Bots ...")

MAINCONFIG = "../tmp/config.txt"
DATA = open(MAINCONFIG, "r").read()
SESSIONS = eval(DATA)

try:
    clients = TelClients(sessions=SESSIONS)
except Exception as error:
    LOGS.error("• Error In Logins:")
    LOGS.error(format_exc())

LOGS.info("• Logins To Account And Bots Was Completed!")

clients.LOGS = LOGS
clients.__version__ = __version__
clients.START_TIME = time.time()