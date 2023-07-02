from FidoSelf import client
from PIL import Image
import time
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "To Photo",
    "Pluginfo": {
        "Help": "To Convert Stickers To Photo!",
        "Commands": {
            "{CMD}SPhoto <Reply(Sticker)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Tools",
    "Plugname": "To Sticker",
    "Pluginfo": {
        "Help": "To Convert Your Photos To Sticker!",
        "Commands": {
            "{CMD}SSticker <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="S(Photo|Sticker)")
async def spconverter(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    reply, mtype = event.checkReply(["Sticker", "Photo"]):
        return await event.edit(reply)
    if mode == "Photo" and mtype in ["Sticker"]:
        sticker = await event.reply_message.download_media(client.PATH)
        newfile = client.PATH + "StickerToPhoto.jpg"
        img = Image.open(sticker)
        img.save(newfile, format="jpeg")  
        await client.send_file(event.chat_id, newfile)
        os.remove(sticker)
        os.remove(newfile)
        await event.delete()
    elif mode == "Sticker" and mtype in ["Photo"]:
        photo = await event.reply_message.download_media(client.PATH)
        newfile = client.PATH + "PhotoToSticker.webp"
        img = Image.open(photo)
        img.save(newfile, format="webp")  
        await client.send_file(event.chat_id, newfile)
        os.remove(photo)
        os.remove(newfile)
        await event.delete()
    else:
        if mode == "Sticker":
            if reply:= event.checkReply(["Photo"])
            await event.edit(reply)
        elif mode == "Photo":
            if reply:= event.checkReply(["Sticker"])
            await event.edit(reply)
