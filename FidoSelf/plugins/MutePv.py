from FidoSelf import client

@client.Command(onlysudo=False, alowedits=False)
async def mutepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("MUTE_PV") or "off"
    if mode == "on":
        await event.delete()