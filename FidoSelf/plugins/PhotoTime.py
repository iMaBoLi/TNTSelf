from FidoSelf import client
from telethon import Button
from FidoSelf.plugins.ManageTime import COLORS
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}Photo (On|Off)$")
async def photo(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("PHOTO_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Photo Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddPhoto (.*)$")
async def addphoto(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.reply_message or not event.reply_message.photo:
        return await event.edit(f"**{client.str} Please Reply To Photo!**")
    phname = str(event.pattern_match.group(1))
    phname = phname + ".png"
    photos = client.DB.get_key("PHOTOS") or {}
    if phname in photos:
        return await event.edit(f"**{client.str} The Photo Name** ( `{phname}` ) **Already In Photo List!**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    photos.update({phname: {"chat_id": client.backch, "msg_id": forward.id}})
    client.DB.set_key("PHOTOS", photos)
    res = await client.inline_query(client.bot.me.username, f"addphoto:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelPhoto (.*)$")
async def delphoto(event):
    await event.edit(f"**{client.str} Processing . . .**")
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(f"**{client.str} The Photo** ( `{phname}` ) **Not In Photo List!**")
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(f"**{client.str} The Photo** ( `{phname}` ) **Deleted From Photo List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}PhotoList$")
async def photolist(event):
    await event.edit(f"**{client.str} Processing . . .**")
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(f"**{client.str} The Photo List Is Empty!**")
    text = f"**{client.str} The Photo List:**\n\n"
    row = 1
    for photo in photos:
        text += f"**{row} -** `{photo}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanPhotoList$")
async def cleanphotos(event):
    await event.edit(f"**{client.str} Processing . . .**")
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(f"**{client.str} The Photo List Is Already Empty!**")
    client.DB.del_key("PHOTOS")
    await event.edit(f"**{client.str} The Photo List Is Cleared!**")

@client.Inline(pattern="addphoto\:(.*)")
async def addphoto(event):
    phname = str(event.pattern_match.group(1))
    text = f"**{client.str} Please Choose Where Should Be Write Text On Photo:**"
    buttons = []
    for where in ["↖️", "⬆️", "↗️", "⬅️", "⏺", "➡️", "↙️", "⬇️", "↘️"]:
        buttons.append(Button.inline(f"• {where} •", data=f"sizephoto:{phname}:{where}"))
    buttons = list(client.utils.chunks(buttons, 3))
    buttons.append([Button.inline("🚫 Close 🚫", data=f"close:{phname}")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Photo", text=text, buttons=buttons)])

@client.Callback(data="(.*)photo\:(.*)")
async def photo(event):
    work = str(event.data_match.group(1).decode('utf-8'))
    data = (str(event.data_match.group(2).decode('utf-8'))).split(":")
    photos = client.DB.get_key("PHOTOS") or {}
    phname = data[0]
    where = data[1]
    if work == "size":
        text = f"**{client.str} Please Choose Size Of The Text Time:**"
        buttons = [[Button.inline("• Very Small •", data=f"colorphoto:{phname}:{where}:vsmall"), Button.inline("• Small •", data=f"colorphoto:{phname}:{where}:small")], [Button.inline("• Medium •", data=f"colorphoto:{phname}:{where}:medium")], [Button.inline("• Big •", data=f"colorphoto:{phname}:{where}:big"), Button.inline("• Very Big •", data=f"colorphoto:{phname}:{where}:vbig")]]
        buttons.append([Button.inline("🚫 Close 🚫", data=f"close:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "color":
        size = data[2]
        text = f"**{client.str} Please Choose Color For Your Time Text:**"
        buttons = [[Button.inline(f"Random ♻️", data=f"fontphoto:{phname}:{where}:{size}:random")]]
        for color in COLORS:
            buttons.append(Button.inline(f"• {color.title()} •", data=f"fontphoto:{phname}:{where}:{size}:{color}"))
        buttons = [buttons[0]] + list(client.utils.chunks(buttons[1:], 4))
        buttons.append([Button.inline("🚫 Close 🚫", data=f"close:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "font":
        size = data[2]
        color = data[3]
        text = f"**{client.str} Please Choose Font For Your Time Text:**"
        fonts = os.listdir(client.path + "fonts/")
        if len(fonts) == 0:
            return await event.answer(f"{client.str} Please Save A Font File First!", alert=True)
        buttons = [[Button.inline(f"Random ♻️", data=f"completephoto:{phname}:{where}:{size}:{color}:random")]]
        for font in fonts:
            buttons.append(Button.inline(f"• {font.title()} •", data=f"completephoto:{phname}:{where}:{size}:{color}:{font}"))
        buttons = [buttons[0]] + list(client.utils.chunks(buttons[1:], 2))
        buttons.append([Button.inline("🚫 Close 🚫", data=f"close:{phname}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "complete":
        size = data[2]
        color = data[3]
        font = data[4]
        photos = client.DB.get_key("PHOTOS")[phname]
        photos.update({"where": where,"size": size,"color": color,"font":font})
        client.DB.set_key("PHOTOS", photos)
        await event.edit(text=f"**{client.str} The New Photo Was Saved!**\n\n**{client.str} Photo Name:** ( `{phname}` )\n**{client.str} Where:** ( `{where}` )\n**{client.str} Size:** ( `{size.title()}` )\n**{client.str} Color:** ( `{color.title()}` )\n**{client.str} Font:** ( `{font.title()}` )")

@client.Callback(data="close\:(.*)")
async def closephoto(event):
    phname = str(event.data_match.group(1).decode('utf-8'))
    photos = client.DB.get_key("PHOTOS") or {}
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(text=f"**{client.str} The Photo Panel Successfuly Closed!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddFont (.*)$")
async def savefontfile(event):
    await event.edit(f"**{client.str} Processing . . .**")
    fname = str(event.pattern_match.group(1))
    fonts = client.DB.get_key("FONTS") or {}
    if len(fonts) > 10:
        return await event.edit(f"**{client.str} Sorry, You Cannot Save More Than 10 Fonts!**")
    if not event.reply_message:
        return await event.edit(f"**{client.str} Please Reply To Font File!**")
    format = str(event.reply_message.media.document.attributes[0].file_name).split(".")[-1]
    if format != "ttf":
        return await event.edit(f"**{client.str} Please Reply To A Font File With .TTF Format!**")
    if not client.backch:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(f"**{client.str} The BackUp Channel Is Not Available!**")
    fonts.update({fname + ".ttf": {"chat_id": client.backch, "msg_id": forward.id}})
    client.DB.set_key("FONTS", fonts)
    await event.edit(f"**{client.str} The Font File** ( `{fname}.ttf` ) **Has Been Saved!**")  

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelFont (.*)$")
async def delfontfile(event):
    await event.edit(f"**{client.str} Processing . . .**")
    fname = str(event.pattern_match.group(1))
    fonts = client.DB.get_key("FONTS") or {}
    if fname not in fonts:
        return await event.edit(f"**{client.str} The Font** ( `{fname}` ) **Not In Fonts List!**")
    del fonts[fname]
    client.DB.set_key("FONTS", fonts)
    await event.edit(f"**{client.str} The Font File** ( `{fname}` ) **Has Been Deleted!**")  

@client.Cmd(pattern=f"(?i)^\{client.cmd}FontList$")
async def fontlist(event):
    await event.edit(f"**{client.str} Processing . . .**")
    fonts = client.DB.get_key("FONTS") or {}
    if not fonts:
        return await event.edit(f"**{client.str} The Font File List Is Empty!**")
    text = f"**{client.str} The Font File List:**\n\n"
    row = 1
    for font in fonts:
        text += f"**{row} -** `{font}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanFontList$")
async def cleanfonts(event):
    await event.edit(f"**{client.str} Processing . . .**")
    fonts = os.listdir(client.path + "fonts/")
    if not fonts:
        return await event.edit(f"**{client.str} The Font File List Is Already Empty!**")
    for font in fonts:
        os.remove(client.path + "fonts/" + font)
    await event.edit(f"**{client.str} The Font File List Is Cleared!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddTextTime (.+)$")
async def addtexttime(event):
    await event.edit(f"**{client.str} Processing . . .**")
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    newtexttime = str(event.pattern_match.group(1))
    if newtexttime in texttimes:
        return await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Already In Text Time List!**")  
    trtexts = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "{", "}", "[", "]", "(", ")", " ", ":", "-", "_", "*", "#", "\n"]
    for word in newtexttime:
        if word not in trtexts:
            newtexttime = newtexttime.replace(word, "")
    texttimes += [newtexttime]
    client.DB.set_key("TEXT_TIMES", texttimes)
    await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Added To Text Time List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}DelTextTime (.+)$")
async def deltexttime(event):
    await event.edit(f"**{client.str} Processing . . .**")
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    newtexttime = str(event.pattern_match.group(1))
    if newtexttime not in texttimes:
        return await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Not In Text Time List!**")  
    texttimes = texttimes.remove(newtexttime)
    client.DB.set_key("TEXT_TIMES", texttimes)
    await event.edit(f"**{client.str} The Text Time** ( `{newtexttime}` ) **Deleted From Text Time List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}TextTimeList$")
async def texttimelist(event):
    await event.edit(f"**{client.str} Processing . . .**")
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    if not texttimes:
        return await event.edit(f"**{client.str} The Text Time List Is Empty!**")
    text = f"**{client.str} The Text Time List:**\n\n"
    row = 1
    for texttime in texttimes:
        text += f"**{row} -** `{texttime}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanTextTimeList$")
async def cleantexttimes(event):
    await event.edit(f"**{client.str} Processing . . .**")
    texttimes = client.DB.get_key("TEXT_TIMES") or []
    if not texttimes:
        return await event.edit(f"**{client.str} The Text Time List Is Already Empty!**")
    client.DB.set_key("TEXT_TIMES", [])
    await event.edit(f"**{client.str} The Text Time List Is Cleared!**")
