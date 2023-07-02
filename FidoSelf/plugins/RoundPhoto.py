from FidoSelf import client
from PIL import Image, ImageDraw
import numpy as np
import os

__INFO__ = {
    "Category": "Funs",
    "Plugname": "Round Photo",
    "Pluginfo": {
        "Help": "To Create Round Sticker For Photo!",
        "Commands": {
            "{CMD}RPhoto <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="RPhoto")
async def roundphoto(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
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
    await client.send_file(event.chat_id, outfile, force_document=False)
    await event.delete()
    os.remove(photo)
    os.remove(outfile)