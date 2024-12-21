from TNTSelf import client
from PIL import Image, ImageOps
import os

__INFO__ = {
    "Category": "Convert",
    "Name": "Invert Photo",
    "Info": {
        "Help": "To Invert Colors For Your Photo!",
        "Commands": {
            "{CMD}SInvert": {
                "Help": "To Invert Photo",
                "Reply": ["Photo"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "invert": "**{STR} The Photo Colors Has Been Inverted!**"
}

@client.Command(command="SInvert")
async def invertphoto(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "InvertPhoto.jpg"
    img = Image.open(photo)
    newimg = ImageOps.invert(img)
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=client.getstrings(STRINGS)["invert"])        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()