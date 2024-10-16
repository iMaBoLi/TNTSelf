from FidoSelf import client
from telethon import functions, types, errors

__INFO__ = {
    "Category": "Groups",
    "Name": "Invite VC",
    "Info": {
        "Help": "To Invite Users To Voice Chat!",
        "Commands": {
            "{CMD}InviteVc": {
                "Help": "To Invite Users",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notcall": "**{STR} The Voice Chat Is Not Found In This Chat!**",
    "notuser": "**{STR} The Users To Invite In To Voice Chat Is Not Found!**",
    "notflood": "**{STR} The Flood Wait Error Is Coming Please Wait And Try Again ...**",
    "inviting": "**{STR} Inviting** ( `{}` ) **Users To Voice Chat ...**",
    "invited": "**{STR} Invited** ( `{}` ) **Users To Voice Chat Completed!**"
}

@client.Command(command="InviteVc")
async def invitevc(event):
    await event.edit(client.STRINGS["wait"])
    if event.chat.megagroup or event.chat.broadcast:
        info = (await client(functions.channels.GetFullChannelRequest(event.chat_id))).full_chat
    else:
        info = (await client(functions.messages.GetFullChatRequest(event.chat_id))).full_chat
    if not info.call:
        return await event.edit(client.getstrings(STRINGS)["notcall"])
    users = []
    async for user in client.iter_participants(event.chat_id, filter=types.ChannelParticipantsRecent, limit=50):
        users.append(user.id)
    if not users:
        return await event.edit(client.getstrings(STRINGS)["notuser"])
    await event.edit(client.getstrings(STRINGS)["inviting"].format(len(users)))
    invited = 0
    try:
        result = await client(functions.phone.InviteToGroupCallRequest(call=info.call, users=users))
        invited += 1
    except errors.FloodWaitError:
        return await event.edit(client.getstrings(STRINGS)["notflood"])
    except:
        pass
    await event.edit(client.getstrings(STRINGS)["invited"].format(len(invited)))