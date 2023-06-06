from FidoSelf import client

STRINGS = {
    "more": "**Sorry, You Cannot Save More Than 10 Fonts!**",
    "ttf": "**Please Reply To Font File With .TTF Format!**",
    "newnot": "**The Font** ( `{}` ) **Already In Font List!**",
    "newadd": "**The Font** ( `{}` ) **Added To Font List!**",
    "delnot": "**The Font** ( `{}` ) **Not In Font List!**",
    "del": "**The Font** ( `{}` ) **Deleted From Font List!**",
    "empty": "**The Font List Is Empty!**",
    "list": "**The Font List:**\n\n",
    "aempty": "**The Font List Is Already Empty!**",
    "clean": "**The Font List Is Cleaned!**",
}

@client.Command(command="NewFont (.*)")
async def savefontfile(event):
    await event.edit(client.STRINGS["wait"])
    fname = str(event.pattern_match.group(1))
    fonts = client.DB.get_key("FONTS") or {}
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["File"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["File"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if (fname + ".ttf") in fonts:
        return await event.edit(STRINGS["newnot"].format(fname + ".ttf"))
    if len(fonts) > 10:
        return await event.edit(STRINGS["more"])
    format = str(event.reply_message.media.document.attributes[0].file_name).split(".")[-1]
    if format != "ttf":
        return await event.edit(STRINGS["ttf"])
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + fname + ".ttf")
    fonts.update({fname + ".ttf": info})
    client.DB.set_key("FONTS", fonts)
    await event.edit(STRINGS["newadd"].format(fname + ".ttf"))

@client.Command(command="DelFont (.*)")
async def delfontfile(event):
    await event.edit(client.STRINGS["wait"])
    fname = str(event.pattern_match.group(1))
    fonts = client.DB.get_key("FONTS") or {}
    if fname not in fonts:
        return await event.edit(STRINGS["delnot"].format(fname))
    del fonts[fname]
    client.DB.set_key("FONTS", fonts)
    await event.edit(STRINGS["del"].format(fname)) 

@client.Command(command="FontList")
async def fontlist(event):
    await event.edit(client.STRINGS["wait"])
    fonts = client.DB.get_key("FONTS") or {}
    if not fonts:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for font in fonts:
        text += f"**{row} -** `{font}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanFontList")
async def cleanfonts(event):
    await event.edit(client.STRINGS["wait"])
    fonts = client.DB.get_key("FONTS") or {}
    if not fonts:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("FONTS")
    await event.edit(STRINGS["clean"])