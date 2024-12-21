from TNTSelf import client
from telethon import events
from traceback import format_exc
import re

def Callback(
    data=None,
    onlysudo=True,
    **kwargs,
):
    if data:
        data = re.compile(data)
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id in client.users else False
                if onlysudo and not event.is_sudo:
                    return await event.answer(client.STRINGS["OtherCallback"], alert=True)
                await func(event)
            except:
                client.LOGS.error(format_exc())
        client.bot.add_event_handler(wrapper, events.CallbackQuery(data=data, **kwargs))
        return wrapper
    return decorator
