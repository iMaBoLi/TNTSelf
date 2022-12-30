from FidoSelf import client
from datetime import datetime
import random
import asyncio
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}Afk (On|Off)$")
async def afkmode(event):
    await event.edit(client.get_string("Afk_1").format(client.str))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("AFK_MODE", mode)
    if mode == "on":
        client.DB.set_key("AFK_LASTSEEN", str(time.time()))
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(client.get_string("Afk_2").format(client.str, change))

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetAfk$")
async def setafk(event):
    await event.edit(client.get_string("Afk_1").format(client.str))
    if not event.is_reply:
        return await event.edit(client.get_string("Afk_3").format(client.str))
    if not client.backch:
        return await event.edit(client.get_string("Afk_4").format(client.str))
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(client.get_string("Afk_5").format(client.str))
    client.DB.set_key("AFK_MSG", str(client.backch) + ":" + str(forward.id))
    await event.edit(client.get_string("Afk_6").format(client.str))

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetAfkSleep (\d*)$")
async def afksleep(event):
    await event.edit(client.get_string("Afk_1").format(client.str))
    sleep = event.pattern_match.group(1)
    client.DB.set_key("AFK_SLEEP", str(sleep))
    await event.edit(client.get_string("Afk_7").format(client.str, client.utils.convert_time(int(sleep))))

@client.Cmd(sudo=False, edits=False)
async def afk(event):
    mode = client.DB.get_key("AFK_MODE") or "off"
    if mode == "off": return
    if event.is_sudo: return
    if not event.mentioned: return
    chat = client.DB.get_key("AFK_MSG")
    if not chat: return 
    lastseen = time.time() - int(client.DB.get_key("AFK_LASTSEEN"))
    lastseen = client.utils.convert_time(lastseen)
    msg = await client.get_messages(int(chat.split(":")[0]), ids=int(chat.split(":")[1]))
    msg.text = await client.vars(msg.text, event)
    msg.text = msg.text.replace("LASTSEEN", lastseen)
    sleep = client.DB.get_key("AFK_SLEEP") or "0"
    await asyncio.sleep(int(sleep))
    await event.reply(msg)
