from FidoSelf import client
from telethon import Button

STRINGS = {
    "main": "**» Welcome To Fido Self Help!**\n**• Please Select The Category You Want:**",
    "category": "**» Welcome To** ( `{}` ) **Help!**\n**Please Choose Plugin To Get Info:**",
    "closehelp": "**The Help Panel Successfully Closed!**",
}

CATS = {
    "Setting": "Settings ⚙️",
    "Manager": "Manager 👮",
    "Tools": "Tools 🔧",
    "Account": "Account 💎",
    "Groups": "Groups 👥",
    "Time": "Time ⏰",
}

@client.Command(command="Help")
async def help(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "Help")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Help")
async def inlinehelp(event):
    text = STRINGS["main"]
    buttons = []
    for category in CATS:
        buttons.append(Button.inline(f"• {CATS[category]} •", data=f"GetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="Help")
async def callhelp(event):
    text = STRINGS["main"]
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
    text = STRINGS["category"].format(category)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetHelp\:(.*)\:(.*)")
async def getplugin(event):
    plugin = event.data_match.group(1).decode('utf-8')
    category = event.data_match.group(2).decode('utf-8')
    info = client.HELP[category][plugin]
    text = info["Help"] + "\n\n"
    text += "-"*10 + "\n"
    for command in info["Commands"]:
        ComName = command.format(CMD=".")
        share = f"http://t.me/share/text?text={ComName}"
        text += f"[Share]({share})" + ": " + f"`{ComName}`" + "\n"
        text += info["Commands"][command] + "\n"
        text += "•"*10 + "\n"
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"GetCategory:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")]]
    await event.edit(text=text, buttons=buttons) 

@client.Callback(data="CloseHelp")
async def closehelp(event):
    text = STRINGS["closehelp"]
    await event.edit(text=text)
