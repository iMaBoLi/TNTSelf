from FidoSelf import client
from PIL import Image, ImageOps
import os

__INFO__ = {
    "Category": "Convert",
    "Name": "Mirror Photo",
    "Info": {
        "Help": "To Mirror Your Photo!",
        "Commands": {
            "{CMD}SMirror <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "mirror": "**The Photo Has Been Mirrored!**",
}

@client.Command(command="SMirror")
async def mirrorphoto(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "MirrorPhoto.jpg"
    img = Image.open(photo)
    newimg = ImageOps.mirror(img)
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["mirror"])        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()