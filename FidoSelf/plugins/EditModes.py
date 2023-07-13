from FidoSelf import client

Commands = {}
for Mode in client.functions.EDITS:
    Cmd = "{CMD}" + Mode + " <On-Off>"
    AllCmd = "{CMD}" + Mode + "All" + " <On-Off>"
    infoCmd = {
        "Help": f"To Turn On-Off {Mode} Edit Mode",
    }
    infoAllCmd = {
        "Help": f"To Turn On-Off {Mode} All Edit Mode",
    }
    Commands.update({Cmd: infoCmd})
    Commands.update({AllCmd: infoAllCmd})

__INFO__ = {
    "Category": "Practical",
    "Name": "Edit Modes",
    "Info": {
        "Help": "To Setting Edit Modes For Your Texts!",
        "Commands": Commands,
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "editchat": "**{STR} The Edit Mode** ( `{}` ) **For This Chat Has Been {}!**",
    "editall": "**{STR} The Edit Mode** ( `{}` ) **Has Been {}!**"
}

PATTERN = ""
for mode in client.functions.EDITS:
    PATTERN += mode + "|"
    PATTERN += mode + "All" + "|"
PATTERN = PATTERN[:-1]

@client.Command(command=f"({PATTERN}) (On|Off)")
async def editchanger(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).title()
    change = event.pattern_match.group(2).upper()
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    if type.endswith("all"):
        getMode = client.DB.get_key("EDIT_MODE")
        if change == "ON":
            type = type.replace("all", "")
            client.DB.set_key("EDIT_MODE", str(type))
            settext = client.getstrings(STRINGS)["editall"].format(type, showchange)
        else:
            type = type.replace("all", "")
            if getMode == type:
                client.DB.set_key("EDIT_MODE", None)
            settext = client.getstrings(STRINGS)["editall"].format(type, showchange)
    else:
        echats = client.DB.get_key("EDIT_CHATS") or {}
        chatid = event.chat_id
        if chatid not in echats:
            echats.update({chatid: ""})
        if change == "ON":
            echats[chatid] = type
            client.DB.set_key("EDIT_CHATS", echats)
            settext = client.getstrings(STRINGS)["editchat"].format(type, showchange)
        else:
            if echats[chatid] == type:
                echats[chatid] = ""
            settext = client.getstrings(STRINGS)["editchat"].format(type, showchange)
    await event.edit(settext)

@client.Command(allowedits=False)
async def editmodes(event):
    if not event.text or event.checkCmd(): return
    allmode = client.DB.get_key("EDIT_MODE") or ""
    chats = client.DB.get_key("EDIT_CHATS") or {}
    lasttext = str(event.text)
    if allmode == "Bold" or (event.chat_id in chats and chats[event.chat_id] == "Bold"):
        await event.edit("**" + lasttext + "**")
    elif allmode == "Mono" or (event.chat_id in chats and chats[event.chat_id] == "Mono"):
        await event.edit("`" + lasttext + "`")
    elif allmode == "Italic" or (event.chat_id in chats and chats[event.chat_id] == "Italic"):
        await event.edit("__" + lasttext + "__")
    elif allmode == "Underline" or (event.chat_id in chats and chats[event.chat_id] == "Underline"):
        await event.edit("<u>" + lasttext + "</u>", parse_mode="HTML")
    elif allmode == "Strike" or (event.chat_id in chats and chats[event.chat_id] == "Strike"):
        await event.edit("~~" + lasttext + "~~")
    elif allmode == "Spoiler" or (event.chat_id in chats and chats[event.chat_id] == "Spoiler"):
        await event.edit("||" + lasttext + "||")
    elif allmode == "Hashtag" or (event.chat_id in chats and chats[event.chat_id] == "Hashtag"):
        lasttext = lasttext.replace(" ", "_")
        lasttext = lasttext.replace("\n", "_")
        await event.edit("#" + lasttext)
    elif allmode == "Mention" or (event.chat_id in chats and chats[event.chat_id] == "Mention"):
        if event.is_reply:
            userid = event.reply_message.sender_id
        elif event.is_private:
            userid = event.chat_id
        else:
            userid = event.sender_id
        text = f"[{event.text}](tg://user?id={userid})"
        await event.edit(text)