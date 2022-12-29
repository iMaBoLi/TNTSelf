from FidoSelf import client
from datetime import datetime
from FidoSelf.plugins.ManageTime import HEARTS
import aiocron
import random
import asyncio

@client.Cmd(pattern=f"(?i)^\{client.cmd}SmartMonshi (On|Off)$")
async def smartmonshimode(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("SMART_MONSHI_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Smart Monshi Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetSmartMonshi$")
async def setsmartmonshi(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_reply:
        return await event.edit(f"**{client.str} Please Reply To Message Or Media**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    client.DB.set_key("SMART_MONSHI_MSG", str(client.backch) + ":" + str(forward.id))
    await event.edit(f"**{client.str} The Smart Monshi Message Has Been Saved!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetSmartMonshiSleep (\d*)$")
async def smartmonshisleep(event):
    await event.edit(f"**{client.str} Processing . . .**")
    sleep = event.pattern_match.group(1)
    client.DB.set_key("SMART_MONSHI_SLEEP", str(sleep))
    await event.edit(f"**{client.str} The Smart Monshi Sleep Has Been Set To {client.utils.convert_time(int(sleep))}!**")

@client.Cmd(sudo=False, edits=False)
async def smartmonshi(event):
    mode = client.DB.get_key("SMART_MONSHI_MODE")
    if mode == "off": return
    if event.is_sudo: return
    if not event.mentioned: return
    chat = client.DB.get_key("SMART_MONSHI_MSG")
    if not chat: return
    users = client.DB.get_key("SMART_MONSHI_USERS")
    if event.sender_id in users: return
    users.append(event.sender_id)
    client.DB.set_key("SMART_MONSHI_USERS", users) 
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
    sleep = client.DB.get_key("SMART_MONSHI_SLEEP") or "0"
    await asyncio.sleep(int(sleep))
    await event.reply(msg)
