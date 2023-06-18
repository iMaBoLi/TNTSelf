from FidoSelf import client
from telethon import Button, events
from .MainHelp import STRINGS, CATS

@client.Command(command="GetHelp ?(.*)?")
async def gethelp(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    res = await client.inline_query(client.bot.me.username, f"GetUserHelp:{userid}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.bot.on(events.InlineQuery(pattern="GetUserHelp\:(.*)"))
async def inlinehelp(event):
    userid = int(event.pattern_match.group(1))
    if event.sender_id != userid: return
    info = await client.get_entity(event.sender_id)
    text = STRINGS["main"].format(client.mention(info))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        ShowName = CATS[category].format(plugcount)
        buttons.append(Button.inline(ShowName, data=f"OTHERGetCategory:{userid}:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"OTHERCloseHelp:{userid}")])
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.bot.on(events.CallbackQuery(data="OTHERHelp\:(.*)"))
async def callhelp(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    if event.sender_id != userid:
        return await event.answer("• This Is Not For You!", alert=True)
    info = await client.get_entity(event.sender_id)
    text = STRINGS["main"].format(client.mention(info))
    buttons = []
    for category in CATS:
        plugcount = len(client.HELP[category])
        ShowName = CATS[category].format(plugcount)
        buttons.append(Button.inline(ShowName, data=f"OTHERGetCategory:{userid}:{category}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"OTHERCloseHelp:{userid}")])
    await event.edit(text=text, buttons=buttons)

@client.bot.on(events.CallbackQuery(data="OTHERGetCategory\:(.*)\:(.*)"))
async def getcategory(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    category = str(event.data_match.group(2).decode('utf-8'))
    if event.sender_id != userid:
        return await event.answer("• This Is Not For You!", alert=True)
    buttons = []
    for plugin in client.HELP[category]:
        buttons.append(Button.inline(f"• {plugin} •", data=f"OTHERGetHelp:{userid}:{plugin}:{category}"))
    buttons = client.functions.chunker(buttons, sizes=[3,2])
    buttons.append([Button.inline(client.STRINGS["inline"]["Back"], data=f"OTHERHelp:{userid}"), Button.inline(client.STRINGS["inline"]["Close"], data=f"OTHERCloseHelp:{userid}")])
    text = STRINGS["category"].format(client.mention(client.me), category)
    await event.edit(text=text, buttons=buttons)

@client.bot.on(events.CallbackQuery(data="OTHERGetHelp\:(.*)\:(.*)\:(.*)"))
async def getplugin(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    plugin = event.data_match.group(2).decode('utf-8')
    category = event.data_match.group(3).decode('utf-8')
    if event.sender_id != userid:
        return await event.answer("• This Is Not For You!", alert=True)
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
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"OTHERGetCategory:{userid}:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data=f"OTHERCloseHelp:{userid}")]]
    await event.edit(text=text, buttons=buttons) 

@client.bot.on(events.CallbackQuery(data=f"OTHERCloseHelp\:(.*)"))
async def closehelp(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    if event.sender_id != userid:
        return await event.answer("• This Is Not For You!", alert=True)
    text = STRINGS["closehelp"]
    await event.edit(text=text)