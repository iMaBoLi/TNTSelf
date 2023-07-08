from FidoSelf import client
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
    "menu": "**Please Use The Options Below To Manage User Modes:**",
    "closemanage": "**The Manage Panel Successfuly Closed!**",
    "infouser": "**User Info:**\n\n**Mention:** ( {} )\n**ID:** ( `{}` )\n**First Name:** ( `{}` )\n**Last Name:** ( `{}` )\n**Username :** ( `{}` )\n**Contact:** ( `{}` )\n**Mutual Contact:** ( `{}` )\n**Status:** ( `{}` )\n**Common Chats:** ( `{}` )\n**Bio:** ( `{}` )",
}

MANAGES = {
    "VIP_USERS": "Vip"
    "LOVE_USERS": "Love",
    "WHITE_LIST": "White",
    "BLACK_LIST": "Black",
    "ECHO_USERS": "Echo",
    "MUTEPV_USERS": "Mute Pv",
}

async def get_manage_buttons(userid, chatid):
    buttons = []
    buttons.append([Button.inline(f"• User Info •", data=f"GetUserInfo:{chatid}:{userid}")])
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    smode = "UnBlock" if info.blocked else "Block"
    buttons.append([Button.inline(f"• {smode} •", data=f"User:{smode}:{chatid}:{userid}")])
    obuts = []
    for manage in MANAGES:
        lists = client.DB.get_key(manage) or []
        smode = client.STRINGS["inline"]["On"] if userid in lists else client.STRINGS["inline"]["Off"]
        cmode = "del" if userid in lists else "add"
        obuts.append(Button.inline(f"{MANAGES[manage]} {smode}", data=f"SetUser:{chatid}:{userid}:{manage}:{cmode}"))
    obuts = list(client.functions.chunks(obuts, 2))
    for but in obuts:
        buttons.append(but)
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseManage")])
    return buttons

@client.Command(command="Manage ?(.*)?")
async def Manage(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"Manage:{chatid}:{userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Manage\:(.*)\:(.*)")
async def inlinemanage(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = STRINGS["menu"]
    buttons = await get_manage_buttons(userid, chatid)
    await event.answer([event.builder.article("FidoSelf - Manage", text=text, buttons=buttons)])

@client.Callback(data="SetUser\:(.*)\:(.*)\:(.*)\:(.*)")
async def SetUsermanage(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    mode = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    info = await client.get_entity(userid)
    lists = client.DB.get_key(mode) or []
    if change == "add":
        lists.append(userid)
        client.DB.set_key(mode, lists)
    elif change == "del":
        lists.remove(userid)
        client.DB.set_key(mode, lists)
    buttons = await get_manage_buttons(userid, chatid)
    await event.edit(buttons=buttons)

@client.Callback(data="User\:(Block|UnBlock)\:(.*)\:(.*)")
async def blockunblock(event):
    change = str(event.data_match.group(1).decode('utf-8'))
    chatid = int(event.data_match.group(2).decode('utf-8'))
    userid = int(event.data_match.group(3).decode('utf-8'))
    if change == "Block":
        await client(functions.contacts.BlockRequest(userid))
    elif change == "UnBlock":
        await client(functions.contacts.UnblockRequest(userid))
    await asyncio.sleep(0.3)
    buttons = await get_manage_buttons(userid, chatid)    
    await event.edit(buttons=buttons)

@client.Callback(data="GetUserInfo\:(.*)\:(.*)")
async def getuserinfo(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    uinfo = await client.get_entity(userid)
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = STRINGS["infouser"].format(client.functions.mention(uinfo), uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await client.send_file(chatid, info.profile_photo, caption=userinfo)
    else:
        await client.send_message(chatid, userinfo)
    buttons = await get_manage_buttons(userid, chatid)    
    await event.edit(buttons=buttons)

@client.Callback(data="CloseManage")
async def closemanage(event):
    text = STRINGS["closemanage"]
    await event.edit(text=text)