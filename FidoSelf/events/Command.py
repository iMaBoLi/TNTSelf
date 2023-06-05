from FidoSelf import client
from telethon import events
from traceback import format_exc
import re

def Command(
    pattern=None,
    command=None,
    onlysudo=True,
    alowedits=True,
    **kwargs,
):
    if command and not pattern:
        pattern = f"(?i)^\.{command}$"
        
    if pattern:
        COMMANDS = client.DB.get_key("SELFCOMMANDS") or []
        if pattern not in COMMANDS:
            COMMANDS += [pattern]
            client.DB.set_key("SELFCOMMANDS", COMMANDS)

    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if onlysudo and not event.is_sudo and not event.is_ch:
                    return
                event.reply_message = await event.get_reply_message()
                event.is_bot = False
                if hasattr(event, "sender") and hasattr(event.sender, "bot"):
                    event.is_bot = event.sender.bot
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