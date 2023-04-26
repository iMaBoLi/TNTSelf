from FidoSelf import client

@client.Command()
async def replace(event):
    #if event.is_cmd or not event.text: return
    mode = client.DB.get_key("AUTO_REPLACE_MODE") or "on"
    if mode == "on":
        try:
            text = await client.vars(str(event.text), event)
            await event.edit(text)
        except:
            pass

category = "Tools"
plugin = "AutoReplace"
note = "Replace Variebels In Your Messages!"
client.HELP.update({
    plugin: {
        "category": category,
        "note": note,
        "commands": {
            "{CMD}AutoReplace <On|Off>": "To Active Or DeActive Auto Replace Mode",
        },
    }
})
