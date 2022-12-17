from self import client
from traceback import format_exc
import os
import sys
import re

def Cmd(
    pattern=None,
    sudo=True,
    edits=True,
    selfmode=True,
    **kwargs,
):
    selfcmds = client.DB.get_key("SELF_CMDS") or []
    if pattern:
        cmds = re.findall("\w+", str(pattern))
        for cmd in cmds:        
            if len(cmd) > 1 and cmd not in selfcmds:        
                selfcmds.append(cmd)
    client.DB.set_key("SELF_CMDS", selfcmds)
    def decorator(func):
        async def wrapper(event):
            try:
                selfall = client.DB.get_key("SELF_ALL_MODE") or "off"
                if selfmode and selfall == "off": return
                selfchats = client.DB.get_key("SELF_MODE") or []
                if selfmode and event.chat_id in selfchats: return
                event.is_cmd = False
                cmds = client.DB.get_key("SELF_CMDS")
                if cmds:
                    for cmd in cmds:
                        if event.text and cmd in event.text:
                            event.is_cmd = True
                event.reply_message = await event.get_reply_message()
                event.media_type = client.media_type(event)
                event.reply_media_type = client.media_type(event.reply_message)
                event.userid = None
                event.userinfo = None
                if event.reply_message:
                    try:
                        event.userid = event.reply_message.sender_id
                        event.userinfo = await client.get_entity(event.reply_message.sender_id)
                    except:
                        pass
                elif event.pattern_match and len(event.pattern_match.group()) > 1:
                    try:
                        userid = event.pattern_match.group(1)
                        event.userid = await client.get_peer_id(userid)
                        event.userinfo = await client.get_entity(event.userid)
                    except:
                        pass
                event.chatid = event.chat_id
                if event.pattern_match and len(event.pattern_match.group()) > 1:
                    try:
                        chatid = event.pattern_match.group(1)
                        event.chatid = await client.get_peer_id(chatid)
                    except:
                        pass
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if sudo and not event.is_sudo and not event.is_ch:
                    return
                await func(event)
            except:
                stext = f"**{client.str} Smart Self Logs **\n\n"
                stext += f"**{client.str} Chat ID :** `{event.chat_id}`\n"
                stext += f"**{client.str} User ID :** `{event.sender_id}`\n"
                stext += f"**{client.str} Traceback Info :**\n`{format_exc()}`\n"
                stext += f"**{client.str} Error Text :**\n`{sys.exc_info()[1]}`"
                await client.bot.send_message(client.realm, stext)
        client.add_event_handler(wrapper, client.events.NewMessage(pattern=pattern, **kwargs))
        if edits:
            client.add_event_handler(wrapper, client.events.MessageEdited(pattern=pattern, **kwargs))
        return wrapper
    return decorator

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
                selfall = client.DB.get_key("SELF_ALL_MODE") or "off"
                if selfall == "off": return
                selfchats = client.DB.get_key("SELF_MODE") or []
                if event.chat_id in selfchats: return
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if sudo and not event.is_sudo:
                    return await event.answer(f"{client.str} This Is Not For You‌!", alert=True)
                await func(event)
            except:
                stext = f"**{client.str} Smart Self Logs **\n\n"
                stext += f"**{client.str} Chat ID :** `{event.chat_id}`\n"
                stext += f"**{client.str} User ID :** `{event.sender_id}`\n"
                stext += f"**{client.str} Traceback Info :**\n`{format_exc()}`\n"
                stext += f"**{client.str} Error Text :**\n`{sys.exc_info()[1]}`"
                await client.bot.send_message(client.realm, stext)
        client.bot.add_event_handler(wrapper, client.events.CallbackQuery(data=data, **kwargs))
        return wrapper
    return decorator

def Inline(
    pattern=None,
    sudo=True,
    **kwargs,
):
    def decorator(func):
        async def wrapper(event):
            try:
                event.is_sudo = True if event.sender_id == client.me.id else False
                event.is_ch = True if event.is_channel and not event.is_group else False
                if sudo and not event.is_sudo: return
                await func(event)
            except:
                stext = f"**{client.str} Smart Self Logs **\n\n"
                stext += f"**{client.str} Chat ID :** `{event.chat_id}`\n"
                stext += f"**{client.str} User ID :** `{event.sender_id}`\n"
                stext += f"**{client.str} Traceback Info :**\n`{format_exc()}`\n"
                stext += f"**{client.str} Error Text :**\n`{sys.exc_info()[1]}`"
                await client.bot.send_message(client.realm, stext)
        client.bot.add_event_handler(wrapper, client.events.InlineQuery(pattern=pattern, **kwargs))
        return wrapper
    return decorator
