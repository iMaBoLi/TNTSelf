from FidoSelf import client
from FidoSelf.events import Cmd, Callback, Inline
from FidoSelf.functions import utils
from FidoSelf.functions.github import Git
from FidoSelf.functions.helper import mention
from FidoSelf.functions.vars import add_vars
from FidoSelf import config
from FidoSelf.database import DB
import time
import os

async def addvars():
    setattr(client, "utils", utils)
    setattr(client, "Git", Git)
    setattr(client, "Cmd", Cmd)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)
    setattr(client, "DB", DB)
    setattr(client, "db", DB)
    setattr(client, "config", config)
    setattr(client, "vars", add_vars)
    setattr(client, "me", (await client.get_me()))
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "str", client.DB.get_key("MESSAGES_STARTER") or "✥")
    setattr(client, "cmd", client.DB.get_key("SELF_CMD") or ".")
    setattr(client, "realm", client.DB.get_key("REALM_CHAT"))
    setattr(client, "backch", client.DB.get_key("BACKUP_CHANNEL"))
    setattr(client, "mention", mention)

def stimezone():
    tzone = client.DB.get_key("TIME_ZONE") or "Asia/Tehran"
    os.environ["TZ"] = str(tzone)
    time.tzset()
