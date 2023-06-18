from FidoSelf import client
from telethon import Button, events
from .MainHelp import STRINGS, CATS

@client.bot.on(events.NewMessage(pattern="(?i)^\/Gethelp$", incoming=True))
async def gethelp(event):
    reply = await event.reply(client.STRINGS["wait"])
    userid = event.sender_id
    info = await client.get_entity(event.sender_id)
    text = STRINGS["main"].format(client.mention(info))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        sname = CATS[category].format(plugcount)
        buttons.append(Button.inline(sname, data=f"OtherGetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="OtherCloseHelp")])
    await event.reply(text, buttons=buttons)
    await reply.delete()
    
@client.bot.on(events.CallbackQuery(data="OtherHelp"))
async def callhelp(event):
    info = await client.get_entity(event.sender_id)
    text = STRINGS["main"].format(client.mention(info))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        sname = CATS[category].format(plugcount)
        buttons.append(Button.inline(sname, data=f"OtherGetCategory:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="OtherCloseHelp")])
    await event.edit(text=text, buttons=buttons)

@client.bot.on(events.CallbackQuery(data="OtherGetCategory\:(.*)"))
async def getcategory(event):
    category = str(event.data_match.group(1).decode('utf-8'))
    buttons = []
    for plugin in client.HELP[category]:
        buttons.append(Button.inline(f"• {plugin} •", data=f"OtherGetHelp:{plugin}:{category}"))
    buttons = client.functions.chunker(buttons, sizes=[3,2])
    buttons.append([Button.inline(client.STRINGS["inline"]["Back"], data="OtherHelp"), Button.inline(client.STRINGS["inline"]["Close"], data="OtherCloseHelp")])
    text = STRINGS["category"].format(client.mention(client.me), category)
    await event.edit(text=text, buttons=buttons)

@client.bot.on(events.CallbackQuery(data="OtherGetHelp\:(.*)\:(.*)"))
async def getplugin(event):
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
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"OtherGetCategory:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data="OtherCloseHelp")]]
    await event.edit(text=text, buttons=buttons) 

@client.bot.on(events.CallbackQuery(data="OtherCloseHelp"))
async def closehelp(event):
    text = STRINGS["closehelp"]
    await event.edit(text=text)