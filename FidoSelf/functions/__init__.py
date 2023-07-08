from FidoSelf import client
from FidoSelf import config
from FidoSelf.functions.database import *
from FidoSelf.functions.helper import *
from FidoSelf.functions.utils import *
from FidoSelf.functions.core import *
from FidoSelf.functions.loader import *
from FidoSelf.functions.tools import *
from FidoSelf.functions.youtube import *
from FidoSelf.functions.github import *
from FidoSelf.functions.strings import STRINGS
from FidoSelf.functions.data import *

async def AddVarsToClient():
    setattr(client, "PLUGINS", get_plugins())
    setattr(client, "DB", DB)
    setattr(client, "Config", config)
    setattr(client, "STRINGS", STRINGS)
    setattr(client, "getstring", getstring)
    setattr(client, "COMMANDS", [])
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", config.MAX_SIZE)
    setattr(client, "PATH", "downloads/")
    setattr(client, "me", (await client.get_me()))
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "REALM", client.DB.get_key("REALM_CHAT") or client.me.id)
    setattr(client, "BACKUP", client.DB.get_key("BACKUP_CHANNEL"))
    AddHandlersToClient()
    SetTimeZone()

def AddHandlersToClient():
    from FidoSelf.events import Command, Callback, Inline
    setattr(client, "Command", Command)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)
    
def SetTimeZone():
    import os, time, jdatetime
    os.environ["TZ"] = "Asia/Tehran"
    time.tzset()
    jdatetime.set_locale("fa_IR")