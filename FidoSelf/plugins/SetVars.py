from FidoSelf import client

STRINGS = {
    "norealm": "**Please Send In Group For Added Realm Chat!**",
    "setrealm": "**This Chat Is Saved For Realm Chat!**",
    "noback": "**Please Send In Channel For Added BackUp Or Support Channel!**",
    "setback": "**This Channel Is Saved For BackUp Channel!**",
}

@client.Command(command="SetRealm")
async def realm(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["norealm"])
    client.DB.set_key("REALM_CHAT", event.chat_id)
    client.realm = event.chat_id
    await event.edit(client.STRINGS["setrealm"])

@client.Command(command="SetBackCh")
async def backch(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_ch:
        return await event.edit(client.STRINGS["noback"])
    client.DB.set_key("BACKUP_CHANNEL", event.chat_id)
    client.backch = event.chat_id
    await event.edit(client.STRINGS["setback"])