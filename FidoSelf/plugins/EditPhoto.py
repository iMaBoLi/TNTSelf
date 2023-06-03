from FidoSelf import client
from PIL import Image
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE_MORE, EMBOSS, SMOOTH_MORE, SHARPEN
import os

STRINGS = {
    "add": "**Filter** ( `{}` ) **Successfully Added To Your Photo!**",
}

MODES = {
    "Blur": BLUR,
    "Contour": CONTOUR,
    "Detail": DETAIL,
    "Emboss": EMBOSS,
    "Edge": EDGE_ENHANCE_MORE,
    "Smooth": SMOOTH_MORE,
    "Sharpen": SHARPEN,
}
Pattern = "Bw|"
for mode in MODES:
    Pattern += mode + "|"
Pattern = Pattern[:-1]

@client.Command(command=f"SF({Pattern})")
async def editphoto(event):
    await event.edit(STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    photo = await event.reply_message.download_media()
    newfile = f"EditPhoto-{str(mode)}.jpg"
    if mode == "Bw":
        img = Image.open(photo)
        newimg = img.convert("1")
        newimg.save(newfile)
    else:
        pmode = MODES[mode]
        img = Image.open(photo)
        newimg = img.filter(pmode)
        newimg.save(newfile)
    mode = "BlackWhite" if mode == "Bw" else mode
    caption = STRINGS["add"].format(mode)
    await client.send_file(event.chat_id, newfile, caption=caption)        
    os.remove(photo)
    os.remove(newfile)
    await event.delete()
