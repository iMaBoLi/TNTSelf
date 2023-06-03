from FidoSelf import client

@client.Command(notcmd=True)
async def replace(event):
    if event.is_cmd or not event.text: return
    mode = client.DB.get_key("AUTO_REPLACE_MODE") or "on"
    if mode == "on":
        try:
            text = await client.AddVars(str(event.text), event)
            await event.edit(text)
        except:
            pass