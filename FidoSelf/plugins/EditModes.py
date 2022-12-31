from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}E(Bold|Mono|Italic|Underline|Strike|Spoiler|Hashtag) (On|off)$")
async def bio(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    mode = event.pattern_match.group(1).lower()
    change = event.pattern_match.group(2).lower()
    last = client.DB.get_key("EDIT_MODE") or ""
    if change == "on":
        if not str(last).lower() == str(mode):
            client.DB.set_key("EDIT_MODE", mode.title())
            await event.edit(f"**{client.str} The {mode.title()} Edit Texts Mode Has Been Actived!**")
        else:
            await event.edit(f"**{client.str} The {mode.title()} Edit Texts Mode Is Already Actived!**")
    else:
        if str(last) == str(mode):
            client.DB.set_key("EDIT_MODE", False)
            await event.edit(f"**{client.str} The {mode.title()} Edit Texts Mode Has Been DeActived!**")
        else:
            await event.edit(f"**{client.str} The {mode.title()} Edit Texts Mode Is Already DeActived!**")

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
