from FidoSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Logo",
    "Info": {
        "Help": "To Set And Add Logo To Images!",
        "Commands": {
            "{CMD}SetLogo <Reply(Photo)>": None,
            "{CMD}GetLogo <Reply(Photo)>": None,
            "{CMD}AddLogo <Size>-<W>,<H> <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**The Logo Has Been Saved!**",
    "notsave": "**The Logo Is Not Saved!**",
    "getlogo": "**The Logo Image!**",
    "adding": "**Adding Logo To Image ...**",
    "added": "**The Logo Is Added To Your Photo!**",
}

@client.Command(command="SetLogo")
async def setlogo(event):
    await event.edit(client.getstrings()["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Logo.png")
    client.DB.set_key("LOGO_FILE", info)
    await event.edit(client.getstrings(STRINGS)["save"])
    
@client.Command(command="GetLogo")
async def setlogo(event):
    await event.edit(client.getstrings()["wait"])
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    await client.send_file(event.chat_id, logo, force_document=True, allow_cache=True, caption=client.getstrings(STRINGS)["getlogo"])
    await event.delete()

@client.Command(command="AddLogo (\d*)\-(\d*)\,(\d*)")
async def addlogo(event):
    await event.edit(client.getstrings()["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    size = int(event.pattern_match.group(1))
    width = int(event.pattern_match.group(2))
    height = int(event.pattern_match.group(3))
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    photo = await event.reply_message.download_media(client.PATH)
    await event.edit(client.getstrings(STRINGS)["adding"])
    image = Image.open(photo).convert("RGBA")
    pwidth, pheight = image.size
    width = width if width < (pwidth - size) else (pwidth - size)
    height = height if height < (pheight - size) else (pheight - size)
    logimg = Image.open(logo).convert("RGBA")
    logimg.thumbnail((size, size))
    image.paste(logimg, (width, height), logimg)
    newphoto = client.PATH + "AddLogo.png"
    image.save(newphoto)
    await client.send_file(event.chat_id, newphoto, force_document=True, allow_cache=True, caption=client.getstrings(STRINGS)["added"])
    await client.send_file(event.chat_id, newphoto, caption=client.getstrings(STRINGS)["added"])
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()