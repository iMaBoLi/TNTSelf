from FidoSelf import client
from datetime import datetime
from FidoSelf.plugins.ManageTime import HEARTS
import asyncio
import random

@client.Cmd(pattern=f"(?i)^\{client.cmd}OfflineMonshi (On|Off)$")
async def offlinemonshimode(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("OFFLINE_MONSHI_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Offline Monshi Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetOfflineMonshi$")
async def setofflinemonshi(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_reply:
        return await event.edit(f"**{client.str} Please Reply To Message Or Media**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    client.DB.set_key("OFFLINE_MONSHI_MSG", str(client.backch) + ":" + str(forward.id))
    await event.edit(f"**{client.str} The Offline Monshi Message Has Been Saved!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetOfflineMonshiSleep (\d*)$")
async def offlinemonshimode(event):
    await event.edit(f"**{client.str} Processing . . .**")
    sleep = event.pattern_match.group(1)
    client.DB.set_key("OFFLINE_MONSHI_SLEEP", str(sleep))
    await event.edit(f"**{client.str} The Offline Monshi Sleep Has Been Set To {client.utils.convert_time(int(sleep))}!**")

@client.Cmd(sudo=False, edits=False)
async def offlinemonshi(event):
    mode = client.DB.get_key("OFFLINE_MONSHI_MODE") or "off"
    if mode == "off": return
    if event.is_sudo: return
    if not event.mentioned: return
    chat = client.DB.get_key("OFFLINE_MONSHI_MSG") or False
    if not chat: return
    if "Online" in client.me.to_dict()["status"]["_"]: return
    user = await event.get_sender()
    me = await event.client.get_me()
    uname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    mname = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
    chattitle = (await event.get_chat()).title
    newtime = datetime.now().strftime("%H:%M")
    datefa = client.DB.get_key("DATE_FA") or "---"
    chatid = int(chat.split(":")[0])
    msgid = int(chat.split(":")[1])
    msg = await client.get_messages(chatid, ids=int(msgid)) 
    msg.text = msg.text.format(TITLE=chattitle, UNAME=uname, MNAME=mname, HEART=random.choice(HEARTS), TIME=newtime, DATE=datefa)
    sleep = client.DB.get_key("OFFLINE_MONSHI_SLEEP") or "0"
    await asyncio.sleep(int(sleep))
    await event.reply(msg)
