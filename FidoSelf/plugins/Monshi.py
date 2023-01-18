from FidoSelf import client
from datetime import datetime
import random
import asyncio
import time

@client.Command(pattern=f"(?i)^\{client.cmd}Monshi (On|Off)$")
async def monshimode(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("MONSHI_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("Monshi_1").format(change))

@client.Command(pattern=f"(?i)^\{client.cmd}SetMonshi$")
async def setmonshi(event):
    await event.edit(client.get_string("Wait"))
    if not event.is_reply:
        return await event.edit(client.get_string("Reply_MM"))
    if not client.backch:
        return await event.edit(client.get_string("LogCh_1"))
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(client.get_string("LogCh_2"))
    client.DB.set_key("MONSHI_MSG", str(client.backch) + ":" + str(forward.id))
    await event.edit(client.get_string("Monshi_2"))

@client.Command(pattern=f"(?i)^\{client.cmd}SetMonshiSleep (\d*)$")
async def monshisleep(event):
    await event.edit(client.get_string("Monshi_1").format(client.str))
    sleep = event.pattern_match.group(1)
    client.DB.set_key("MONSHI_SLEEP", str(sleep))
    await event.edit(client.get_string("Monshi_3").format(client.utils.convert_time(int(sleep))))

@client.Command(sudo=False, edits=False)
async def monshi(event):
    mode = client.DB.get_key("MONSHI_MODE") or "off"
    if mode == "off": return
    if event.is_sudo: return
    if not event.mentioned: return
    chat = client.DB.get_key("MONSHI_MSG")
    if not chat: return 
    msg = await client.get_messages(int(chat.split(":")[0]), ids=int(chat.split(":")[1]))
    msg.text = await client.vars(msg.text, event)
    sleep = client.DB.get_key("MONSHI_SLEEP") or "0"
    await asyncio.sleep(int(sleep))
    await event.reply(msg)
