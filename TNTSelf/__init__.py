from telethon import TelegramClient
from TNTSelf.MultiClient import MultiClient
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
    sessions = {
        1: {
            "session": config.SESSION,
            "api_id": config.API_ID,
            "api_hash": config.API_HASH,
        },
        2: {
            "session": "1BJWap1sBu6EHKg2H4-L-uaOD4FJqrluN85Va3dSp-Era9fBumXQr1uHIisIt_DbumlAvts5UbI-AKOIeBQSOp_Bb-mOqjfj4kdcsrnOGLJz9Jjvgp1jmC5uHNKl5gjlvIta1h1ugrOGgAGa4uGDkbfh_JTETDybODFftFnOXF_7rCe111ID8nDJDGDS_8W1bfBPa7fLNqwdc_ymcQVAvgoV7GCDxUlBwncAoXamxz_uMo6epLcAbWhweNYdar7jbyxSJPJM4rlqO8chNdCrSOcMcYWFzifHEoLKkmHefYMh50jFTu1Xmv2d8W5VLZL1-dC0BPmrQvjtBtlxqDeHI1doODofwfk0=",
            "api_id": 29111179,
            "api_hash": "f24167b48a3c86a54a8afdd8192c92d4",
        },
    }
    client = MultiClient(sessions=sessions, app_version=__version__)
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
