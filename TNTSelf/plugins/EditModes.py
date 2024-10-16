from TNTSelf import client

Commands = {}
PATTERN = ""
for Mode in client.functions.EDITS:
    PATTERN += Mode + "|"
    Cmd = "{CMD}" + Mode + " <On-Off>"
    infoCmd = {
        "Help": f"To Turn On-Off {Mode} Edit Mode",
    }
    Commands.update({Cmd: infoCmd})
PATTERN = PATTERN[:-1]

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
    "editmode": "**{STR} The Edit Mode** ( `{}` ) **Has Been {}!**"
}

@client.Command(command=f"({PATTERN}) (On|Off)")
async def editmodechanger(event):
    await event.edit(client.STRINGS["wait"])
    editmode = event.pattern_match.group(1).title()
    change = event.pattern_match.group(2).upper()
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    getMode = client.DB.get_key("EDIT_MODE")
    if change == "ON":
        client.DB.set_key("EDIT_MODE", editmode)
    else:
        if getMode == editmode:
            client.DB.set_key("EDIT_MODE", None)
    text = client.getstrings(STRINGS)["editmode"].format(editmode, showchange)
    await event.edit(text)

@client.Command(allowedits=False, checkCmd=True)
async def editmodes(event):
    if not event.raw_text: return
    editmode = client.DB.get_key("EDIT_MODE") or ""
    if editmode == "Bold":
        await event.edit("**" + event.raw_text + "**")
    elif editmode == "Mono":
        await event.edit("`" + event.raw_text + "`")
    elif editmode == "Italic":
        await event.edit("__" + event.raw_text + "__")
    elif editmode == "Underline":
        await event.edit("<u>" + event.raw_text + "</u>", parse_mode="HTML")
    elif editmode == "Strike":
        await event.edit("~~" + event.raw_text + "~~")
    elif editmode == "Spoiler":
        await event.edit("||" + event.raw_text + "||")
    elif editmode == "Hashtag":
        newtext = event.raw_text.replace(" ", "_")
        newtext = newtext.replace("\n", "_")
        await event.edit("#" + newtext)
    elif editmode == "Mention":
        if event.is_reply:
            userid = event.reply_message.sender_id
        elif event.is_private:
            userid = event.chat_id
        else:
            userid = event.sender_id
        text = f"[{event.raw_text}](tg://user?id={userid})"
        await event.edit(text)