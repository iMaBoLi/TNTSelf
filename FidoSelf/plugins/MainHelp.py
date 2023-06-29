from FidoSelf import client
from telethon import Button

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Help",
    "Pluginfo": {
        "Help": "To Get Help About Self Commands!",
        "Commands": {
            "{CMD}Help": None,
            "{CMD}Help <Name>": "To Get Help Of Plugin!",
        },
    },
}

client.functions.AddInfo(__INFO__)

STRINGS = {
    "notfound": "**✾ The Plugin With Name** ( `{}` ) **Is Not Available!**",
    "main": "**» Dear** ( {} )\n   **✾ Welcome To Fido Self Help!**\n      **✾ Please Select The Category You Want:**",
    "category": "**» Dear** ( {} )\n   **✾ Welcome To** ( `{}` ) **Category Help!**\n      **✾ Please Choose Plugin To Get Info:**",
    "closehelp": "**☻ The Help Panel Successfully Closed!**",
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

def gethelp(category, plugin):
    info = client.HELP[category][plugin]
    text = "**꥟ " + info["Help"] + "**\n\n"
    for command in info["Commands"]:
        cname = command.replace("{CMD}", ".")
        share = f"http://t.me/share/text?text={cname.split(' ')[0]}"
        text += f"\n[𒆜]({share})" + " : " + f"`{cname}`" + "\n"
        if info["Commands"][command]:
            text += "  **› " + info["Commands"][command] + "**\n"
    return text

def search_plugin(pluginname):
    pluginname = pluginname.replace(" ", "").lower()
    for category in CATS:
        for plugin in client.HELP[category]:
            plname = plugin.replace(" ", "").lower()
            if pluginname == plname:
                return category, plugin
    return None, None

@client.Command(command="Help ?(.*)?")
async def help(event):
    await event.edit(client.STRINGS["wait"])
    pname = event.pattern_match.group(1)
    if pname:
        category, plugin = search_plugin(pname)
        if not (category or plugin):
            return await event.edit(STRINGS["notfound"].format(pname))
        text = gethelp(category, plugin)
        return await event.edit(text)
    else:
        res = await client.inline_query(client.bot.me.username, "Help")
        await res[0].click(event.chat_id)
        await event.delete()

@client.Inline(pattern="Help")
async def inlinehelp(event):
    text = STRINGS["main"].format(client.functions.mention(client.me))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        sname = CATS[category].format(plugcount)
        buttons.append(Button.inline(sname, data=f"GetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="Help")
async def callhelp(event):
    text = STRINGS["main"].format(client.functions.mention(client.me))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        sname = CATS[category].format(plugcount)
        buttons.append(Button.inline(sname, data=f"GetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetCategory\:(.*)")
async def getcategory(event):
    category = str(event.data_match.group(1).decode('utf-8'))
    buttons = []
    for plugin in client.HELP[category]:
        buttons.append(Button.inline(f"• {plugin} •", data=f"GetHelp:{plugin}:{category}"))
    buttons = client.functions.chunker(buttons, [3,2])
    buttons.append([Button.inline(client.STRINGS["inline"]["Back"], data="Help"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    text = STRINGS["category"].format(client.functions.mention(client.me), category)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetHelp\:(.*)\:(.*)")
async def getplugin(event):
    plugin = event.data_match.group(1).decode('utf-8')
    category = event.data_match.group(2).decode('utf-8')
    text = gethelp(category, plugin)
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"GetCategory:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")]]
    await event.edit(text=text, buttons=buttons) 

@client.Callback(data="CloseHelp")
async def closehelp(event):
    text = STRINGS["closehelp"]
    await event.edit(text=text)