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
            "{CMD}AddLogo <W>,<H> <Reply(Photo)>": None,
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

@client.Command(command="AddLogo (\d*)\,(\d*)")
async def addlogo(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    width = int(event.pattern_match.group(1))
    height = int(event.pattern_match.group(2))
    logo = client.PATH + "Logo.png"
    if not os.path.exists(logo):
        return await event.edit(STRINGS["notsave"])
    photo = await event.reply_message.download_media(client.PATH)
    await event.edit(STRINGS["adding"])
    image = Image.open(photo)
    logimg = Image.open(logo)
    logimg.thumbnail((250, 250))
    image.paste(logimg, (width, height))
    await client.send_file(event.chat_id, photo, caption=STRINGS["added"])
    os.remove(photo)
    await event.delete()