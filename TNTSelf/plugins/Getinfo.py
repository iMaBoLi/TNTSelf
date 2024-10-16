from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Users",
    "Name": "User Info",
    "Info": {
        "Help": "To Get Information Of Users!",
        "Commands": {
            "{CMD}Info": {
                "Help": "To Get User Info",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Groups",
    "Name": "Chat Info",
    "Info": {
        "Help": "To Get Information Of Chats!",
        "Commands": {
            "{CMD}GInfo": {
                "Help": "To Get Chat Info",
                "Getid": "You Must Send In Chat Or Input ChatID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "EN": {
        "user": "**{STR} User Info:**\n\n**{STR} Mention:** ( {} )\n**{STR} ID:** ( `{}` )\n**{STR} First Name:** ( `{}` )\n**{STR} Last Name:** ( `{}` )\n**{STR} Username :** ( `{}` )\n**{STR} Contact:** ( `{}` )\n**{STR} Mutual Contact:** ( `{}` )\n**{STR} Status:** ( `{}` )\n**{STR} Common Chats:** ( `{}` )\n**{STR} Bio:** ( `{}` )",
        "chat": "**{STR} Chat Info:**\n\n**{STR} ID:** ( `{}` )\n**{STR} Title:** ( `{}` )\n**{STR} Username :** ( `{}` )\n\n**{STR} Messages Count:** ( `{}` )\n\n**{STR} Members Count:** ( `{}` )\n**{STR} Administrators Count:** ( `{}` )\n**{STR} Bots Count:** ( `{}` )\n**{STR} Onlines Count:** ( `{}` )\n**{STR} Banned Count:** ( `{}` )\n**{STR} Kicked Count:** ( `{}` )\n**{STR} Description:** ( `{}` )",
    },
    "FA": {
        "user": "**{STR} اطلاعات کاربر:**\n\n**{STR} تگ:** ( {} )\n**{STR} آیدی:** ( `{}` )\n**{STR} اسم:** ( `{}` )\n**{STR} فامیل:** ( `{}` )\n**{STR} یوزرنیم:** ( `{}` )\n**{STR} مخاطب:** ( `{}` )\n**{STR} مخاطب دوطرفه:** ( `{}` )\n**{STR} وضعیت:** ( `{}` )\n**{STR} چت های مشترک:** ( `{}` )\n**{STR} بیوگرافی:** ( `{}` )",
        "chat": "**{STR} اطلاعات چت:**\n\n**{STR} آیدی:** ( `{}` )\n**{STR} نام:** ( `{}` )\n**{STR} یوزرنیم :** ( `{}` )\n\n**{STR} تعداد پیام ها:** ( `{}` )\n\n**{STR} تعداد کاربران:** ( `{}` )\n**{STR} تعداد ادمین ها:** ( `{}` )\n**{STR} تعداد ربات ها:** ( `{}` )\n**{STR} تعداد کاربران آنلاین:** ( `{}` )\n**{STR} تعداد کاربران مسدود:** ( `{}` )\n**{STR} تعداد کاربران اخراجی:** ( `{}` )\n**{STR} توضیحات:** ( `{}` )",
    },
}

@client.Command(command="Info", userid=True)
async def userinfo(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    uinfo = await client.get_entity(event.userid)
    info = await client(functions.users.GetFullUserRequest(event.userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = client.getstring(STRINGS, "user").format(client.functions.mention(uinfo), uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await event.respond(userinfo, file=info.profile_photo)
    else:
        await event.respond(userinfo)
    await event.delete()

@client.Command(command="Ginfo", chatid=True)
async def ginfo(event):
    await event.edit(client.STRINGS["wait"])
    if not event.chatid:
        return await event.edit(client.STRINGS["getchatID"])
    cinfo = await client.get_entity(event.chatid)
    if cinfo.megagroup or cinfo.broadcast:
        info = (await client(functions.channels.GetFullChannelRequest(event.chatid))).full_chat
    else:
        info = (await client(functions.messages.GetFullChatRequest(event.chatid))).full_chat
    history = await client(functions.messages.GetHistoryRequest(peer=event.chatid, offset_id=0, offset_date=None, add_offset=-0, limit=0, max_id=0, min_id=0, hash=0))
    members = getattr(info, "participants_count", None) or "---"
    bans = getattr(info, "banned_count", None) or "---"
    admins = getattr(info, "admins_count", None) or "---"
    kicks = getattr(info, "kicked_count", None) or "---"
    onlines = getattr(info, "online_count", None) or "---"
    username = f"@{cinfo.username}" if cinfo.username else "---"
    chatinfo = client.getstring(STRINGS, "chat").format(cinfo.id, cinfo.title, username, history.count, members, admins, len(info.bot_info), onlines, bans, kicks, (info.about or "---"))
    if str(cinfo.photo) == "ChatPhotoEmpty()":
        await event.respond(chatinfo)
    else:
        await event.respond(chatinfo, file=info.chat_photo)
    await event.delete()