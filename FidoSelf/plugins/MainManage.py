from FidoSelf import client
from telethon import functions, Button
import asyncio

async def get_manage_buttons(userid):
    buttons = []
    MANAGES = client.get_string("Manages")
    buttons.append([Button.inline(f'• {MANAGES["INFO"]} •', data=f"getinfo:{userid}")])
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    smode = client.get_string("Manages_UNBLOCK") if info.blocked else client.get_string("Manages_BLOCK")
    cmode = "unblock" if info.blocked else "block"
    buttons.append([Button.inline(f"• {smode} •", data=f"{cmode}:{userid}")])
    obuts = []
    for manage in ["BLACKS", "WHITES", "ECHOS"]:
        lists = client.DB.get_key(manage) or []
        smode = "( ✔️ )" if userid in lists else "( ✖️ )"
        cmode = "del" if userid in lists else "add"
        obuts.append(Button.inline(f"• {MANAGES[manage]} - {smode} •", data=f"setuser:{userid}:{manage}:{cmode}"))
    obuts = list(client.utils.chunks(obuts, 2))
    for but in obuts:
        buttons.append(but)
    buttons.append([Button.inline(client.get_string("Inline_3"), data="closemanage")])
    buttons = client.get_buttons(buttons)
    return buttons

@client.Cmd(pattern=f"(?i)^\{client.cmd}Manage ?(.*)?$")
async def managepanel(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    res = await client.inline_query(client.bot.me.username, f"managepanel:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="managepanel\:(.*)")
async def inlinemanagepanel(event):
    userid = int(event.pattern_match.group(1))
    text = client.get_string("Manage_1")
    buttons = await get_manage_buttons(userid)
    await event.answer([event.builder.article(f"{client.str} FidoSelf - Manage", text=text, buttons=buttons)])

@client.Callback(data="setuser\:(.*)\:(.*)\:(.*)")
async def setusermanage(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    mode = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    info = await client.get_entity(userid)
    lists = client.DB.get_key(mode) or []
    if change == "add":
        lists.append(userid)
        client.DB.set_key(mode, lists)
    elif change == "del":
        lists.remove(userid)
        client.DB.set_key(mode, lists)
    buttons = await get_manage_buttons(userid)
    await event.edit(buttons=buttons)

@client.Callback(data="(block|unblock)\:(.*)")
async def closemanagepanel(event):
    change = str(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    if change == "block":
        await client(functions.contacts.BlockRequest(userid))
    elif change == "unblock":
        await client(functions.contacts.UnblockRequest(userid))
    await asyncio.sleep(0.3)
    buttons = await get_manage_buttons(userid)    
    await event.edit(buttons=buttons)

@client.Callback(data="getinfo\:(.*)")
async def getinfo(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    uinfo = await client.get_entity(userid)
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    contact = "✅" if uinfo.contact else "❌"
    mcontact = "✅" if uinfo.mutual_contact else "❌"
    status = uinfo.status.to_dict()["_"].replace("UserStatus", "") if uinfo.status else "---"
    username = f"@{uinfo.username}" if uinfo.username else "---"
    userinfo = client.get_string("GetInfo_1").format(uinfo.id, uinfo.first_name, (uinfo.last_name or "---"), username, contact, mcontact,status, info.common_chats_count, (info.about or "---"))
    if info.profile_photo:
        await client.send_file(event.chat_id, info.profile_photo, caption=userinfo)
    else:
        await client.send_message(event.chat_id, userinfo)
    buttons = await get_manage_buttons(userid)    
    await event.edit(buttons=buttons)

@client.Callback(data="closemanage")
async def closemanagepanel(event):
    text = client.get_string("Manage_2")
    await event.edit(text=text)
