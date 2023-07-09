from FidoSelf import client

__INFO__ = {
    "Category": "Account",
    "Name": "Chats Count",
    "Info": {
        "Help": "To Get Chats Count Of Your Account!",
        "Commands": {
            "{CMD}CCount": {
                "Help": "To Get Count",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "count": "**{STR} Account Chats Count:**\n\n  **{STR} All:** ( `{}` )\n  **{STR} Privates:** ( `{}` )\n  **{STR} SuperGroups:** ( `{}` )\n  **{STR} Groups:** ( `{}` )\n  **{STR} Channels:** ( `{}` )\n  **{STR} Bots:** ( `{}` )"
}

@client.Command(command="CCount")
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
    text = client.getstrings(STRINGS)["count"].format(all, users, sgroups, groups, channels, bots)
    await event.edit(text)