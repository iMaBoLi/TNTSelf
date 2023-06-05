from FidoSelf import client
from PIL import Image
import time
import os

@client.Command(command="S(Photo|Sticker)")
async def spconverter(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo", "Sticker"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"] + " - " + medias["Sticker"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if mode == "Photo" and mtype in ["Sticker"]:
        sticker = await event.reply_message.download_media()
        newfile = "StickerToPhoto.jpg"
        img = Image.open(sticker)
        img.save(newfile, format="jpeg")  
        await client.send_file(event.chat_id, newfile)
        os.remove(sticker)
        os.remove(newfile)
        await event.delete()
    elif mode == "Sticker" and mtype in ["Photo"]:
        photo = await event.reply_message.download_media()
        newfile = "PhotoToSticker.webp"
        img = Image.open(photo)
        img.save(newfile, format="webp")  
        await client.send_file(event.chat_id, newfile)
        os.remove(photo)
        os.remove(newfile)
        await event.delete()
    else:
        media = medias["Sticker"] if mode == "Photo" else medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
