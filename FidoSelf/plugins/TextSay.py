from FidoSelf import client
import asyncio

@client.Cmd(pattern=f"(?i)^\{client.cmd}TSay ([\S\s]*)$")
async def tsay(event):
    text = event.pattern_match.group(1)
    sleep = client.DB.get_key("SAY_SLEEP") or 1
    sleep = int(sleep) if str(sleep).isdigit() else float(sleep)
    new = ""
    for par in text:
        new += par
        await event.edit(new)
        await asyncio.sleep(sleep)

@client.Cmd(edits=False)
async def autosay(event):
    if event.is_cmd or not event.text: return
    mode = client.DB.get_key("AUTO_SAY_MODE") or "off"
    sleep = client.DB.get_key("SAY_SLEEP") or 1
    sleep = int(sleep) if str(sleep).isdigit() else float(sleep)
    if mode == "off": return
    text = str(event.text)
    new = ""
    for par in text:
        new += par
        await event.edit(new)
        await asyncio.sleep(sleep)
