from FidoSelf import client
from FidoSelf import config
from FidoSelf.functions.database import *
from FidoSelf.functions.helper import *
from FidoSelf.functions.vars import *
from FidoSelf.functions.utils import *
from FidoSelf.functions.core import *
from FidoSelf.functions.tools import *
from FidoSelf.functions.loader import *
#from FidoSelf.functions.youtube import *
from FidoSelf.functions.help import *
from FidoSelf.functions.strings import STRINGS
from FidoSelf.functions.data import *

async def AddVarsToClient():
    setattr(client, "PLUGINS", get_plugins())
    setattr(client, "DB", DB)
    setattr(client, "Config", config)
    setattr(client, "checkCmd", checkCmd)
    setattr(client, "AddVars", add_vars)
    setattr(client, "mention", mention)
    setattr(client, "STRINGS", STRINGS)
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
    import os, time
    os.environ['TZ'] = "Asia/Tehran"
    time.tzset()
    
HEADERS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.46 Safari/536.5",
    "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.46 Safari/536.5",
    "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
]