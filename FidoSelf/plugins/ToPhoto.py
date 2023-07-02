from FidoSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "To Photo",
    "Pluginfo": {
        "Help": "To Convert Stickers To Photo!",
        "Commands": {
            "{CMD}ToPhoto <Reply(Sticker)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="ToPhoto")
async def tophoto(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Sticker"]):
        return await event.edit(reply)
    sticker = await event.reply_message.download_media(client.PATH)
    photo = client.PATH + "StickerToPhoto.jpg"
    img = Image.open(sticker)
    img.save(photo, format="jpeg")  
    await client.send_file(event.chat_id, photo)
    os.remove(sticker)
    os.remove(photo)
    await event.delete()