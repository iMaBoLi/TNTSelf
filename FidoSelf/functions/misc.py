from FidoSelf import client
from FidoSelf.events import Command, Callback, Inline
from FidoSelf.functions import *

async def addvars():
    setattr(client, "Command", Command)
    setattr(client, "Callback", Callback)
    setattr(client, "Inline", Inline)
    setattr(client, "DB", DB)
    setattr(client, "LANG", client.DB.get_key("LANGUAGE") or "EN")
    setattr(client, "get_string", get_string)
    setattr(client, "add_vars", add_vars)
    setattr(client, "HELP", {})
    setattr(client, "MAX_SIZE", MAX_SIZE)
    setattr(client, "me", (await client.get_me()))
    setattr(client.bot, "me", (await client.bot.get_me()))
    setattr(client, "STR", client.DB.get_key("MESSAGES_STARTER") or "✥")
    setattr(client, "CMD", client.DB.get_key("SELF_CMD") or "")
    setattr(client, "REALM", client.DB.get_key("REALM_CHAT") or client.me.id)
    setattr(client, "BACKUP", client.DB.get_key("BACKUP_CHANNEL"))
