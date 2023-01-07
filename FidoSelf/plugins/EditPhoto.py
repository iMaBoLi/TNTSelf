from FidoSelf import client
from PIL import Image
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE_MORE, EMBOSS, SMOOTH_MORE, SHARPEN
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Bw|Blur|Contour|Detail|Emboss|Edge|Smooth|Sharpen)$")
async def editphoto(event):
    await event.edit(client.get_string("Wait"))
    if not event.is_reply or not event.reply_message.photo:
        return await event.edit(client.get_string("Reply_P"))
    photo = await event.reply_message.download_media()
    mode = event.pattern_match.group(1).title()
    newfile = f"EditImage-{str(mode)}.jpg"
    if mode == "Bw":
        img = Image.open(photo)
        newimg = img.convert("1")
        newimg.save(newfile)
    else:
        modes = {
            "Blur": BLUR,
            "Contour": CONTOUR,
            "Detail": DETAIL,
            "Emboss": EMBOSS,
            "Edge": EDGE_ENHANCE_MORE,
            "Smooth": SMOOTH_MORE,
            "Sharpen": SHARPEN,
        }
        mode = modes[mode]
        img = Image.open(photo)
        newimg = img.filter(mode)
        newimg.save(newfile)
    await event.respond(file=newfile)        
    os.remove(photo)
    os.remove(newfile)
    await event.delete()
