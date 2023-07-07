from FidoSelf import client

__INFO__ = {
    "Category": "Groups",
    "Name": "Kick",
    "Info": {
        "Help": "To Kick Users In Chats!",
        "Commands": {
            "{CMD}Kick": {
                "Help": "To Kick User",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notacs": "**✶ You Do Not Have Access To Kick Users!**",
    "kickuser": "**The User** ( {} ) **Was Kicked In This Chat!**",
    "errorkick": "**The User** ( {} ) **Is Not Kicked!**\n**Error:** ( `{}` )",
}

@client.Command(command="Kick ?(.*)?")
async def kickuser(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(STRINGS["notacs"])
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, view_messages=False)
        await client.edit_permissions(event.chat_id, info.id)
    except Exception as error:
        return await event.edit(STRINGS["errorkick"].format(mention, error))
    text = STRINGS["kickuser"].format(mention)
    await event.edit(text)