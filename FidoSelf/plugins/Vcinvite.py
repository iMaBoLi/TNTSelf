from FidoSelf import client
from telethon import functions, types, errors

STRINGS = {
    "notcall": "**The Voice Chat Is Not Founded For This Chat!**",
    "notuser": "**The Users To Invite In To Voice Chat Is Not Founded!**",
    "notflood": "**The Flood Wait Error Is Coming Please Wait And Try Again!**",
    "inviting": "**Inviting** ( `{}` ) **User To Chat Call In This Chat ...**",
    "invited": "**Invite Users To Voice Chat Completed!**",
}

@client.Command(command="InvVc ?(.*)?")
async def ginfo(event):
    await event.edit(client.STRINGS["wait"])
    users = str(event.pattern_match.group(1) or "")
    if event.chat.megagroup or event.chat.broadcast:
        info = (await client(functions.channels.GetFullChannelRequest(event.chat_id))).full_chat
    else:
        info = (await client(functions.messages.GetFullChatRequest(event.chat_id))).full_chat
    if not info.call:
        return await event.edit(STRINGS["notcall"])
    if users:
        usernames = users.replace("@", "").split(",")[:50]
    else:
        usernames = []
        async for user in client.iter_participants(event.chat_id, filter=types.ChannelParticipantsRecent, limit=50):
            usernames.append(user.id)
    if not usernames:
        return await event.edit(STRINGS["notuser"])
    await event.edit(STRINGS["inviting"].format(len(usernames)))
    try:
        result = await client(functions.phone.InviteToGroupCallRequest(call=info.call, users=usernames))
    except errors.FloodWaitError:
        return await event.edit(STRINGS["notflood"])
    except:
        continue
    await event.edit(STRINGS["invited"])