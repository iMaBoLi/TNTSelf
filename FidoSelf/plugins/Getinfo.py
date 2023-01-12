from FidoSelf import client
from telethon import functions

@client.Cmd(pattern=f"(?i)^\{client.cmd}Uinfo ?(.*)?$")
async def uinfo(event):
    await event.edit(client.get_string("Wait"))
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.get_string("Reply_UUP"))
    uinfo = await client.get_entity(userid)
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = client.get_string("GetInfo_1").format(client.mention(uinfo), uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await event.respond(userinfo, file=info.profile_photo)
    else:
        await event.respond(userinfo)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}(G|C)info ?(.*)?$")
async def ginfo(event):
    await event.edit(client.get_string("Wait"))
    chatid = await event.chatid(event.pattern_match.group(2))
    if not chatid:
        return await event.edit(client.get_string("Reply_UUP"))
    cinfo = await client.get_entity(chatid)
    try:
        info = (await client(functions.channels.GetFullChannelRequest(chatid))).full_chat
    except:
        info = (await client(functions.messages.GetFullChatRequest(chatid))).full_chat
    history = await client(functions.messages.GetHistoryRequest(peer=chatid, offset_id=0, offset_date=None, add_offset=-0, limit=0, max_id=0, min_id=0, hash=0))
    members = getattr(info, "participants_count", None) or "---"
    bans = getattr(info, "banned_count", None) or "---"
    admins = getattr(info, "admins_count", None) or "---"
    kicks = getattr(info, "kicked_count", None) or "---"
    onlines = getattr(info, "online_count", None) or "---"
    username = f"@{cinfo.username}" if cinfo.username else "---"
    chatinfo = client.get_string("GetInfo_2").format(cinfo.id, cinfo.title, username, history.count, members, admins, len(info.bot_info), onlines, bans, kicks, (info.about or "---"))
    if str(cinfo.photo) == "ChatPhotoEmpty()":
        await event.respond(chatinfo)
    else:
        await event.respond(chatinfo, file=info.chat_photo)
    await event.delete()
