from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Set(Realm|Backup)$")
async def setchats(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    if mode == "Realm":
        if not event.is_group:
            return await event.edit(client.get_string("SetChats_1"))
        client.DB.set_key("REALM_CHAT", event.chat_id)
        client.realm = event.chat_id
        await event.edit(client.get_string("SetChats_2"))
    elif mode == "Backup":
        if not event.is_ch:
            return await event.edit(client.get_string("SetChats_3"))
        client.DB.set_key("BACKUP_CHANNEL", event.chat_id)
        client.backch = event.chat_id
        await event.edit(client.get_string("SetChats_4"))

category = "Settings"
plugin = "SetChats"
note = "Set Coustom Realm Chat And BackUp And Support Channel!"
client.HELP.update({
    plugin: {
        "category": category,
        "note": note,
        "commands": {
            "{CMD}SetRealm": "To Set Coustom Realm Chat",
            "{CMD}SetBackUp": "To Set Coustom BackUp Channel",
        },
    }
})
