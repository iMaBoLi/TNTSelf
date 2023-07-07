from FidoSelf import client
from datetime import timedelta

__INFO__ = {
    "Category": "Groups",
    "Name": "Mute",
    "Info": {
        "Help": "To Mute/UnMute Users In Chats!",
        "Commands": {
            "{CMD}Mute": {
                "Help": "To Mute User",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}UnMute": {
                "Help": "To UnMute User",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}TMute <Time>": {
                "Help": "To Mute User For Minutes",
                "Getid": "You Must Reply To User",
                "Input": {
                    "<Time>": "Time For Mute (Minutes)",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notacs": "**✶ You Do Not Have Access To Mute/UnMute Users!**",
    "muteuser": "**The User** ( {} ) **Was Muted In This Chat!**",
    "errormute": "**The User** ( {} ) **Is Not Muted!**\n**Error:** ( `{}` )",
    "tmuteuser": "**The User** ( {} ) **Was Muted For** ( `{}Minutes` ) **In This Chat!**",
    "unmuteuser": "**The User** ( {} ) **Was UnMuted In This Chat!**",
    "errorunabn": "**The User** ( {} ) **Is Not UnMuted!**\n**Error:** ( `{}` )",
}

@client.Command(command="Mute ?(.*)?")
async def muteuser(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(STRINGS["notacs"])
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, send_messages=False)
    except Exception as error:
        return await event.edit(STRINGS["errormute"].format(mention, error))
    text = STRINGS["muteuser"].format(mention)
    await event.edit(text)

@client.Command(command="TMute (\d*)")
async def timermuteuser(event):
    await event.edit(client.STRINGS["wait"])
    timer = int(event.pattern_match.group(1))
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["user"]["reply"])
    if not event.checkAdmin(ban_users=True):
        return await event.edit(STRINGS["notacs"])
    userid = event.reply_message.sender_id
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    try:
        await client.edit_permissions(event.chat_id, info.id, timedelta(minutes=timer), send_messages=False)
    except Exception as error:
        return await event.edit(STRINGS["errormute"].format(mention, error))
    text = STRINGS["tmuteuser"].format(mention, timer)
    await event.edit(text)
    
@client.Command(command="UnMute ?(.*)?")
async def unmuteuser(event):
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
        await client.edit_permissions(event.chat_id, info.id)
    except Exception as error:
        return await event.edit(STRINGS["errorunmute"].format(mention, error))
    text = STRINGS["unmuteuser"].format(mention)
    await event.edit(text)