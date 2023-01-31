from FidoSelf import client

STRINGS = {
    "EN": {
        "notrealm": "^{STR} Please Send In Group To Set Realm Chat!$",
        "realm": "^{STR} This Chat Was Set For Realm Chat!$",
        "notbackup": "^{STR} Please Send In Channel To Set Backup Channel!$",
        "backup": "^{STR} This Channel Was Set For Backup Channel!$",    },
    "FA": {
        "notrealm": "^{STR} لطفا داخل یک گروه ارسال کنید تا ریلم چت تنظیم شود!$",
        "realm": "^{STR} این چت برای ریلم چت تنظیم شد!$",
        "notbackup": "^{STR} لطفا داخل یک چنل ارسال کنید تا چنل پشتیبان تنظیم شود!$",
        "backup": "^{STR} این چت برای چنل پشتیبان تنظیم شد!$",
    },
}

@client.Command(
    commands={
        "EN": "Set (Realm|BackUp)",
        "FA": "تنظیم (ریلم|پشتیبان)",
     }
)
async def ping(event):
    text = client.get_string("wait")
    await event.edit(text)
    mode = event.pattern_match.group(1).title()
    if mode in ["Realm", "ریلم"]:
        if not event.is_group:
            text = client.get_string("notrealm", STRINGS)
            return await event.edit(text)
        client.DB.set_key("REALM_CHAT", event.chat_id)
        client.realm = event.chat_id
        text = client.get_string("realm", STRINGS)
        await event.edit(text)
    elif mode == ["Backup", "پشتیبان"]:
        if not event.is_ch:
            text = client.get_string("notbackup", STRINGS)
            return await event.edit(text)
        client.DB.set_key("BACKUP_CHANNEL", event.chat_id)
        client.backch = event.chat_id
        text = client.get_string("backup", STRINGS)
        await event.edit(text)

Category = "Settings"
Plugin = {
    "EN": "Setting Chats",
    "FA": "تنظیم چت ها",
}
Note = {
    "EN": "Set Coustom Realm Chat And BackUp Channel!",
    "FA": "تنظیم ریلم چت و چنل پشتیبان دلخواه",
}
note = "client.HELP.update({
    Plugin: {
        "Category": Category,
        "Note": Note,
        "Commands": {
            "EN": {
                "{CMD}Set Realm": "To Set Coustom Realm Chat",
                "{CMD}Set BackUp": "To Set Coustom BackUp Channel",
            },
            "FA": {
                "تنظیم ریلم": "برای تنظیم ریلم چت دلخواه{CMD}",
                "تنظیم پشتیبان": "برای تنظیم چنل پشتیبان دلخواه{CMD}",
             },
        },
    }
})
