from FidoSelf import client
from telethon import events
from traceback import format_exc

def Inline(
    pattern=None,
    sudo=True,
    **kwargs,
):
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                if sudo and not event.is_sudo:
                    text = client.get_string("OtherUse_Inline")
                    return await event.answer([event.builder.article(f"{client.str} FidoSelf - PMeme", text=text)])
                await func(event)
            except:
                stext = f"{client.str} The Lastest Error:\n\n{format_exc()}"
                open("InlineError.log", "w").write(stext)
        client.bot.add_event_handler(wrapper, events.InlineQuery(pattern=pattern, **kwargs))
        return wrapper
    return decorator
