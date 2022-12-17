from self import client
from telethon import events
from traceback import format_exc

def Cmd(
    pattern=None,
    sudo=True,
    edits=True,
    selfmode=True,
    **kwargs,
):
    def decorator(func):
        async def wrapper(event):
            try:
                await func(event)
            except:
                stext = f"{client.str} The Lastest Error:\n\n{format_exc()}"
                open("CmdError.txt", "w").write(str(stext))
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if edits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator
