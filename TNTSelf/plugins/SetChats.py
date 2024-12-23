from TNTSelf import client

__INFO__ = {
    "Category": "Setting",
    "Name": "Realm",
    "Info": {
        "Help": "To Setting Your Realm Chat!",
        "Commands": {
            "{CMD}SetRealm": {
                "Help": "To Set Realm",
                "Note": "Send In Groups"
            },
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Setting",
    "Name": "BackUp",
    "Info": {
        "Help": "To Setting Your BackUp Channel!",
        "Commands": {
            "{CMD}SetBackUp": {
                "Help": "To Set BackUp",
                "Note": "Send In Channels"
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setrealm": "**{STR} This Chat Is Saved For Realm Chat!**",
    "setback": "**{STR} This Channel Is Saved For BackUp Channel!**"
}

@client.Command(command="SetRealm")
async def realm(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    event.client.DB.set_key("REALM_CHAT", event.chat_id)
    event.client.REALM = event.chat_id
    await event.edit(client.getstrings(STRINGS)["setrealm"])

@client.Command(command="SetBackUp")
async def backup(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_ch:
        return await event.edit(client.STRINGS["only"]["Channel"])
    event.client.DB.set_key("BACKUP_CHANNEL", event.chat_id)
    event.client.BACKUP = event.chat_id
    await event.edit(client.getstrings(STRINGS)["setback"])