from FidoSelf import client
from PIL import Image
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE_MORE, EMBOSS, SMOOTH_MORE, SHARPEN
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Bw|Blur|Contour|Detail|Emboss|Edge|Smooth|Sharpen)$")
async def editphoto(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Photo"]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        return await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
    photo = await event.reply_message.download_media()
    newfile = f"EditPhoto-{str(mode)}.jpg"
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
        pmode = modes[mode]
        img = Image.open(photo)
        newimg = img.filter(pmode)
        newimg.save(newfile)
    mode = "BlackWhite" if mode == "Bw" else mode
    caption = client.get_string("EditPhoto_1").format(mode)
    await client.send_file(event.chat_id, newfile, caption=caption)        
    os.remove(photo)
    os.remove(newfile)
    await event.delete()
