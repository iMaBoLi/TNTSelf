from FidoSelf import client

__INFO__ = {
    "Category": "Groups",
    "Name": "Ban",
    "Info": {
        "Help": "To Ban/UnBan Users In Chats!",
        "Commands": {
            "{CMD}Ban": {
                "Help": "To Ban User",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}UnBan": {
                "Help": "To UnBan User",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notacs": "**✶ You Do Not Have Access To Ban/UnBan Users!**",
    "banuser": "**The User** ( {} ) **Was Banned In This Chat!**",
    "errorban": "**The User** ( {} ) **Is Not Banned!**\n**Error:** ( `{}` )",
    "unbanuser": "**The User** ( {} ) **Was UnBanned In This Chat!**",
    "errorunabn": "**The User** ( {} ) **Is Not UnBanned!**\n**Error:** ( `{}` )",
}

@client.Command(command="Ban ?(.*)?")
async def banuser(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(STRINGS["notacs"])
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, view_messages=False)
    except Exception as error:
        return await event.edit(STRINGS["errorban"].format(mention, error))
    text = STRINGS["banuser"].format(mention)
    await event.edit(text)
    
@client.Command(command="UnBan ?(.*)?")
async def unbanuser(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(STRINGS["notacs"])
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id)
    except Exception as error:
        return await event.edit(STRINGS["errorunban"].format(mention, error))
    text = STRINGS["unbanuser"].format(mention)
    await event.edit(text)