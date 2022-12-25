from FidoSelf import client

EDITS = ["Bold", "Mono", "Italic", "Underline", "Strike", "Spoiler"]

@client.Cmd(edits=False)
async def editmodes(event):
    if event.is_cmd or not event.text: return
    mode = client.DB.get_key("EDIT_MODE") or False
    lasttext = str(event.text)
    if not mode:
        return
    elif mode == "Bold":
        await event.edit("**" + lasttext + "**")
    elif mode == "Mono":
        await event.edit("`" + lasttext + "`")
    elif mode == "Italic":
        await event.edit("__" + lasttext + "__")
    elif mode == "Underline":
        await event.edit("<u>" + lasttext + "</u>", parse_mode="HTML")
    elif mode == "Strike":
        await event.edit("~~" + lasttext + "~~")
    elif mode == "Spoiler":
        await event.edit("||" + lasttext + "||")
