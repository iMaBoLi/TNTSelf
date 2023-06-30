from FidoSelf import client
from .ManageTime import photochanger
from telethon import Button
import os

__INFO__ = {
    "Category": "Account",
    "Plugname": "Photo Time",
    "Pluginfo": {
        "Help": "To Save Your Photo For Profile Time And Turn On-Off!",
        "Commands": {
            "{CMD}Photo <On-Off>": None,
            "{CMD}NewPhoto <Name><Reply(Photo)>": "Save Photo White Name!",
            "{CMD}DelPhoto <Name>": "Delete Photo White Name!",
            "{CMD}GetPhoto <Name>": "Get Photo White Name!",
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
}

INPHOTOS = {}

@client.Command(command="Photo (On|Off)")
async def photomode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("PHOTO_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))
    await photochanger()

def get_buttons(phname):
    buttons = []
    photos = INPHOTOS
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
        ocolorbts.append(Button.inline(f"{color} {ShowMode}", data=f"SetPhoto:Color:{phname}:{scolor}"))
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

@client.Command(command="NewPhoto (.*)")
async def addphoto(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    phname = str(event.pattern_match.group(1)) + ".jpg"
    photos = client.DB.get_key("PHOTOS") or {}
    if phname in photos:
        return await event.edit(STRINGS["notall"].format(phname))
    info = await event.reply_message.save()
    INPHOTOS.update({phname: {"chat_id": info["chat_id"], "msg_id": info["msg_id"], "Where": "⏺", "Size": "small", "Color": "Random", "Align": "center", "DO": False}})
    res = await client.inline_query(client.bot.me.username, f"PhotoPage:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()

@client.Command(command="DelPhoto (.*)")
async def delphoto(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(STRINGS["notin"].format(phname))
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    await event.edit(STRINGS["delphoto"].format(phname))
    await photochanger()

@client.Command(command="GetPhoto (.*)")
async def getphoto(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    phname = str(event.pattern_match.group(1))
    if phname not in photos:
        return await event.edit(STRINGS["notin"].format(phname))
    photo = photos[phname]
    fphoto = client.PATH + phname
    caption = STRINGS["getphoto"].format(phname, photo["Where"], photo["Size"], photo["Color"], photo["Align"])
    await event.respond(caption, file=fphoto)
    await event.delete()

@client.Command(command="PhotoList")
async def photolist(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["listphoto"]
    for row, photo in enumerate(photos):
        text += f"**{row + 1} -** `{photo}`\n"
    await event.edit(text)

@client.Command(command="CleanPhotoList")
async def cleanphotos(event):
    await event.edit(client.STRINGS["wait"])
    photos = client.DB.get_key("PHOTOS") or {}
    if not photos:
        return await event.edit(STRINGS["allempty"])
    client.DB.del_key("PHOTOS")
    await event.edit(STRINGS["cleanphoto"])

@client.Inline(pattern="PhotoPage\:(.*)")
async def photopage(event):
    phname = str(event.pattern_match.group(1))
    text = STRINGS["photopage"].format(phname)
    buttons = get_buttons(phname)
    await event.answer([event.builder.article("FidoSelf - Photo Page", text=text, buttons=buttons)])

@client.Callback(data="SetPhoto\:(.*)\:(.*)\:(.*)")
async def setphoto(event):
    smode = event.data_match.group(1).decode('utf-8')
    phname = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    photos = INPHOTOS
    info = photos[phname]
    photos[phname][smode] = change 
    lasttext = STRINGS["photopage"].format(phname)
    settext = STRINGS["setphoto"].format(smode, change)
    text = settext + "\n\n" + lasttext
    buttons = get_buttons(phname)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="SavePhoto\:(.*)")
async def savephoto(event):
    phname = event.data_match.group(1).decode('utf-8')
    photos = client.DB.get_key("PHOTOS") or {}
    info = INPHOTOS[phname]
    photos.update({phname: info})
    client.DB.set_key("PHOTOS", photos)
    get = await client.get_messages(info["chat_id"], ids=int(info["msg_id"]))
    await get.download_media(client.PATH)
    text = STRINGS["savephoto"].format(phname, info["Where"], info["Size"], info["Color"], info["Align"])
    await event.edit(text=text)
    await photochanger()
    
@client.Callback(data="DelPhoto\:(.*)")
async def delphoto(event):
    phname = event.data_match.group(1).decode('utf-8')
    photos = client.DB.get_key("PHOTOS") or {}
    del photos[phname]
    client.DB.set_key("PHOTOS", photos)
    text = STRINGS["delphoto"].format(phname)
    await event.edit(text=text)