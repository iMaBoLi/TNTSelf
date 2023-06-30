from FidoSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Logo",
    "Pluginfo": {
        "Help": "To Set And Add Logo To Images!",
        "Commands": {
            "{CMD}SetLogo <Reply(Photo)>": None,
            "{CMD}AddLogo <Size>-<W>,<H> <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**The Logo Has Been Saved!**",
    "notsave": "**The Logo Is Not Saved!**",
    "adding": "**Adding Logo To Image ...**",
    "added": "**The Logo Is Added To Your Photo!**",
}

@client.Command(command="SetLogo")
async def setlogo(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Logo.png")
    client.DB.set_key("LOGO_FILE", info)
    await event.edit(STRINGS["save"])  

@client.Command(command="AddLogo (\d*)\-(\d*)\,(\d*)")
async def addlogo(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    size = int(event.pattern_match.group(1))
    width = int(event.pattern_match.group(2))
    height = int(event.pattern_match.group(3))
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(STRINGS["notsave"])
    photo = await event.reply_message.download_media(client.PATH)
    await event.edit(STRINGS["adding"])
    image = Image.open(photo).convert("RGBA")
    logimg = Image.open(logo).convert("RGBA")
    logimg.thumbnail((size, size))
    image.paste(logimg, (width, height), logimg)
    newphoto = client.PATH + "AddLogo.png"
    image.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["added"])
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()