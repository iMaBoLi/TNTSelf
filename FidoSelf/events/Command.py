from FidoSelf import client
from telethon import events
from traceback import format_exc
import re

SELFCMDS = []

def Command(
    pattern=None,
    commands=None,
    onlysudo=True,
    alowedits=True,
    **kwargs,
):
    if commamds: 
        PAT = pattern if pattern else "(?i)^\{SAM}{CMD}$"
        SAM = client.CMD or ""
        if SAM:
            PAT = PAT.replace("{SAM}", SAM)
        else:
            PAT = PAT.replace("\{SAM}", "")
        CMD = commands[client.LANG]
        PAT = PAT.replace("{CMD}", CMD)
        pattern = PAT
        save_cmd(pattern)        
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if onlysudo and not event.is_sudo and not event.is_ch:
                    return
                event.reply_message = await event.get_reply_message()
                event.is_bot = False
                if event.sender and event.sender.to_dict()["_"] == "User":
                    event.is_bot = event.sender.bot
                event.is_black = False
                blacks = client.DB.get_key("BLACKS") or []
                if event.sender_id in blacks:
                    event.is_black = True
                event.is_white = False
                whites = client.DB.get_key("WHITES") or []
                if event.sender_id in whites:
                    event.is_white = True
                cmds = client.DB.get_key("SELF_CMDS") or []
                event.is_cmd = False
                for cmd in cmds:
                    if re.search(f"(?i){cmd}", event.text): 
                        event.is_cmd = True
                await func(event)
            except:
                client.LOGS.error(format_exc())
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if edits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator

def save_cmd(pattern):
    CMDS = []
    finds = re.findall("\w+", pattern)
    for find in finds:
        if len(find) > 2:
            CMDS.append(find)
    SELFCMDS += CMDS
