from FidoSelf import client
from datetime import datetime
from FidoSelf.plugins.ManageTime import HEARTS
import random
import asyncio
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}Afk (On|Off)$")
async def afkmode(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("AFK_MODE", mode)
    if mode == "on":
        client.DB.set_key("AFK_LASTSEEN", str(time.time()))
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Afk Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetAfk$")
async def setafk(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_reply:
        return await event.edit(f"**{client.str} Please Reply To Message Or Media**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    client.DB.set_key("AFK_MSG", str(client.backch) + ":" + str(forward.id))
    await event.edit(f"**{client.str} The Afk Message Has Been Saved!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetAfkSleep (\d*)$")
async def afksleep(event):
    await event.edit(f"**{client.str} Processing . . .**")
    sleep = event.pattern_match.group(1)
    client.DB.set_key("AFK_SLEEP", str(sleep))
    await event.edit(f"**{client.str} The Afk Sleep Has Been Set To {client.utils.convert_time(int(sleep))}!**")

@client.Cmd(sudo=False, edits=False)
async def afk(event):
    mode = client.DB.get_key("AFK_MODE") or "off"
    if mode == "off": return
    if event.is_sudo: return
    if not event.mentioned: return
    chat = client.DB.get_key("AFK_MSG") or ""
    if not chat: return 
    user = await event.get_sender()
    me = await event.client.get_me()
    uname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    mname = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
    chattitle = (await event.get_chat()).title
    newtime = datetime.now().strftime("%H:%M")
    lastseen = time.time() - int(client.DB.get_key("AFK_LASTSEEN"))
    lastseen = client.utils.convert_time(lastseen)
    msg = await client.get_messages(int(chat.split(":")[0]), ids=int(chat.split(":")[1]))
    msg.text = msg.text.format(TITLE=chattitle, UNAME=uname, MNAME=mname, HEART=random.choice(HEARTS), TIME=newtime, LASTSEEN=lastseen)
    sleep = client.DB.get_key("AFK_SLEEP") or "0"
    await asyncio.sleep(int(sleep))
    await event.reply(msg)
