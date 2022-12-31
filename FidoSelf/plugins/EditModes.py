from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}E(Bold|Mono|Italic|Underline|Strike|Spoiler|Hashtag) (On|off)$")
async def bio(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    change = event.pattern_match.group(2).lower()
    changer = client.get_string("Change_1") if change == "on" else client.get_string("Change_2")
    if change == "on":
        client.DB.set_key("EDIT_MODE", mode.title())
    else:
        client.DB.del_key("EDIT_MODE")
    mode = client.get_string(f"Edits_{mode.title()}")
    await event.edit(client.get_string("EditMode_1").format(mode.title(), changer))

@client.Cmd(edits=False)
async def editmodes(event):
    if event.is_cmd or not event.text: return
    mode = client.DB.get_key("EDIT_MODE") or ""
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
    elif mode == "Hashtag":
        lasttext = lasttext.replace(" ", "_")
        await event.edit("#" + lasttext)
