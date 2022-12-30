from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}AutoReplace (On|Off)$")
async def autoreplace(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("AUTO_REPLACE_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Auto Replace Messages Mode Has Been {change}!**")

@client.Cmd()
async def autodeleters(event):
    mode = client.DB.get_key("AUTO_REPLACE_MODE") or "on"
    if mode == "on":
        try:
            text = await client.vars(str(event.text), event)
            await event.edit(text)
        except:
            pass
