from FidoSelf import client
from PIL import Image, ImageOps
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE_MORE, EMBOSS, SMOOTH_MORE, SHARPEN
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Bw Photo",
    "Info": {
        "Help": "To Convert Photo To Black White!",
        "Commands": {
            "{CMD}SBw <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Tools",
    "Name": "Filter Photo",
    "Info": {
        "Help": "To Convert Photo Add Filters To Photo!",
        "Commands": {
            "{CMD}SPBlur <Reply(Photo)>": None,
            "{CMD}SPContour <Reply(Photo)>": None,
            "{CMD}SPDetail <Reply(Photo)>": None,
            "{CMD}SPEmboss <Reply(Photo)>": None,
            "{CMD}SPEdge <Reply(Photo)>": None,
            "{CMD}SPSmooth <Reply(Photo)>": None,
            "{CMD}SPSharpen <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "bw": "**The Photo Converted To Black White!**",
    "filter": "**The Filter** ( `{}` ) **Added To Your Photo!**",
}

@client.Command(command="SBw")
async def blackwhite(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "BwPhoto.jpg"
    img = Image.open(photo)
    newimg = ImageOps.grayscale(img)
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["bw"])        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()

@client.Command(command="SP(Blur|Contour|Detail|Emboss|Edge|Smooth|Sharpen)")
async def filterphoto(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + f"FilterPhoto-{str(mode)}.jpg"
    MODES = {
        "Blur": BLUR,
        "Contour": CONTOUR,
        "Detail": DETAIL,
        "Emboss": EMBOSS,
        "Edge": EDGE_ENHANCE_MORE,
        "Smooth": SMOOTH_MORE,
        "Sharpen": SHARPEN,
    }
    img = Image.open(photo)
    newimg = img.filter(MODES[mode])
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["filter"].format(mode))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()
