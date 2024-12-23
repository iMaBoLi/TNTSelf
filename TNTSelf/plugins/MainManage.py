from TNTSelf import client
from telethon import functions, Button
import asyncio

__INFO__ = {
    "Category": "Setting",
    "Name": "Manage",
    "Info": {
        "Help": "To Get Manage Panel For Users!",
        "Commands": {
            "{CMD}Manage": {
                "Help": "To Get Manage Panel",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "menu": "**{STR} Select The Options Below To Manage User Modes:**\n\n**{STR} User:** ( {} )",
    "closemanage": "**{STR} The Manage Panel Successfuly Closed!**",
    "infouser": "**{STR} User Info:**\n\n**{STR} Mention:** ( {} )\n**{STR} ID:** ( `{}` )\n**{STR} First Name:** ( `{}` )\n**{STR} Last Name:** ( `{}` )\n**{STR} Username :** ( `{}` )\n**{STR} Contact:** ( `{}` )\n**{STR} Mutual Contact:** ( `{}` )\n**{STR} Status:** ( `{}` )\n**{STR} Common Chats:** ( `{}` )\n**{STR} Bio:** ( `{}` )",
}

MANAGES = {
    "WHITE_LIST": "White",
    "BLACK_LIST": "Black",
    "LOVE_USERS": "Love",
    "ECHO_USERS": "Echo",
    "MUTEPV_USERS": "MutePv",
}

async def get_manage_buttons(userid, chatid):
    buttons = []
    buttons.append([Button.inline(f"• User Info •", data=f"GetUserInfo:{chatid}:{userid}")])
    buttons.append([Button.inline("• Spector •", data=f"Spector:{chatid}:{userid}")])
    obuts = []
    for manage in MANAGES:
        lists = event.client.DB.get_key(manage) or []
        smode = client.STRINGS["inline"]["On"] if userid in lists else client.STRINGS["inline"]["Off"]
        cmode = "del" if userid in lists else "add"
        obuts.append(Button.inline(f"{MANAGES[manage]} {smode}", data=f"SetUser:{chatid}:{userid}:{manage}:{cmode}"))
    obuts = list(client.functions.chunks(obuts, 2))
    for but in obuts:
        buttons.append(but)
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseManage")])
    return buttons

@client.Command(command="Manage", userid=True)
async def Manage(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    chatid = event.chat_id
    res = await event.client.inline_query(event.client.bot.me.username, f"Manage:{chatid}:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Manage\\:(.*)\\:(.*)")
async def inlinemanage(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    info = await event.client.get_entity(userid)
    mention = client.functions.mention(info)
    text = client.getstrings(STRINGS)["menu"].format(mention)
    buttons = await get_manage_buttons(userid, chatid)
    await event.answer([event.builder.article("TNTSelf - Manage", text=text, buttons=buttons)])

@client.Callback(data="SetUser\\:(.*)\\:(.*)\\:(.*)\\:(.*)")
async def SetUsermanage(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    mode = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    info = await event.client.get_entity(userid)
    lists = event.client.DB.get_key(mode) or []
    if change == "add":
        lists.append(userid)
        event.client.DB.set_key(mode, lists)
    elif change == "del":
        lists.remove(userid)
        event.client.DB.set_key(mode, lists)
    buttons = await get_manage_buttons(userid, chatid)
    await event.edit(buttons=buttons)

@client.Callback(data="GetUserInfo\\:(.*)\\:(.*)")
async def getuserinfo(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    uinfo = await event.client.get_entity(userid)
    info = await event.client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = client.getstrings(STRINGS)["infouser"].format(client.functions.mention(uinfo), uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await event.client.send_file(chatid, info.profile_photo, caption=userinfo)
    else:
        await event.client.send_message(chatid, userinfo)
    buttons = await get_manage_buttons(userid, chatid)    
    await event.edit(buttons=buttons)

@client.Callback(data="CloseManage")
async def closemanage(event):
    text = client.getstrings(STRINGS)["closemanage"]
    await event.edit(text=text)