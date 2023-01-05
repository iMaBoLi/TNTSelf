from FidoSelf import client
from telethon import functions, Button
import asyncio

async def get_manage_buttons(userid):
    buttons = []
    info = await client(functions.users.GetFullUserRequest(userid))
    info = info.full_user
    smode = client.get_string("Manages_UNBLOCK") if info.blocked else client.get_string("Manages_BLOCK")
    cmode = "unblock" if info.blocked else "block"
    buttons.append([Button.inline(f"• {smode} •", data=f"{cmode}:{userid}")])
    MANAGES = client.get_string("Manages")
    obuts = []
    for manage in ["BLACKS", "ECHOS"]:
        lists = client.DB.get_key(manage) or []
        smode = "( ✔️ )" if userid in lists else "( ✖️ )"
        cmode = "del" if userid in lists else "add"
        obuts.append(Button.inline(f"• {MANAGES[manage]} - {smode} •", data=f"setuser:{userid}:{manage}:{cmode}"))
    buttons.append(obuts)
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
    await asyncio.sleep(0.5)
    buttons = await get_manage_buttons(userid)    
    await event.edit(buttons=buttons)

@client.Callback(data="closemanage")
async def closemanagepanel(event):
    text = client.get_string("Manage_2")
    await event.edit(text=text)
