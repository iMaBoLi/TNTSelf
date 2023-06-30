from FidoSelf import client

__INFO__ = {
    "Category": "Account",
    "Plugname": "Chats Count",
    "Pluginfo": {
        "Help": "To Get Chats Count Of Your Account!",
        "Commands": {
            "{CMD}GChats": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "count": "**✿ Account Chats Count:**\n\n  **๛ All:** ( `{}` )\n  **๛ Privates:** ( `{}` )\n  **๛ SuperGroups:** ( `{}` )\n  **๛ Groups:** ( `{}` )\n  **๛ Channels:** ( `{}` )\n  **๛ Bots:** ( `{}` )",
}

@client.Command(command="GChats")
async def chatcounts(event):
    await event.edit(client.STRINGS["wait"])
    all, users, groups, sgroups, channels, bots = 0,0,0,0,0,0
    async for dialog in client.iter_dialogs():
        all += 1
        entity = dialog.entity
        type = entity.to_dict()["_"]
        if type == "User":
            if entity.bot:
                bots += 1
            else:
                users += 1
        elif type == "Channel":
            if entity.megagroup:
                sgroups += 1
            elif entity.broadcast:
                channels += 1
            else:
                groups += 1
        elif type == "Chat":
            groups += 1
    text = STRINGS["count"].format(all, users, sgroups, groups, channels, bots)
    await event.edit(text)