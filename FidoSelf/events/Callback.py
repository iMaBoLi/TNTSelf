from FidoSelf import client
from telethon import events
from traceback import format_exc
import re

def Callback(
    data=None,
    sudo=True,
    **kwargs,
):
    if data:
        data = re.compile(data)
    def decorator(func):
        async def wrapper(event):
            try:
                selfall = client.DB.get_key("SELF_ALL_MODE") or "on"
                if selfall == "off": return
                selfchats = client.DB.get_key("SELF_MODE") or []
                if event.chat_id in selfchats: return
                event.is_sudo = True if event.sender_id == client.me.id else False
                if sudo and not event.is_sudo:
                    return await event.answer(f"{client.str} This Is Not For You‌!", alert=True)
                await func(event)
            except:
                stext = f"{client.str} The Lastest Error:\n\n{format_exc()}"
                open("CallbackError.log", "w").write(stext)
        client.bot.add_event_handler(wrapper, events.CallbackQuery(data=data, **kwargs))
        return wrapper
    return decorator
