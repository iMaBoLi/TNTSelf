from FidoSelf import client
from FidoSelf.events import Command, Callback, Inline
from FidoSelf.functions import *
import time
import os

async def addvars():
    setattr(client, "utils", utils)
    setattr(client, "Command", Command)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)
    setattr(client, "DB", DB)
    setattr(client, "lang", client.DB.get_key("LANGUAGE") or "EN")
    setattr(client, "get_string", get_string)
    setattr(client, "config", config)
    setattr(client, "vars", add_vars)
    setattr(client, "mention", mention)
    setattr(client, "progress", progress)
    setattr(client, "mediatype", mediatype)
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", MAX_SIZE)
    setattr(client, "me", (await client.get_me()))
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "str", client.DB.get_key("MESSAGES_STARTER") or "✥")
    setattr(client, "cmd", client.DB.get_key("SELF_CMD") or ".")
    setattr(client, "realm", client.DB.get_key("REALM_CHAT") or client.me.id)
    setattr(client, "backch", client.DB.get_key("BACKUP_CHANNEL"))
