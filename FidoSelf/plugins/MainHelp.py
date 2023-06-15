from FidoSelf import client
from telethon import Button

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Help",
    "Pluginfo": {
        "Help": "To Get Help About Self Commands!",
        "Commands": {
            "{CMD}Help": None,
        },
    },
}

client.functions.AddInfo(__INFO__)

STRINGS = {
    "main": "**» Dear** ( {} )\n  **✾ Welcome To Fido Self Help!**\n  **✾ Please Select The Category You Want:**",
    "category": "**» Dear** ( {} )\n  **✾ Welcome To** ( `{}` ) **Category Help!**\n  **✾ Please Choose Plugin To Get Info:**",
    "closehelp": "**The Help Panel Successfully Closed!**",
}

CATS = {
    "Setting": "Settings ⚙️",
    "Manage": "Manage 👮",
    "Tools": "Tools 🔧",
    "Practical": "Practical 🧪",
    "Profile": "Profile 💎",
    "Users": "Users ⭐",
    "Group": "Group 👥",
    "Private": "Private 🔒",
}

@client.Command(command="Help")
async def help(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "Help")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Help")
async def inlinehelp(event):
    text = STRINGS["main"].format(client.mention(client.me))
    buttons = []
    for category in CATS:
        buttons.append(Button.inline(f"• {CATS[category]} •", data=f"GetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="Help")
async def callhelp(event):
    text = STRINGS["main"].format(client.mention(client.me))
    buttons = []
    for category in CATS:
        buttons.append(Button.inline(f"• {CATS[category]} •", data=f"GetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetCategory\:(.*)")
async def getcategory(event):
    category = str(event.data_match.group(1).decode('utf-8'))
    buttons = []
    for plugin in client.HELP[category]:
        buttons.append(Button.inline(f"• {plugin} •", data=f"GetHelp:{plugin}:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Back"], data="Help"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    text = STRINGS["category"].format(client.mention(client.me), category)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetHelp\:(.*)\:(.*)")
async def getplugin(event):
    plugin = event.data_match.group(1).decode('utf-8')
    category = event.data_match.group(2).decode('utf-8')
    info = client.HELP[category][plugin]
    text = "**꥟ " + info["Help"] + "**\n"
    text += "⊰ ┈───╌ ❊ ╌───┈ ⊱" + "\n\n"
    addline = False
    for command in info["Commands"]:
        if addline:
            text += "\n" + "─────── ⋆ ───────" + "\n\n"
        addline = True
        ComName = command.format(CMD=".")
        share = f"http://t.me/share/text?text={ComName.split(' ')[0]}"
        text += f"◎ [🔗]({share})" + ": " + f"`{ComName}`" + "\n"
        if info["Commands"][command]:
            text += "    **› " + info["Commands"][command] + "**\n"
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"GetCategory:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")]]
    await event.edit(text=text, buttons=buttons) 

@client.Callback(data="CloseHelp")
async def closehelp(event):
    text = STRINGS["closehelp"]
    await event.edit(text=text)
