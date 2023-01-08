from FidoSelf import client
from FidoSelf.events import Cmd, Callback, Inline
from FidoSelf.functions import utils
from FidoSelf.strings import get_string, get_buttons
from FidoSelf.functions.github import Git
from FidoSelf.functions.helper import progress, get_ids, mention
from FidoSelf.functions.vars import add_vars
from FidoSelf import config
from FidoSelf.database import DB
import time
import os

MAX_SIZE = 104857600 * 2

async def addvars():
    ITEMS = {
        "utils": utils,
        "Git": Git,
        "Cmd": Cmd,
        "Callback": Callback,
        "Inline": Inline,
        "DB": DB,
        "lang": client.DB.get_key("LANGUAGE") or "en",
        "get_string": get_string,
        "get_buttons": get_buttons,
        "vars": add_vars,
        "mention": mention,
        "progress": progress,
        "get_ids": get_ids,
        "MAX_SIZE": MAX_SIZE,
        "me": (await client.get_me()),
    }
    for item in ITEMS:
        setattr(client, item, ITEMS[item])
    DBITEMS = {
        "str": client.DB.get_key("MESSAGES_STARTER") or "✥",
        "cmd": client.DB.get_key("SELF_CMD") or ".",
        "realm": client.DB.get_key("REALM_CHAT"),
        "backch": client.DB.get_key("BACKUP_CHANNEL"),
    }
    for item in DBITEMS:
        setattr(client, item, DBITEMS[item])
    BOTITEMS = {
        "me": (await client.bot.get_me()), 
    }
    for item in BOTITEMS:
        setattr(client.bot, item, BOTITEMS[item])

def stimezone():
    tzone = client.DB.get_key("TIME_ZONE") or "Asia/Tehran"
    os.environ["TZ"] = str(tzone)
    time.tzset()
