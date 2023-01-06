from FidoSelf import client
from telethon import functions

@client.Cmd(pattern=f"(?i)^\{client.cmd}Gid$")
async def Getid(event):
    await event.edit(client.get_string("Wait"))
    if event.is_private:
        text = f"**{client.str} YourID:** ( `{client.me.id}` )\n**{client.str} UserID:** ( `{event.chat_id}` )\n"    
        await event.edit(text) 
    else:
        text = f"**{client.str} YourID:** ( `{client.me.id}` )\n**{client.str} ChatID:** ( `{event.chat_id}` )\n"
        if event.reply_message:
            text += f"**{client.str} Reply UserID:** ( `{event.reply_message.sender_id}` )"
        await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}Uinfo ?(.*)?$")
async def uinfo(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    uinfo = await client.get_entity(event.userid)
    info = await client(functions.users.GetFullUserRequest(event.userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = client.get_string("GetInfo_1").format(uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await event.respond(userinfo, file=info.profile_photo)
    else:
        await event.respond(userinfo)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}Cinfo ?(.*)?$")
async def ginfo(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.chatid:
        return await event.edit(client.get_string("Reply_U"))
    cinfo = await client.get_entity(event.chatid)
    try:
        info = (await client(functions.channels.GetFullChannelRequest(event.chatid))).full_chat
    except:
        info = (await client(functions.messages.GetFullChatRequest(event.chatid))).full_chat
    history = await client(functions.messages.GetHistoryRequest(peer=event.chatid, offset_id=0, offset_date=None, add_offset=-0, limit=0, max_id=0, min_id=0, hash=0))
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
