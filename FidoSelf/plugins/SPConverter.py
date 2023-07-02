from FidoSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "To Sticker",
    "Pluginfo": {
        "Help": "To Convert Your Photos To Sticker!",
        "Commands": {
            "{CMD}ToSticker <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="ToSticker")
async def tosticker(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    sticker = client.PATH + "PhotoToSticker.webp"
    img = Image.open(photo)
    img.save(sticker, format="webp")  
    await client.send_file(event.chat_id, sticker)
    os.remove(photo)
    os.remove(sticker)
    await event.delete()