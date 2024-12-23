from TNTSelf import client
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
                "Help": "To Ban User For Seconds",
                "Getid": "You Must Reply To User",
                "Input": {
                    "<Time>": "Time For Ban (Seconds)",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notacs": "**{STR} You Do Not Have Access To Ban/UnBan Users!**",
    "banuser": "**{STR} The User** ( {} ) **Was Banned In This Chat!**",
    "errorban": "**{STR} The User** ( {} ) **Is Not Banned!**\n**Error:** ( `{}` )",
    "tbanuser": "**{STR} The User** ( {} ) **Was Banned For** ( `{}` ) **In This Chat!**",
    "unbanuser": "**{STR} The User** ( {} ) **Was UnBanned In This Chat!**",
    "errorunabn": "**{STR} The User** ( {} ) **Is Not UnBanned!**\n**Error:** ( `{}` )"
}

@client.Command(command="Ban", userid=True)
async def banuser(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(client.getstrings(STRINGS)["notacs"])
    info = await event.client.get_entity(event.userid)
    mention = client.functions.mention(info)
    try:
        await event.client.edit_permissions(event.chat_id, info.id, view_messages=False)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errorban"].format(mention, error))
    text = client.getstrings(STRINGS)["banuser"].format(mention)
    await event.edit(text)
    
@client.Command(command="TBan (\\d*)")
async def timerbanuser(event):
    await event.edit(client.STRINGS["wait"])
    timer = int(event.pattern_match.group(1))
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["user"]["reply"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(client.getstrings(STRINGS)["notacs"])
    userid = event.reply_message.sender_id
    info = await event.client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await event.client.edit_permissions(event.chat_id, info.id, timedelta(seconds=timer), view_messages=False)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errorban"].format(mention, error))
    stimer = client.functions.convert_time(timer)
    text = client.getstrings(STRINGS)["tbanuser"].format(mention, stimer)
    await event.edit(text)
    
@client.Command(command="UnBan", userid=True)
async def unbanuser(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(client.getstrings(STRINGS)["notacs"])
    info = await event.client.get_entity(event.userid)
    mention = client.functions.mention(info)
    try:
        await event.client.edit_permissions(event.chat_id, info.id)
    except Exception as error:
        return await event.edit(client.getstrings(STRINGS)["errorunban"].format(mention, error))
    text = client.getstrings(STRINGS)["unbanuser"].format(mention)
    await event.edit(text)