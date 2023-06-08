from FidoSelf import client
from PIL import Image, ImageDraw
import numpy as np
import os

@client.Command(command="RPhoto")
async def roundphoto(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    photo = await event.reply_message.download_media(client.PATH)
    img = Image.open(photo).convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    outfile = client.PATH + "RoundPhoto.webp"
    Image.fromarray(npImage).save(outfile)
    rgimage = PIL.Image.open(path_to_image)
    newimage = rgimage.convert("RGB")
    await client.send_file(event.chat_id, outfile, force_document=False)
    await event.delete()
    os.remove(photo)
    os.remove(outfile)