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
    **kwargs,
):
    if command and not pattern:
        pattern = f"(?i)^\.{command}$"
    if pattern and pattern not in client.COMMANDS:
        client.COMMANDS.append(pattern)
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                event.reply_message = await event.get_reply_message()
                if onlysudo and not event.is_sudo and not event.is_ch: return
                event.is_bot = True if (not isinstance(event.sender, types.User) or event.sender.bot) else False
                blacks = client.DB.get_key("BLACKS") or []
                event.is_black = True if event.sender_id in blacks else False
                whites = client.DB.get_key("WHITES") or []
                event.is_white = True if event.sender_id in whites else False
                if not event.is_sudo and event.is_black: return
                if event.via_bot_id: return
                await func(event)
            except:
                client.LOGS.error(format_exc())
        addhandler = client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        client.HANDLERS.append(func)
        client.HANDLERS.append(wrapper)
        if allowedits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator