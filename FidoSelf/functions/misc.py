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

MAX_SIZE = 102400

async def addvars():
    setattr(client, "utils", utils)
    setattr(client, "Git", Git)
    setattr(client, "Cmd", Cmd)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)
    setattr(client, "DB", DB)
    setattr(client, "lang", client.DB.get_key("LANGUAGE") or "en")
    setattr(client, "get_string", get_string)
    setattr(client, "get_buttons", get_buttons)
    setattr(client, "config", config)
    setattr(client, "vars", add_vars)
    setattr(client, "mention", mention)
    setattr(client, "progress", progress)
    setattr(client, "get_ids", get_ids)
    setattr(client, "MAX_SIZE", MAX_SIZE)
    setattr(client, "me", (await client.get_me()))
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "str", client.DB.get_key("MESSAGES_STARTER") or "✥")
    setattr(client, "cmd", client.DB.get_key("SELF_CMD") or ".")
    setattr(client, "realm", client.DB.get_key("REALM_CHAT"))
    setattr(client, "backch", client.DB.get_key("BACKUP_CHANNEL"))

def stimezone():
    tzone = client.DB.get_key("TIME_ZONE") or "Asia/Tehran"
    os.environ["TZ"] = str(tzone)
    time.tzset()
