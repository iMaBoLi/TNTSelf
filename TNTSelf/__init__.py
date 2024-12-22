from telethon import TelegramClient
from TNTSelf.MultiClient import TelClient
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

MAINCONFIG = "../tmp/config.txt"
DATA = open(MAINCONFIG, "r").read()
SESSIONS = eval(DATA)

try:
    client = TelClient(
        sessions=SESSIONS,
        app_version=__version__,
    )
except Exception as error:
    LOGS.error("• Login To Accounts Was Unsuccessful!")
    LOGS.error(format_exc())

LOGS.info("• Login Api Bot ...")

BOT_SESSION = "1BJWap1sBuyCO-P8-X9ejsMyf7ukard_RJNXXCGlP-_KiEmSU7jH_diwqrUMFiaKUJcujbwErb4VoyRwyoS9JA4Ti8EH80ZCvk6WacNJ0D0gG6RO0hD7XxsvPjy0EBgxFyspNQZA4fiKEMKRutSVL4yRnHsNK18nB9k3sL08XrImo7WZk2LNxBDyLDQkHKkA71TVh_cw7Lofv818KhTqL46jAix90Rndo3KCu20RABqCymbX7ZM_l3b6CbIdhbNtObVrXU4JltXvBmrTE3b_cFrjciZyoSS0DhDct68Z8VGcdsd_qMFX13teZG1_xwcS1H9wew5k8zRBf8svOMoaNGjTh7-YpGvE="
BOT_APIID = 22317398
BOT_APIHASH = "f9bfaf9bad8b7787e0159f32ee9ef88f"

try:
    client.bot = TelegramClient(
        session=StringSession(BOT_SESSION),
        api_id=BOT_APIID,
        api_hash=BOT_APIHASH,
    ).start()
except Exception as error:
    LOGS.error("• Login To Bot Was Unsuccessful!")
    LOGS.error(error)

LOGS.info("• Logins Was Completed!")

client.LOGS = LOGS
client.__version__ = __version__
client.START_TIME = time.time()
