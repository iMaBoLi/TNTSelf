from FidoSelf import client
from telethon import functions

@client.Cmd(pattern=f"(?i)^\{client.cmd}id$")
async def id(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if event.is_private:
        text = f"**{client.str} Your ID:** ( `{client.me.id}` )\n**{client.str} User ID:** ( `{event.chat_id}` )\n**{client.str} Message ID:** ( `{event.id}` )\n"    
        await event.edit(text) 
    else:
        text = f"**{client.str} Your ID:** ( `{client.me.id}` )\n**{client.str} Chat ID:** ( `{event.chat_id}` )\n**{client.str} Message ID:** ( `{event.id}` )\n"
        if event.reply_message:
            text += f"**{client.str} User ID:** ( `{event.reply_message.sender_id}` )"
        await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}Cinfo ?(.*)?$")
async def ginfo(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_group and not event.is_ch:
        return await event.edit(f"**{client.str} Please Enter Chatid Or Chat Username Or Send In Groups Or Channels!**")
    cinfo = await client.get_entity(event.chatid)
    if not cinfo.to_dict()["_"] == "Channel" and not cinfo.to_dict()["_"] == "Group":
        return await event.edit(f"**{client.str} Please Enter Chatid Or Chat Username Or Send In Groups Or Channels!**")
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
    chatinfo = f"""
**{client.str} Chat Info:**
    
**{client.str} ID:** ( `{cinfo.id}` )
**{client.str} Title:** ( `{cinfo.title}` )
**{client.str} Username :** ( `{username}` )

**{client.str} Messages Count:** ( `{history.count}` )

**{client.str} Members Count:** ( `{members}` )
**{client.str} Administrators Count:** ( `{admins}` )
**{client.str} Bots Count:** ( `{len(info.bot_info)}` )
**{client.str} Onlines Count:** ( `{onlines}` )
**{client.str} Banned Count:** ( `{bans}` )
**{client.str} Kicked Count:** ( `{kicks}` )

**{client.str} Description:** ( `{info.about[:2000] or "---"}` )
"""
    if str(cinfo.photo) == "ChatPhotoEmpty()":
        await event.respond(chatinfo)
    else:
        await event.respond(chatinfo, file=info.chat_photo)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}Uinfo ?(.*)?$")
async def uinfo(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_private and not event.userid:
        return await event.edit(f"**{client.str} Please Enter Userid Or Username Or Send In Private Chats!**")
    if not event.userid:
        event.userid = event.chat_id
    uinfo = await client.get_entity(event.userid)
    if not uinfo.to_dict()["_"] == "User":
        return await event.edit(f"**{client.str} Please Enter Userid Or Username Or Send In Private Chats!**")
    info = (await client(functions.users.GetFullUserRequest(event.userid))).full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    isbot = "✅" if uinfo.bot else "❌"
    verified = "✅" if uinfo.verified else "❌"
    pcalls = "✅" if info.phone_calls_available else "❌"
    vcalls = "✅" if info.video_calls_available else "❌"
    if uinfo.status: 
        status = uinfo.status.to_dict()["_"].replace("UserStatus", "")
    else:
        status = "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = f"""
**{client.str} User Info:**
    
**{client.str} ID:** ( `{uinfo.id}` )
**{client.str} First Name:** ( `{uinfo.first_name}` )
**{client.str} Last Name:** ( `{uinfo.last_name or "---"}` )
**{client.str} Username :** ( `{username}` )
**{client.str} Is Bot:** ( `{isbot}` )
**{client.str} Contact:** ( `{contact}` )
**{client.str} Mutual Contact:** ( `{mcontact}` )
**{client.str} Verified:** ( `{verified}` )
**{client.str} PhoneCalls Available:** ( `{pcalls}` )
**{client.str} VideoCalls Available:** ( `{vcalls}` )
**{client.str} Status:** ( `{status}` )
**{client.str} Common Chats:** ( `{info.common_chats_count}` )

**{client.str} Bio:** ( `{info.about or "---"}` )
"""
    if info.profile_photo:
        await event.respond(userinfo, file=info.profile_photo)
    else:
        await event.respond(userinfo)
    await event.delete()
