from FidoSelf import client
from telethon import Button

STRINGS = {
    "category": "**» Welcome To Fido Self Help!**\n**• Please Select The Category You Want:**",
    "closehelp": "**The Help Panel Successfully Closed!**",
    "Categorys": {
        "Setting": "Settings ⚙️",
        "Manager": "Manager 👮",
        "Tools": "Tools 🔧",
        "Account": "Account 💎",
        "Groups": "Groups 👥",
        "Time": "Time ⏰",
    },
}
def get_helpbuttons():
    buttons = []
    CATS = STRINGS["Categorys"]
    for Category in CATS:
        buttons.append(Button.inline(f"• {CATS[Category]} •", data=f"GetCategory:{Category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    return buttons

def get_plugins(Category):
    plugins = []
    for plugin in client.HELP[Category]:
        plugins.append(plugin)
    return plugins

def get_catbuttons(Category):
    buttons = []
    plugins = get_plugins(Category)
    for plugin in plugins:
        emoji = client.DB.get_key("HELP_EMOJI") or "•"
        name = emoji + " " + plugin + " " + emoji
        buttons.append(Button.inline(name, data=f"GetHelp:{plugin}:{Category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline("• Back •", data=f"Help")])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    return buttons

@client.Command(command="Help")
async def help(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "Help")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Help")
async def inlinehelp(event):
    text = STRINGS["category"]
    buttons = get_helpbuttons()
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="Help")
async def callhelp(event):
    text = STRINGS["category"]
    buttons = get_helpbuttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetCategory\:(.*)")
async def getcategory(event):
    Category = str(event.data_match.group(1).decode('utf-8'))
    buttons = get_catbuttons(Category)
    text = STRINGS["category"]
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetHelp\:(.*)\:(.*)")
async def getplugin(event):
    plugin = str(event.data_match.group(1).decode('utf-8'))
    Category = int(event.data_match.group(2).decode('utf-8'))
    text = client.HELP[Category][plugin]
    buttons = [[Button.inline("• Back •", data=f"GetCategory:{Category}"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")]]
    await event.edit(text=text, buttons=buttons) 

@client.Callback(data="CloseHelp")
async def closehelp(event):
    text = STRINGS["closehelp"]
    await event.edit(text=text)
