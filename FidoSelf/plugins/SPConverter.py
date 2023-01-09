from FidoSelf import client
from PIL import Image
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Photo|Sticker)$")
async def spconverter(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo", "Sticker"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Photo"] + " - " + medias["Sticker"]
        rtype = medias[mtype]
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    if mode == "Photo" and mtype in ["Sticker"]:
        sticker = await event.reply_message.download_media()
        newfile = "StickerToPhoto.jpg"
        img = Image.open(sticker)
        img.save(newfile, format="jpeg")  
        await client.send_file(event.chat_id, newfile)
        os.remove(sticker)
        os.remove(newfile)
    elif mode == "Sticker" and mtype in ["Photo"]:
        photo = await event.reply_message.download_media()
        newfile = "PhotoToSticker.webp"
        img = Image.open(photo)
        img.save(newfile, format="webp")  
        await client.send_file(event.chat_id, newfile)
        os.remove(photo)
        os.remove(newfile)
    else:
        medias = client.get_string("ReplyMedia")
        media = medias["Sticker"] if mode == "Photo" else medias["Photo"]
        rtype = medias[mtype]
        await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    await event.delete()
