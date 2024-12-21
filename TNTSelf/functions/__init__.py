from TNTSelf import client
from TNTSelf import config
from TNTSelf.functions.database import *
from TNTSelf.functions.helper import *
from TNTSelf.functions.utils import *
from TNTSelf.functions.core import *
from TNTSelf.functions.loader import *
from TNTSelf.functions.tools import *
from TNTSelf.functions.youtube import *
from TNTSelf.functions.strings import STRINGS
from TNTSelf.functions.data import *
from TNTSelf.functions.fasttelethon import download_file, upload_file

async def AddVarsToClient():
    setattr(client, "PLUGINS", get_plugins())
    setattr(client, "DB", DB)
    setattr(client, "Config", config)
    setattr(client, "STRINGS", STRINGS)
    setattr(client, "getstrings", getstrings)
    setattr(client, "COMMANDS", [])
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", config.MAX_SIZE)
    setattr(client, "PATH", "downloads/")
    setattr(client, "fast_download", download_file)
    setattr(client, "fast_upload", upload_file)
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "REALM", client.DB.get_key("REALM_CHAT"))
    setattr(client, "BACKUP", client.DB.get_key("BACKUP_CHANNEL"))
    AddHandlersToClient()
    SetTimeZone()

def AddHandlersToClient():
    from TNTSelf.events import Command, Callback, Inline
    setattr(client, "Command", Command)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)
    
def SetTimeZone():
    import os, time, jdatetime
    os.environ["TZ"] = "Asia/Tehran"
    time.tzset()
    jdatetime.set_locale("fa_IR")