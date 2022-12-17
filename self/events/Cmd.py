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
                selfall = client.DB.get_key("SELF_ALL_MODE") or "off"
                if selfmode and selfall == "off": return
                selfchats = client.DB.get_key("SELF_MODE") or []
                if selfmode and event.chat_id in selfchats: return
                event.reply_message = await event.get_reply_message()
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if sudo and not event.is_sudo and not event.is_ch: return
                await func(event)
            except:
                stext = f"{client.str} The Lastest Error:\n\n{format_exc()}"
                open("CmdError.log", "w").write(stext)
                await client.bot.send_file("TheaBoLi", "CmdError.log")
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if edits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator
