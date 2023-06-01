from FidoSelf import client
from telethon import events
from traceback import format_exc
import re

def Command(
    pattern=None,
    command=None,
    handler=client.CMD,
    onlysudo=True,
    alowedits=True,
    **kwargs,
):
    if command:
        pattern = pattern or "(?i)^\{SAM}{CMD}$"
        pattern = pattern.replace("{SAM}", handler or ".")
        pattern = pattern.replace("{CMD}", command)
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if onlysudo and not event.is_sudo and not event.is_ch:
                    return
                event.reply_message = await event.get_reply_message()
                event.is_black = False
                blacks = client.DB.get_key("BLACKS") or []
                if event.sender_id in blacks:
                    event.is_black = True
                event.is_white = False
                whites = client.DB.get_key("WHITES") or []
                if event.sender_id in whites:
                    event.is_white = True
                await func(event)
            except:
                client.LOGS.error(format_exc())
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if alowedits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator
