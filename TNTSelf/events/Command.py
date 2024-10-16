from FidoSelf import client
from telethon import events, types
from traceback import format_exc
import re
import time

def Command(
    pattern=None,
    command=None,
    onlysudo=True,
    allowedits=True,
    userid=False,
    chatid=False,
    checkCmd=False,
    **kwargs,
):
    if command and not pattern:
        CMD = client.DB.get_key("CMD_SIMBEL") or "."
        if userid or chatid:
            pattern = f"(?i)^\\{CMD}{command}"
        else:
            pattern = f"(?i)^\\{CMD}{command}$"
    if pattern and pattern not in client.COMMANDS:
        client.COMMANDS.append(pattern)
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if onlysudo and not (event.is_sudo or event.out): return
                event.reply_message = await event.get_reply_message()
                event.is_bot = event.sender.bot if isinstance(event.sender, types.User) else False
                event.userid = await client.functions.getuserid(event) if userid else 0
                event.chatid = await client.functions.getchatid(event) if chatid else 0
                if checkCmd and event.text and client.functions.checkCmd(event.text): return
                blacks = client.DB.get_key("BLACK_LIST") or []
                event.is_black = True if event.sender_id in blacks else False
                whites = client.DB.get_key("WHITE_LIST") or []
                event.is_white = True if event.sender_id in whites else False
                if not event.is_sudo and event.is_black: return
                if event.via_bot_id: return
                await func(event)
            except:
                client.LOGS.error(format_exc())
                errortext = f"**• Error :**\n\n`{format_exc()}`"
                await client.bot.send_message(client.REALM, errortext)
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if allowedits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator