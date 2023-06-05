from FidoSelf import client
from telethon import Button
import os

STRINGS = {
    "nall": "**The Photo Name** ( `{}` ) **Already In Photo List!**",
    "nin": "**The Photo** ( `{}` ) **Not In Photo List!**",
    "del": "**The Photo** ( `{}` ) **Deleted From Photo List!**",
    "get": "**Photo Name:** ( `{}` )\n**Where:** ( `{}` )\n**Size:** ( `{}` )\n**Color:** ( `{}` )\n**Font:** ( `{}` )\n**Align:** ( `{}` )",
    "empty": "**The Photo List Is Empty!**",
    "list": "**The Photo List:**\n\n",
    "aempty": "**The Photo List Is Already Empty!**",
    "clean": "**The Photo List Is Cleaned!**",
    "where": "**Select Where Should Be Write Text On Photo:**",
    "size": "**Select Size Of The Text Time:**",
    "color": "**Select Color For Your Time Text:**",
    "font": "**Select Font For Your Time Text:**",
    "align": "**Please Specify How To Align The Time Text On This Image:**",
    "com": "**The New Photo Was Saved!**\n\n**Photo Name:** ( `{}` )\n**Where:** ( `{}` )\n**Size:** ( `{}` )\n**Color:** ( `{}` )\n**Font:** ( `{}` )\n**Align:** ( `{}` )",
}

@client.Command(command="AddPhoto (.*)")
async def addphoto(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    phname = str(event.pattern_match.group(1))
    phname = phname + ".png"
    photos = client.DB.get_key("PHOTOS") or {}
    if phname in photos:
        return await event.edit(STRINGS["nall"].format(phname))
    info = await event.reply_message.save()
    photos.update({phname: info})
    client.DB.set_key("PHOTOS", photos)
    res = await client.inline_query(client.bot.me.username, f"addphoto:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()

@client.Command(command="DelPhoto (.*)")
async def delphoto(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(STRINGS["nin"].format(phname))
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(STRINGS["del"].format(phname))

@client.Command(command="GetPhoto (.*)")
async def getphoto(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(STRINGS["nin"].format(phname))
    photo = photos[phname]
    get = await client.get_messages(photo["chat_id"], ids=int(photo["msg_id"]))
    fphoto = await get.download_media()
    caption = STRINGS["get"].format(phname, photo["where"], photo["size"].title(), photo["color"].title(), photo["font"].title(), photo["align"].title())
    await event.respond(caption=caption, file=fphoto)
    await event.delete()
    os.remove(fphoto)

@client.Command(command="PhotoList")
async def photolist(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for photo in photos:
        text += f"**{row} -** `{photo}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanPhotoList")
async def cleanphotos(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("PHOTOS")
    await event.edit(STRINGS["clean"])

@client.Inline(pattern="addphoto\:(.*)")
async def addphoto(event):
    phname = str(event.pattern_match.group(1))
    text = STRINGS["where"]
    buttons = []
    for where in ["↖️", "⬆️", "↗️", "⬅️", "⏺", "➡️", "↙️", "⬇️", "↘️"]:
        buttons.append(Button.inline(f"• {where} •", data=f"sizephoto:{phname}:{where}"))
    buttons = list(client.utils.chunks(buttons, 3))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"photoclose:{phname}")])
    await event.answer([event.builder.article("FidoSelf - Photo", text=text, buttons=buttons)])

@client.Callback(data="(.*)photo\:(.*)")
async def photo(event):
    work = str(event.data_match.group(1).decode('utf-8'))
    data = (str(event.data_match.group(2).decode('utf-8'))).split(":")
    photos = client.DB.get_key("PHOTOS") or {}
    phname = data[0]
    where = data[1]
    if work == "size":
        text = STRINGS["size"]
        buttons = [[Button.inline("• Very Small •", data=f"colorphoto:{phname}:{where}:vsmall"), Button.inline("• Small •", data=f"colorphoto:{phname}:{where}:small")], [Button.inline("• Medium •", data=f"colorphoto:{phname}:{where}:medium")], [Button.inline("• Big •", data=f"colorphoto:{phname}:{where}:big"), Button.inline("• Very Big •", data=f"colorphoto:{phname}:{where}:vbig")]]
        buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "color":
        size = data[2]
        text = STRINGS["color"]
        buttons = [[Button.inline("Random ♻️", data=f"fontphoto:{phname}:{where}:{size}:random")]]
        for color in client.functions.COLORS:
            buttons.append(Button.inline(f"• {color.title()} •", data=f"fontphoto:{phname}:{where}:{size}:{color}"))
        buttons = [buttons[0]] + list(client.utils.chunks(buttons[1:], 4))
        buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "font":
        size = data[2]
        color = data[3]
        text = STRINGS["font"]
        fonts = client.DB.get_key("FONTS")
        if len(fonts) == 0:
            return await event.answer(f"Please Save A Font File First!", alert=True)
        buttons = [[Button.inline("Random ♻️", data=f"alignphoto:{phname}:{where}:{size}:{color}:random")]]
        for font in fonts:
            buttons.append(Button.inline(f"• {font.title()} •", data=f"alignphoto:{phname}:{where}:{size}:{color}:{font}"))
        buttons = [buttons[0]] + list(client.utils.chunks(buttons[1:], 2))
        buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "align":
        size = data[2]
        color = data[3]
        font = data[4]
        text = STRINGS["align"]
        buttons = [[Button.inline("• Left •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}:left"), Button.inline("• Center •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}:center"), Button.inline("• Right •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}:right")]]
        buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"photoclose:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "complete":
        size = data[2]
        color = data[3]
        font = data[4]
        align = data[5]
        data = client.DB.get_key("PHOTOS")[phname]
        photos.update({phname: {"chat_id": data["chat_id"], "msg_id": data["msg_id"], "where": where,"size": size,"color": color,"font": font,"align": align}})
        client.DB.set_key("PHOTOS", photos)
        complete = STRINGS["com"].format(phanme, where, size.title(), color.title(), font.title(), align.title())
        await event.edit(text=caomplete)
        
@client.Callback(data="photoclose\:(.*)")
async def closephoto(event):
    phname = str(event.data_match.group(1).decode('utf-8'))
    photos = client.DB.get_key("PHOTOS") or {}
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(text=f"**The Photo Panel Successfuly Closed!**")