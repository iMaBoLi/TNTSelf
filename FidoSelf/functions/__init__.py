from FidoSelf import client
from FidoSelf import config
from FidoSelf.functions.database import *
from FidoSelf.functions.helper import *
from FidoSelf.functions.vars import *
from FidoSelf.functions.utils import *
from FidoSelf.functions.loader import *
from FidoSelf.data.strings import STRINGS

async def AddVarsToClient():
    setattr(client, "PLUGINS", get_plugins())
    setattr(client, "DB", DB)
    setattr(client, "Config", config)
    setattr(client, "AddVars", add_vars)
    setattr(client, "mention", mention)
    setattr(client, "STRINGS", STRINGS)
    setattr(client, "COMMANDS", [])
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", config.MAX_SIZE)
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
    import os, time
    os.environ['TZ'] = "Asia/Tehran"
    time.tzset()