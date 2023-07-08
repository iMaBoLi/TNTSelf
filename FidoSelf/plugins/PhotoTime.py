from FidoSelf import client
from .ManageTime import photochanger
from telethon import Button
import os

__INFO__ = {
    "Category": "Time",
    "Name": "Photo Time",
    "Info": {
        "Help": "To Save Your Photo For Profile Time!",
        "Commands": {
            "{CMD}Photo <On-Off>": None,
            "{CMD}AddPhoto <Name><Reply(Photo)>": None,
            "{CMD}DelPhoto <Name>": None,
            "{CMD}GetPhoto <Name>": None,
            "{CMD}PhotoList": None,
            "{CMD}CleanPhotoList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**𑁍 The Photo Mode Has Been {}!**",
    "notall": "**𑁍 The Photo** ( `{}` ) **Is Already In Photo List!**",
    "notin": "**𑁍 The Photo** ( `{}` ) **Not In Photo List!**",
    "photopage": "**𑁍 Select And Setting This Photo:**\n\n**Photo Name:** ( `{}` )",
    "setphoto": "**➜ The {} Setting Was Set To** ( `{}` )",
    "savephoto": "**𑁍 The Photo Was Saved!**\n\n**✯ Where:** ( `{}` )\n**✯ Size:** ( `{}` )\n**✯ Color:** ( `{}` )\n**✯ Align:** ( `{}` )",
    "delphoto": "**𑁍 The Photo** ( `{}` ) **Has Been Deleted!**",
    "getphoto": "**✯ Photo Name:** ( `{}` )\n\n**✯ Where:** ( `{}` )\n**✯ Size:** ( `{}` )\n**✯ Color:** ( `{}` )\n**✯ Align:** ( `{}` )",
    "empty": "**𑁍 The Photo List Is Empty!**",
    "listphoto": "**𑁍 The Photo List:**\n\n",
    "allempty": "**𑁍 The Photo List Is Already Empty!**",
    "cleanphoto":  "**𑁍 The Photo List Was Cleaned!**",
    "saveagain":  "**𑁍 The Photo Was Removed Try Again To Save!**",
}

INPHOTO_LIST = {}

@client.Command(command="Photo (On|Off)")
async def photomode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("PHOTO_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))
    await photochanger()

def get_buttons(phname):
    buttons = []
    photos = INPHOTO_LIST
    info = photos[phname]
    wherbts = [[Button.inline("• Where : ⤵️", data="Empty")]]
    owherbts = []
    for where in ["↖️", "⬆️", "↗️", "⬅️", "⏺", "➡️", "↙️", "⬇️", "↘️"]:
        ShowMode = client.STRINGS["inline"]["On"] if str(info["Where"]) == str(where) else client.STRINGS["inline"]["Off"]
        owherbts.append(Button.inline(f"{where} {ShowMode}", data=f"SetPhoto:Where:{phname}:{where}"))
    buttons += wherbts + list(client.functions.chunks(owherbts, 3))
    sizebts = [[Button.inline("• Size : ⤵️", data="Empty")]]
    osizebts = []
    for size in ["Very Small", "Small", "Medium", "Big", "Very Big"]:
        ssize = size.replace(" ", "").lower()
        ShowMode = client.STRINGS["inline"]["On"] if str(info["Size"]) == str(ssize) else client.STRINGS["inline"]["Off"]
        osizebts.append(Button.inline(f"{size} {ShowMode}", data=f"SetPhoto:Size:{phname}:{ssize}"))
    buttons += sizebts + client.functions.chunker(osizebts, [2,1,2])
    colorbts = [[Button.inline("• Color : ⤵️", data="Empty")]]
    ocolorbts = []
    for color in (["Random ♻️"] + client.functions.COLORS):
        scolor = color if color != "Random ♻️" else "Random"
        ShowMode = client.STRINGS["inline"]["On"] if str(info["Color"]) == str(scolor) else client.STRINGS["inline"]["Off"]
        ocolorbts.append(Button.inline(f"{color.title()} {ShowMode}", data=f"SetPhoto:Color:{phname}:{scolor}"))
    buttons += colorbts + list(client.functions.chunks(ocolorbts, 3))
    alignbts = [[Button.inline("• Align : ⤵️", data="Empty")]]
    oalignbts = []
    for align in ["Left", "Center", "Right"]:
        salign = align.lower()
        ShowMode = client.STRINGS["inline"]["On"] if str(info["Align"]) == str(salign) else client.STRINGS["inline"]["Off"]
        oalignbts.append(Button.inline(f"{align} {ShowMode}", data=f"SetPhoto:Align:{phname}:{salign}"))
    buttons += alignbts + list(client.functions.chunks(oalignbts, 3))
    buttons.append([Button.inline("📥 Save ✅", data=f"SavePhoto:{phname}"), Button.inline(client.STRINGS["inline"]["Delete"], data=f"DelPhoto:{phname}")])
    return buttons

@client.Command(command="AddPhoto (.*)")
async def addphoto(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    phname = str(event.pattern_match.group(1)) + ".jpg"
    photos = client.DB.get_key("PHOTO_LIST") or {}
    if phname in photos:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(phname))
    info = await event.reply_message.save()
    INPHOTO_LIST.update({phname: {"chat_id": info["chat_id"], "msg_id": info["msg_id"], "Where": "⏺", "Size": "small", "Color": "Random", "Align": "center", "DO": False}})
    res = await client.inline_query(client.bot.me.username, f"PhotoPage:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()

@client.Command(command="DelPhoto (.*)")
async def delphoto(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTO_LIST") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(phname))
    del photos[phname]
    client.DB.set_key("PHOTO_LIST", photos)
    phfile = client.PATH + phname
    if os.path.exists(phfile):
        os.remove(phfile)
    await event.edit(client.getstrings(STRINGS)["delphoto"].format(phname))
    await photochanger()

@client.Command(command="GetPhoto (.*)")
async def getphoto(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTO_LIST") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(phname))
    photo = photos[phname]
    fphoto = client.PATH + phname
    caption = client.getstrings(STRINGS)["getphoto"].format(phname, photo["Where"], photo["Size"], photo["Color"], photo["Align"])
    await event.respond(caption, file=fphoto)
    await event.delete()

@client.Command(command="PhotoList")
async def photolist(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTO_LIST") or {}
    if not photos:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["listphoto"]
    for row, photo in enumerate(photos):
        text += f"**{row + 1} -** `{photo}`\n"
    await event.edit(text)

@client.Command(command="CleanPhotoList")
async def cleanphotos(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTO_LIST") or {}
    if not photos:
        return await event.edit(client.getstrings(STRINGS)["allempty"])
    client.DB.del_key("PHOTO_LIST")
    await event.edit(client.getstrings(STRINGS)["cleanphoto"])

@client.Inline(pattern="PhotoPage\:(.*)")
async def photopage(event):
    phname = str(event.pattern_match.group(1))
    text = client.getstrings(STRINGS)["photopage"].format(phname)
    buttons = get_buttons(phname)
    await event.answer([event.builder.article("FidoSelf - Photo Page", text=text, buttons=buttons)])

@client.Callback(data="SetPhoto\:(.*)\:(.*)\:(.*)")
async def setphoto(event):
    smode = event.data_match.group(1).decode('utf-8')
    phname = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    if phname not in INPHOTO_LIST:
        return await event.edit(client.getstrings(STRINGS)["saveagain"])
    INPHOTO_LIST[phname][smode] = change 
    lasttext = client.getstrings(STRINGS)["photopage"].format(phname)
    settext = client.getstrings(STRINGS)["setphoto"].format(smode, change)
    text = settext + "\n\n" + lasttext
    buttons = get_buttons(phname)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="SavePhoto\:(.*)")
async def savephoto(event):
    phname = event.data_match.group(1).decode('utf-8')
    photos = client.DB.get_key("PHOTO_LIST") or {}
    if phname not in INPHOTO_LIST:
        return await event.edit(client.getstrings(STRINGS)["saveagain"])
    info = INPHOTO_LIST[phname]
    photos.update({phname: info})
    client.DB.set_key("PHOTO_LIST", photos)
    get = await client.get_messages(info["chat_id"], ids=int(info["msg_id"]))
    await get.download_media(client.PATH + phname)
    text = client.getstrings(STRINGS)["savephoto"].format(phname, info["Where"], info["Size"], info["Color"], info["Align"])
    await event.edit(text=text)
    await photochanger()
    
@client.Callback(data="DelPhoto\:(.*)")
async def delphoto(event):
    phname = event.data_match.group(1).decode('utf-8')
    if phname not in INPHOTO_LIST:
        return await event.edit(client.getstrings(STRINGS)["saveagain"])
    del INPHOTO_LIST[phname]
    text = client.getstrings(STRINGS)["delphoto"].format(phname)
    await event.edit(text=text)