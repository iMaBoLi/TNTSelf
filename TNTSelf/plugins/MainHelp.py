from TNTSelf import client
from telethon import Button
from .Variebels import VARIEBELS
import re

__INFO__ = {
    "Category": "Setting",
    "Name": "Help",
    "Info": {
        "Help": "To Get Help About Self Commands!",
        "Commands": {
            "{CMD}Help": {
                "Help": "To Get Help Panel!",
            },
            "{CMD}Help <Name>": {
               "Help": "To Get Help Of Plugin",
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
    "notplug": "✾ The Plugins In This Category Is Not Founded!",
    "main": "**ᯓ Dear** ( {} )\n   **✾ Welcome To TNT Self Help!**\n      **✾ Please Select The Category You Want:**",
    "category": "**ᯓ Dear** ( {} )\n   **✾ Welcome To** ( `{}` ) **Category Help!**\n      **✾ Please Choose Plugin To Get Info:**",
    "closehelp": "**☻ The Help Panel Successfully Closed!**",
}

CATEGORYS = {
    "Setting": ["Help", "Panel", "Language", "Lists", "Manage", "Save", "Command", "Realm", "BackUp", "Simbel", "Ping", "Reload"],
    "Manage": ["Quick", "Spector", "Save", "Auto", "Love", "White", "Black", "MarkRead", "Enemy", "Foshs", "Echo", "Timer", "Until"],
    "Tools": ["Download", "Time", "Translate", "Upload Site", "SpeechText", "RemoveBg", "Ocr", "Logo", "Image Slicer", "Screen Shot", "Open Ai", "Ai Image", "Country Info", "Najva"],
    "Practical": ["Action", "Copy Action", "Edit Modes", "Anti Forward", "Anti Edit", "Auto Delete", "Auto Translate", "Reaction", "Repeat", "Replace", "Emoji", "Poker"],
    "Usage": ["Youtube", "Spotify", "Google Play", "Trim Video", "Trim Audio", "Cover File", "Video Shot", "Shazam", "Search Music", "Extract Audio", "Edit Duration", "Music Info", "Rotater"],
    "Time": ["Name Time", "Bio Time", "Photo Time", "Font", "Text Time"],
    "Convert": ["Convert Video", "Convert Photo", "Color Photo", "Filter Video", "Filter Photo", "Bw Photo", "Mirror Photo", "Round Photo"],
    "Funs": ["Bank Card", "Wikipedia", "FakeMail", "Flood", "Password", "Number To Word", "Say", "Sign", "Len", "Contact", "Emojis"],
    "Account": ["Edit Profile", "Set Profile", "My Info", "My Stickers", "Share Me", "Left", "Online", "Chats Count", "Del Profiles", "Clean Profiles", "Add Contacts", "Del Contacts", "Clean Gifs", "Clean Stickers"],
    "Groups": ["Ban", "Kick", "Mute", "Chat Info", "Search", "Delete Msg", "Welcome", "GoodBy", "Comment", "Auto Join", "Auto Leave", "Invite VC", "Channel Sign", "Global Search"],
    "Pv": ["MutePv", "LockPv", "Anti Spam", "Media Save", "Timer Save", "Clean Medias", "Pv Mute", "Filter Pv"],
    "Users": ["User Info", "Get Profiles", "Get Stories", "Copy Profile"],
    "Variebels": list(VARIEBELS.keys()),
    "Other": [],
}

def search_category(plugin):
    for category in CATEGORYS:
        if plugin in CATEGORYS[category]:
            return category
    if plugin in client.HELP:
        return client.HELP[plugin]["Category"]
    return None

def gethelp(plugin):
    info = client.HELP[plugin]
    text = f"**꥟ Plugin:** ( `{plugin}` )\n"
    category = search_category(plugin)
    text += f"**꥟ Category:** ( `{category}` )\n"
    text += f'**꥟ Help:** ( `{info["Help"]}` )\n\n'
    text += "⊱┈───╌ ❊ ╌───┈⊰\n"
    for i, command in enumerate(info["Commands"]):
        CMD = client.DB.get_key("CMD_SIMBEL") or "."
        cname = command.replace("{CMD}", CMD)
        ccname = cname.split(" ")[0]
        scname = "`" + cname.replace(" ", "` `") + "`"
        share = f"http://t.me/share/text?text={ccname}"
        text += f"\n[𒆜]({share}) : " + scname + "\n"
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

def search_plugin(query):
    query = query.replace(" ", "").lower()
    for plugin in client.HELP:
        plname = plugin.replace(" ", "").lower()
        if query == plname:
            return plugin
        for com in client.HELP[plugin]["Commands"]:
            search = re.search(query, com.lower())
            if search:
                return plugin
    return None

@client.Command(command="Help ?(.*)?")
async def help(event):
    await event.edit(client.STRINGS["wait"])
    pname = event.pattern_match.group(1)
    if pname:
        plugin = search_plugin(pname)
        if not plugin:
            return await event.edit(client.getstrings(STRINGS)["notfound"].format(pname))
        text = gethelp(plugin)
        return await event.edit(text)
    else:
        res = await client.inline_query(client.bot.me.username, "Help")
        await res[0].click(event.chat_id)
        await event.delete()

@client.Inline(pattern="Help")
async def inlinehelp(event):
    text = client.getstrings(STRINGS)["main"].format(client.functions.mention(client.me))
    buttons = []
    for category in CATEGORYS:
        sname = "「 " + category + " 」"
        buttons.append(Button.inline(sname, data=f"GetCategory:{category}"))
    buttons = client.functions.chunker(buttons, [2,1])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.answer([event.builder.article("TNTSelf - Help", text=text, buttons=buttons)])

@client.Callback(data="Help")
async def callhelp(event):
    text = client.getstrings(STRINGS)["main"].format(client.functions.mention(client.me))
    buttons = []
    for category in CATEGORYS:
        sname = "「 " + category + " 」"
        buttons.append(Button.inline(sname, data=f"GetCategory:{category}"))
    buttons = client.functions.chunker(buttons, [2,1])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetCategory\\:(.*)")
async def getcategory(event):
    category = str(event.data_match.group(1).decode('utf-8'))
    buttons = []
    if not CATEGORYS[category]:
        return await event.answer(client.getstrings(STRINGS)["notplug"], alert=True)
    for plugin in CATEGORYS[category]:
        buttons.append(Button.inline(f"๑ {plugin} ๑", data=f"GetHelp:{plugin}:{category}"))
    buttons = client.functions.chunker(buttons, [2,1])
    buttons.append([Button.inline(client.STRINGS["inline"]["Back"], data="Help"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")])
    text = client.getstrings(STRINGS)["category"].format(client.functions.mention(client.me), category)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetHelp\\:(.*)\\:(.*)")
async def getplugin(event):
    plugin = event.data_match.group(1).decode('utf-8')
    category = event.data_match.group(2).decode('utf-8')
    text = gethelp(plugin)
    buttons = [[Button.inline(client.STRINGS["inline"]["Back"], data=f"GetCategory:{category}"), Button.inline(client.STRINGS["inline"]["Close"], data="CloseHelp")]]
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="CloseHelp")
async def closehelp(event):
    text = client.getstrings(STRINGS)["closehelp"]
    await event.edit(text=text)