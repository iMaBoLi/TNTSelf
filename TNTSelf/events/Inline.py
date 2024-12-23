from TNTSelf import client
from telethon import events
from traceback import format_exc

def Inline(
    pattern=None,
    onlysudo=True,
    **kwargs,
):
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == event.client.user.id else False
                if onlysudo and not event.is_sudo:
                    text = client.STRINGS["OtherInline"]
                    return await event.answer([event.builder.article("TNTSelf - NotForYou", text=text)])
                await func(event)
            except:
                client.LOGS.error(format_exc())
        for sinclient in client.clients:
            sinclient.bot.add_event_handler(wrapper, events.InlineQuery(pattern=pattern, **kwargs))
        return wrapper
    return decorator