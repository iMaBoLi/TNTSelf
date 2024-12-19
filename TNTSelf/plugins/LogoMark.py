from TNTSelf import client
from telethon import Button
from PIL import Image
import os

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
    "wherelogo": "**{STR} Select Position For Adding Logo To Image:**",
    "adding": "**{STR} Adding Logo To Image ...**",
    "added": "**{STR} The Logo Is Added To Your Photo!**"
}

@client.Command(command="SetLogo")
async def setlogo(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Logo.png")
    client.DB.set_key("LOGO_FILE", info)
    await event.edit(client.getstrings(STRINGS)["save"])
    
@client.Command(command="GetLogo")
async def setlogo(event):
    await event.edit(client.STRINGS["wait"])
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    await client.send_file(event.chat_id, logo, force_document=True, allow_cache=True, caption=client.getstrings(STRINGS)["getlogo"])
    await event.delete()
    
@client.Command(command="AddLogo")
async def addlogo(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    phname = await event.reply_message.download_media(client.PATH)
    res = await client.inline_query(client.bot.me.username, f"AddLogo:{event.chat_id}:{phname}")
    await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    await event.delete()
    
@client.Inline(pattern="AddLogo\\:(.*)\\:(.*)")
async def addlogo(event):
    chatid = event.pattern_match.group(1)
    phname = event.pattern_match.group(2)
    text = client.getstrings(STRINGS)["wherelogo"]
    buttons = []
    for where in ["↖️", "⬆️", "↗️", "⬅️", "⏺", "➡️", "↙️", "⬇️", "↘️"]:
        buttons.append(Button.inline(f"{where}", data=f"FAddLogo:{chatid}:{phname}:{where}"))
    buttons = list(client.functions.chunks(buttons, 3))
    await event.answer([event.builder.article("TNTSelf - Add Logo", text=text, buttons=buttons)])

@client.Callback(data="FAddLogo\\:(.*)\\:(.*)\\:(.*)")
async def faddlogo(event):
    chatid = event.data_match.group(1).decode('utf-8')
    phname = event.data_match.group(2).decode('utf-8')
    where = event.data_match.group(3).decode('utf-8')
    await event.edit(client.getstrings(STRINGS)["adding"])
    image = Image.open(phname).convert("RGBA")
    width, height = image.size
    twidth, theight = round(width / 6), round(height / 6)
    WHERES = {
        "↖️": [1, 1],
        "⬆️": [(width - twidth) / 2, 1],
        "↗️": [(width - twidth) - 1, 1],
        "⬅️": [1, (height - theight) /2],
        "⏺": [(width - twidth) / 2, (height - theight) / 2],
        "➡️": [(width - twidth) - 1, (height - theight) / 2],
        "↙️": [1, (height - theight) - 1],
        "⬇️": [(width - twidth) / 2, (height - theight) - 1],
        "↘️": [(width - twidth) - 1, (height - theight) - 1],
    }
    where = round(WHERES[where][0]), round(WHERES[where][1])
    logo = client.PATH + "Logo.png"
    logimg = Image.open(logo).convert("RGBA")
    logimg.thumbnail((twidth, theight))
    image.paste(logimg, where, logimg)
    newphoto = client.PATH + "AddLogo.png"
    image.save(newphoto)
    caption = client.getstrings(STRINGS)["added"]
    await client.send_file(chatid, newphoto, force_document=True, allow_cache=True, caption=caption)
    await client.send_file(chatid, newphoto, caption=caption)
    os.remove(phname)
    os.remove(newphoto)
    await event.delete()