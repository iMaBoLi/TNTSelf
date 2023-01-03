from FidoSelf import client
from telethon import Button

def get_manage_buttons(userid):
    buttons = []
    MANAGES = client.get_string("Manages")
    for manage in MANAGES:
        lists = client.DB.get_key(manage) or []
        smode = "( ✔️ )" if userid in lists else "( ✖️ )"
        cmode = "del" if userid in lists else "add"       
        buttons.append([Button.inline(f"• {MODES[mode]} - {smode} •", data=f"setuser:{userid}:{manage}:{cmode}")])
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
    userid = str(event.pattern_match.group(1))
    text = client.get_string("Manage_1")
    buttons = get_manage_buttons(userid)
    await event.answer([event.builder.article(f"{client.str} Smart Self - Manage", text=text, buttons=buttons)])

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
    buttons = get_mode_buttons(page)
    await event.edit(buttons=buttons)

@client.Callback(data="closemanage")
async def closemanagepanel(event):
    text = client.get_string("Manage_2")
    await event.edit(text=text)
