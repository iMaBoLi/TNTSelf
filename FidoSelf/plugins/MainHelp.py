from FidoSelf import client
from telethon import Button

CATEGORY = "Setting"
__INFO__ = {
    "Category": CATEGORY,
    "Plugname": "Help",
    "Pluginfo": {
        "Help": "To Get Help About Self Commands!",
        "Commands": {
            "{CMD}Help": {
                "Help": "To Get Help Panel!",
            },
            "{CMD}Help <Name>": {
                "Help": "To Get Help Of Plugin!",
                "Input": {
                    "<Name>" : "Name Of Plugin"
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notfound": "**✾ The Plugin With Name** ( `{}` ) **Is Not Available!**",
    "plinfo": "**» The Plugin Info:** ( `{}` - `{}` )\n\n",
    "main": "**ᯓ Dear** ( {} )\n   **✾ Welcome To Fido Self Help!**\n      **✾ Please Select The Category You Want:**",
    "category": "**ᯓ Dear** ( {} )\n   **✾ Welcome To** ( `{}` ) **Category Help!**\n      **✾ Please Choose Plugin To Get Info:**",
    "closehelp": "**☻ The Help Panel Successfully Closed!**",
}

CATS = [
    "Setting",
    "Manage",
    "Tools",
    "Practical",
    "Usage",
    "Funs",
    "Account",
    "Group",
    "Private",
    "Variebels"
    "Other",
]

def gethelp(category, plugin):
    info = client.HELP[category][plugin]
    text = "**꥟ Note:** ( `" + info["Help"] + "` )\n"
    for i, command in enumerate(info["Commands"]):
        cname = command.replace("{CMD}", ".")
        ccname = cname.split(" ")[0]
        share = f"http://t.me/share/text?text={ccname}"
        text += f"\n[𒆜]({share})" + " : " + f"`{cname}`" + "\n"
        if info["Commands"][command]:
            text += "\n"
            hcom = info["Commands"][command]
            if "Help" in hcom:
                text += "    **💡 Help:** __" + hcom["Help"] + "__\n"
            if "Input" in hcom:
                for inp in hcom["Input"]:
                    inpinf = hcom["Input"][inp]
                    text += f"    **✏️** `{inp}` : __{inpinf}__\n"
            if "Getid" in hcom:
                text += "    **🆔 GetID:** __" + hcom["Getid"] + "__\n"
            if "Reply" in hcom:
                replyes = ""
                for reply in hcom["Reply"]:
                    replyes += f"__{reply}__ - "
                replyes = replyes[:-3]
                text += "    **↩️ Reply:** " + replyes + "\n"
            if "Vars" in hcom:
                variebels = ""
                for var in hcom["Vars"]:
                    variebels += f"\n          `{var}`"
                text += "    **📍 Variebels:** " + variebels + "\n"
            if "Note" in hcom:
                text += "    **📝 Note:** __" + hcom["Note"] + "__\n"
        if len(info["Commands"]) != (i + 1):
            text += "\n┈━━═ ☆ ═━━┈\n"
    return text

def search_plugin(pluginname):
    pluginname = pluginname.replace(" ", "").lower()
    for category in client.HELP:
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
        text = STRINGS["plinfo"].format(plugin, category)
        text += gethelp(category, plugin)
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
        sname = "「 " + category + " 」"
        buttons.append(Button.inline(sname, data=f"GetCategory:{category}"))
    buttons = client.functions.chunker(buttons, [2,1])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.answer([event.builder.article("FidoSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="Help")
async def callhelp(event):
    text = STRINGS["main"].format(client.functions.mention(client.me))
    buttons = []
    for category in CATS:
        sname = "「 " + category + " 」"
        buttons.append(Button.inline(sname, data=f"GetCategory:{category}"))
    buttons = client.functions.chunker(buttons, [2,1])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetCategory\:(.*)")
async def getcategory(event):
    category = str(event.data_match.group(1).decode('utf-8'))
    buttons = []
    for plugin in client.HELP[category]:
        buttons.append(Button.inline(f"๑ {plugin} ๑", data=f"GetHelp:{plugin}:{category}"))
    buttons = client.functions.chunker(buttons, [2,1])
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