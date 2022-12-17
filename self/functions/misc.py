from self import client
from self.events import Cmd, Callback, Inline
from self.functions import utils
from self.functions.github import Git
from self.functions.helper import media_type, mention
from self import config
from self.database import DB
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
    setattr(client, "me", (await client.get_me()))
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "str", client.DB.get_key("MESSAGES_STARTER") or "✥")
    setattr(client, "cmd", client.DB.get_key("SELF_CMD") or ".")
    setattr(client, "realm", client.DB.get_key("REALM_CHAT") or "me")
    setattr(client, "backch", client.DB.get_key("BACKUP_CHANNEL") or "me")
    setattr(client, "media_type", media_type)
    setattr(client, "mention", mention)
    setattr(client, "path", "../mo-data/SELFFILES/")
    create_folders()

def stimezone():
    tzone = client.DB.get_key("TIME_ZONE") or "Asia/Tehran"
    os.environ["TZ"] = str(tzone)
    time.tzset()

def create_folders():
    flist = ["../mo-data/SELFFILES", "../mo-data/SELFFILES/fonts", "../mo-data/SELFFILES/pics"]
    for folder in flist:
         if not os.path.exists(folder):
             os.mkdir(folder)
