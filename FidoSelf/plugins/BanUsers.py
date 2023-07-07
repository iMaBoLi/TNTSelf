from FidoSelf import client
from datetime import timedelta

__INFO__ = {
    "Category": "Groups",
    "Name": "Ban",
    "Info": {
        "Help": "To Ban/UnBan Users In Chats!",
        "Commands": {
            "{CMD}Ban": {
                "Help": "To Ban User",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}UnBan": {
                "Help": "To UnBan User",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}TBan <Time>": {
                "Help": "To Ban User For Minutes",
                "Getid": "You Must Reply To User",
                "Input": {
                    "<Time>": "Time For Ban (Minutes)",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notacs": "**✶ You Do Not Have Access To Ban/UnBan Users!**",
    "banuser": "**The User** ( {} ) **Was Banned In This Chat!**",
    "errorban": "**The User** ( {} ) **Is Not Banned!**\n**Error:** ( `{}` )",
    "tbanuser": "**The User** ( {} ) **Was Banned For** ( `{}Minutes` ) **In This Chat!**",
    "unbanuser": "**The User** ( {} ) **Was UnBanned In This Chat!**",
    "errorunabn": "**The User** ( {} ) **Is Not UnBanned!**\n**Error:** ( `{}` )",
}

@client.Command(command="Ban ?(.*)?")
async def banuser(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
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
    
@client.Command(command="TBan (\d*)")
async def timerbanuser(event):
    await event.edit(client.STRINGS["wait"])
    timer = int(event.pattern_match.group(1))
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["user"]["reply"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(STRINGS["notacs"])
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, timedelta(minutes=timer), view_messages=False)
    except Exception as error:
        return await event.edit(STRINGS["errorban"].format(mention, error))
    text = STRINGS["tbanuser"].format(mention, timer)
    await event.edit(text)
    
@client.Command(command="UnBan ?(.*)?")
async def unbanuser(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
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