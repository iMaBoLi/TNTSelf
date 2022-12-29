from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}AutoDelete (On|Off)$")
async def autodelete(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("AUTO_DELETE_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Auto Delete Messages Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetAutoDeleteSleep (\d*)$")
async def setautodeletesleep(event):
    await event.edit(f"**{client.str} Processing . . .**")
    sleep = event.pattern_match.group(1)
    client.DB.set_key("AUTO_DELETE_SLEEP", str(sleep))
    await event.edit(f"**{client.str} The Auto Delete Messages Sleep Has Been Set To {client.utils.convert_time(int(sleep))}!**")

@client.Cmd()
async def autodeleters(event):
    mode = client.DB.get_key("AUTO_DELETE_MODE") or "off"
    if mode == "on":
        sleep = client.DB.get_key("AUTO_DELETE_SLEEP") or 5
        sleep = int(sleep) * 60
        await asyncio.sleep(sleep)
        try:
            await event.delete()
        except:
            pass
