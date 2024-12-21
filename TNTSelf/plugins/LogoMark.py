from TNTSelf import client
from telethon import Button
from PIL import Image
import os
import secrets

__INFO__ = {
    "Category": "Tools",
    "Name": "Logo",
    "Info": {
        "Help": "To Setting And Adding Coustom Logo To Images!",
        "Commands": {
            "{CMD}SetLogo": {
                "Help": "To Set Logo",
                "Reply": ["Photo"]
            },
            "{CMD}GetLogo": {
                "Help": "To Get Logo",
            },
            "{CMD}AddLogo": {
                "Help": "To Add Logo To Image",
                "Reply": ["Photo"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**{STR} The Logo Image Has Been Saved!**",
    "notsave": "**{STR} The Logo Image Is Not Saved!**",
    "getlogo": "**{STR} The Logo Image!**",
    "sizelogo": "**{STR} Select Size For Adding Logo To Image:**",
    "wherelogo": "**{STR} Select Position For Adding Logo To Image:**",
    "adding": "**{STR} Adding Logo To Image ...**",
    "added": "**{STR} The Adding Logo To Your Image Completed!**"
}

@client.Command(command="SetLogo")
async def setlogo(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    info = await event.reply_message.save()
    get = await event.client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Logo.png")
    client.DB.set_key("LOGO_FILE", info)
    await event.edit(client.getstrings(STRINGS)["save"])
    
@client.Command(command="GetLogo")
async def setlogo(event):
    await event.edit(client.STRINGS["wait"])
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    await event.client.send_file(event.chat_id, logo, force_document=True, allow_cache=True, caption=client.getstrings(STRINGS)["getlogo"])
    await event.delete()
    
@client.Command(command="AddLogo")
async def addlogo(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    token = secrets.token_hex(nbytes=3)
    phname = client.PATH + token + ".jpg"
    await event.reply_message.download_media(phname)
    res = await event.client.inline_query(client.bot.me.username, f"AddLogo:{event.chat_id}:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()
    
@client.Inline(pattern="AddLogo\\:(.*)\\:(.*)")
async def addlogo(event):
    chatid = event.pattern_match.group(1)
    phname = event.pattern_match.group(2)
    text = client.getstrings(STRINGS)["sizelogo"]
    buttons = []
    for size in ["Very Small", "Small", "Medium", "Big", "Very Big"]:
        ssize = size.replace(" ", "").lower()
        buttons.append(Button.inline(f"• {size} •", data=f"WAddLogo:{chatid}:{phname}:{ssize}"))
    buttons = client.functions.chunker(buttons, [2,1,2])
    await event.answer([event.builder.article("TNTSelf - Add Logo", text=text, buttons=buttons)])

@client.Callback(data="WAddLogo\\:(.*)\\:(.*)\\:(.*)")
async def waddlogo(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    phname = event.data_match.group(2).decode('utf-8')
    size = event.data_match.group(3).decode('utf-8')
    text = client.getstrings(STRINGS)["sizelogo"]
    buttons = []
    for where in ["↖️", "⬆️", "↗️", "⬅️", "⏺", "➡️", "↙️", "⬇️", "↘️"]:
        buttons.append(Button.inline(f"{where}", data=f"FAddLogo:{chatid}:{phname}:{size}:{where}"))
    buttons = list(client.functions.chunks(buttons, 3))
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="FAddLogo\\:(.*)\\:(.*)\\:(.*)\\:(.*)")
async def faddlogo(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    phname = event.data_match.group(2).decode('utf-8')
    size = event.data_match.group(3).decode('utf-8')
    where = event.data_match.group(4).decode('utf-8')
    await event.edit(client.getstrings(STRINGS)["adding"])
    image = Image.open(phname).convert("RGBA")
    width, height = image.size
    logo = client.PATH + "Logo.png"
    logimg = Image.open(logo).convert("RGBA")
    SIZES = {"verysmall":8, "small":6, "medium":5, "big":4, "verybig":2}
    numsize = SIZES[size]
    minsize = min(width, height)
    lwidth, lheight = round(minsize / numsize), round(minsize / numsize)
    logimg = logimg.resize((lwidth, lheight))
    WHERES = {
        "↖️": [5, 5],
        "⬆️": [(width - lwidth) / 2, 5],
        "↗️": [(width - lwidth) - 5, 5],
        "⬅️": [5, (height - lheight) /2],
        "⏺": [(width - lwidth) / 2, (height - lheight) / 2],
        "➡️": [(width - lwidth) - 5, (height - lheight) / 2],
        "↙️": [5, (height - lheight) - 5],
        "⬇️": [(width - lwidth) / 2, (height - lheight) - 5],
        "↘️": [(width - lwidth) - 5, (height - lheight) - 5],
    }
    where = round(WHERES[where][0]), round(WHERES[where][1])
    image.paste(logimg, where, logimg)
    newphoto = client.PATH + "AddLogo.png"
    image.save(newphoto)
    await event.client.send_file(chatid, newphoto)
    await event.client.send_file(chatid, newphoto, force_document=True, allow_cache=True)
    os.remove(phname)
    os.remove(newphoto)
    await event.edit(client.getstrings(STRINGS)["added"])