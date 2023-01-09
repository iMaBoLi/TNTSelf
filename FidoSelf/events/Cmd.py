from FidoSelf import client
from telethon import events
from traceback import format_exc
import re

def Cmd(
    pattern=None,
    sudo=True,
    edits=True,
    selfmode=True,
    **kwargs,
):
    cmds = client.DB.get_key("SELF_CMDS") or []
    if pattern:
        finds = re.findall("\w+", pattern)
        for find in finds:
            if len(find) > 2 and not find in cmds:
                cmds.append(find)
    client.DB.set_key("SELF_CMDS", cmds)
    def decorator(func):
        async def wrapper(event):
            try:
                selfall = client.DB.get_key("SELF_ALL_MODE") or "on"
                if selfmode and selfall == "off": return
                selfchats = client.DB.get_key("SELF_MODE") or []
                if selfmode and event.chat_id in selfchats: return
                event.reply_message = await event.get_reply_message()
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                event.is_bot = event.sender.bot
                if sudo and not event.is_sudo and not event.is_ch: return
                event.is_black = False
                blacks = client.DB.get_key("BLACKS") or []
                if event.sender_id in blacks:
                    event.is_black = True
                event.is_white = False
                whites = client.DB.get_key("WHITES") or []
                if event.sender_id in whites:
                    event.is_white = True
                cmds = client.DB.get_key("SELF_CMDS") or []
                event.is_cmd = False
                for cmd in cmds:
                    if re.search(f"(?i){cmd}", event.text): 
                        event.is_cmd = True
                await func(event)
            except:
                client.LOGS.error(format_exc())
        client.add_event_handler(wrapper, events.NewMessage(pattern=pattern, **kwargs))
        if edits:
            client.add_event_handler(wrapper, events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator
