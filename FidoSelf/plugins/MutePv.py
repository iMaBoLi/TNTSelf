from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}MutePv (On|Off)$")
async def mutepv(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("MUTE_PV", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("MutePv_1").format(change))

@client.Command(sudo=False, edits=False)
async def muter(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("MUTE_PV") or "off"
    if mode == "on":
        await event.delete()
