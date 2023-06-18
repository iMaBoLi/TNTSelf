from FidoSelf import client
from telethon import Button, events

STRINGS = {
    "notall": "**The User** ( {} ) **Already In Help List!**",
    "add": "**The User** ( {} ) **Is Added To Help List!**",
    "notin": "**The User** ( {} ) **Is Not In Help List!**",
    "del": "**The User** ( {} ) **Deleted From Help List!**",
    "main": "**» Dear** ( {} )\n  **✾ Welcome To Fido Self Help!**\n  **✾ Please Select The Category You Want:**",
    "category": "**» Dear** ( {} )\n  **✾ Welcome To** ( `{}` ) **Category Help!**\n  **✾ Please Choose Plugin To Get Info:**",
    "closehelp": "**The Help Panel Successfully Closed!**",
}

CATS = {
    "Setting": "⚙️ Settings ({})",
    "Manage": "👮 Manage ({})",
    "Tools": "🔧 Tools ({})",
    "Practical": "🧪 Practical ({})",
    "Account": "💎 Account ({})",
    "Group": "👥 Groups ({})",
    "Private": "🔒 Private ({})",
    "Funs": "🎨 Funs ({})",
}

@client.Command(command="AddHelp ?(.*)?")
async def addhelp(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    helps = client.DB.get_key("HELP_USERS") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
    if userid in helps:
        return await event.edit(STRINGS["notall"].format(mention))
    helps.append(userid)
    client.DB.set_key("HELP_USERS", helps)
    await event.edit(STRINGS["add"].format(mention))
    
@client.Command(command="DelHelp ?(.*)?")
async def delhelp(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    helps = client.DB.get_key("HELP_USERS") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
    if userid not in helps:
        return await event.edit(STRINGS["notin"].format(mention))  
    helps.remove(userid)
    client.DB.set_key("HELP_USERS", helps)
    await event.edit(STRINGS["del"].format(mention))

@client.on(events.InlineQuery(pattern="help"))
async def inlinehelp(event):
    USERS = client.DB.get_key("HELP_USERS") or []
    if event.sender_id not in USERS: return
    info = await client.get_entity(event.sender_id)
    text = STRINGS["main"].format(client.mention(info))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        ShowName = CATS[category].format(plugcount)
        buttons.append(Button.inline(ShowName, data=f"OTHERSGetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="OTHERSCloseHelp")])
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.on(events.CallbackQuery(data="OTHERSHelp")
async def callhelp(event):
    USERS = client.DB.get_key("HELP_USERS") or []
    if event.sender_id not in USERS: return
    info = await client.get_entity(event.sender_id)
    text = STRINGS["main"].format(client.mention(info))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        ShowName = CATS[category].format(plugcount)
        buttons.append(Button.inline(ShowName, data=f"OTHERSGetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="OTHERSCloseHelp")])
    await event.edit(text=text, buttons=buttons)

@client.on(events.CallbackQuery(data="OTHERSGetCategory\:(.*)")
async def getcategory(event):
    USERS = client.DB.get_key("HELP_USERS") or []
    if event.sender_id not in USERS: return
    category = str(event.data_match.group(1).decode('utf-8'))
    buttons = []
    for plugin in client.HELP[category]:
        buttons.append(Button.inline(f"• {plugin} •", data=f"OTHERSGetHelp:{plugin}:{category}"))
    buttons = client.functions.chunker(buttons, sizes=[3,2])
    buttons.append([Button.inline(client.STRINGS["inline"]["Back"], data="OTHERSHelp"), Button.inline(client.STRINGS["inline"]["Close"], data="OTHERSCloseHelp")])
    text = STRINGS["category"].format(client.mention(client.me), category)
    await event.edit(text=text, buttons=buttons)

@client.on(events.CallbackQuery(data="OTHERSGetHelp\:(.*)\:(.*)")
async def getplugin(event):
    USERS = client.DB.get_key("HELP_USERS") or []
    if event.sender_id not in USERS: return
    plugin = event.data_match.group(1).decode('utf-8')
    category = event.data_match.group(2).decode('utf-8')
    info = client.HELP[category][plugin]
    text = "**꥟ " + info["Help"] + "**\n"
    text += "⊰ ┈───╌ ❊ ╌───┈ ⊱" + "\n\n"
    for command in info["Commands"]:
        ComName = command.format(CMD=".")
        share = f"http://t.me/share/text?text={ComName.split(' ')[0]}"
        text += f"[🔗]({share})" + ": " + f"`{ComName}`" + "\n"
        if info["Commands"][command]:
            text += "    **› " + info["Commands"][command] + "**\n"
        text += "\n" + "─────── ⋆ ───────" + "\n\n"
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"OTHERSGetCategory:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data="OTHERSCloseHelp")]]
    await event.edit(text=text, buttons=buttons) 

@client.on(events.CallbackQuery(data="OTHERSCloseHelp")
async def closehelp(event):
    USERS = client.DB.get_key("HELP_USERS") or []
    if event.sender_id not in USERS: return
    text = STRINGS["closehelp"]
    await event.edit(text=text)