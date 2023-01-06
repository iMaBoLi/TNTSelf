from FidoSelf import client
import asyncio

@client.Cmd(pattern=f"(?i)^\{client.cmd}AutoSay (On|off)$")
async def autosay(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    change = client.get_string("Change_1") if change == "on" else client.get_string("Change_2")
    client.DB.set_key("AUTO_SAY_MODE", mode)
    await event.edit(client.get_string("TextSay_1").format(change))

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetSaySleep (\d\.*)$")
async def saysleep(event):
    await event.edit(client.get_string("Wait"))
    sleep = event.pattern_match.group(1)
    client.DB.set_key("SAY_SLEEP", str(sleep))
    await event.edit(client.get_string("TextSay_2").format(client.utils.convert_time(int(sleep))))

@client.Cmd(edits=False)
async def say(event):
    if event.is_cmd or not event.text: return
    mode = client.DB.get_key("AUTO_SAY_MODE") or "off"
    sleep = client.DB.get_key("SAY_SLEEP") or "0"
    if mode == "off": return
    text = str(event.text)
    new = ""
    for par in text:
        new += par
        await asyncio.sleep(int(sleep))
        await event.edit(new)

@client.Cmd(pattern=f"(?i)^\{client.cmd}tSay ([\S\s*])$")
async def tsay(event):
    text = event.pattern_match.group(1)
    sleep = client.DB.get_key("SAY_SLEEP") or "0"
    new = ""
    for par in text:
        new += par
        await asyncio.sleep(int(sleep))
        await event.edit(new)
