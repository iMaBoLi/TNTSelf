from telethon import TelegramClient
from TNTSelf.client import TelClient
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
    tlclient = TelClient(
        sessions=SESSIONS,
        app_version=__version__,
    )
except Exception as error:
    LOGS.error("• Error In Logins:")
    LOGS.error(format_exc())

LOGS.info("• Logins To Account And Bots Was Completed!")

tlclient.LOGS = LOGS
tlclient.__version__ = __version__
tlclient.START_TIME = time.time()