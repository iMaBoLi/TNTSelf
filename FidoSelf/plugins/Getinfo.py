from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Practical",
    "Plugname": "User Info",
    "Pluginfo": {
        "Help": "To Get Information Of Users!",
        "Commands": {
            "{CMD}UInfo <Pv|Reply|UserId|Username>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Practical",
    "Plugname": "Chat Info",
    "Pluginfo": {
        "Help": "To Get Information Of Chats!",
        "Commands": {
            "{CMD}CInfo <Chat|ChatId>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "user": "**User Info:**\n\n**Mention:** ( {} )\n**ID:** ( `{}` )\n**First Name:** ( `{}` )\n**Last Name:** ( `{}` )\n**Username :** ( `{}` )\n**Contact:** ( `{}` )\n**Mutual Contact:** ( `{}` )\n**Status:** ( `{}` )\n**Common Chats:** ( `{}` )\n**Bio:** ( `{}` )",
    "chat": "**Chat Info:**\n\n**ID:** ( `{}` )\n**Title:** ( `{}` )\n**Username :** ( `{}` )\n\n**Messages Count:** ( `{}` )\n\n**Members Count:** ( `{}` )\n**Administrators Count:** ( `{}` )\n**Bots Count:** ( `{}` )\n**Onlines Count:** ( `{}` )\n**Banned Count:** ( `{}` )\n**Kicked Count:** ( `{}` )\n**Description:** ( `{}` )",
}

@client.Command(command="UInfo ?(.*)?")
async def userinfo(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    uinfo = await client.get_entity(userid)
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = STRINGS["user"].format(client.mention(uinfo), uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await event.respond(userinfo, file=info.profile_photo)
    else:
        await event.respond(userinfo)
    await event.delete()

@client.Command(command="Cinfo ?(.*)?")
async def ginfo(event):
    await event.edit(client.STRINGS["wait"])
    chatid = await event.chatid(event.pattern_match.group(1))
    if not chatid:
        return await event.edit(client.STRINGS["getchatID"])
    cinfo = await client.get_entity(chatid)
    if cinfo.megagroup or cinfo.broadcast:
        info = (await client(functions.channels.GetFullChannelRequest(chatid))).full_chat
    else:
        info = (await client(functions.messages.GetFullChatRequest(chatid))).full_chat
    history = await client(functions.messages.GetHistoryRequest(peer=chatid, offset_id=0, offset_date=None, add_offset=-0, limit=0, max_id=0, min_id=0, hash=0))
    members = getattr(info, "participants_count", None) or "---"
    bans = getattr(info, "banned_count", None) or "---"
    admins = getattr(info, "admins_count", None) or "---"
    kicks = getattr(info, "kicked_count", None) or "---"
    onlines = getattr(info, "online_count", None) or "---"
    username = f"@{cinfo.username}" if cinfo.username else "---"
    chatinfo = STRINGS["chat"].format(cinfo.id, cinfo.title, username, history.count, members, admins, len(info.bot_info), onlines, bans, kicks, (info.about or "---"))
    if str(cinfo.photo) == "ChatPhotoEmpty()":
        await event.respond(chatinfo)
    else:
        await event.respond(chatinfo, file=info.chat_photo)
    await event.delete()