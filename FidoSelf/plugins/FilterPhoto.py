from FidoSelf import client
from PIL import Image, ImageOps
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE_MORE, EMBOSS, SMOOTH_MORE, SHARPEN
import os

__INFO__ = {
    "Category": "Convert",
    "Name": "Bw Photo",
    "Info": {
        "Help": "To Convert Photo To Black White!",
        "Commands": {
            "{CMD}SPBw": {
                "Help": "To Convert Black White",
                "Reply": ["Photo"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Convert",
    "Name": "Filter Photo",
    "Info": {
        "Help": "To Convert Photo Add Filters To Photo!",
        "Commands": {
            "{CMD}SPBlur": {
                "Help": "To Add Blur Filter",
                "Reply": ["Photo"]
            },
            "{CMD}SPContour": {
                "Help": "To Add Contour Filter",
                "Reply": ["Photo"]
            },
            "{CMD}SPDetail": {
                "Help": "To Add Detail Filter",
                "Reply": ["Photo"]
            },
            "{CMD}SPEmboss": {
                "Help": "To Add Emboss Filter",
                "Reply": ["Photo"]
            },
            "{CMD}SPEdge": {
                "Help": "To Add Edge Filter",
                "Reply": ["Photo"]
            },
            "{CMD}SPSmooth": {
                "Help": "To Add Smooth Filter",
                "Reply": ["Photo"]
            },
            "{CMD}SPSharpen": {
                "Help": "To Add Sharpen Filter",
                "Reply": ["Photo"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "bw": "**{STR} The Photo Converted To Black White!**",
    "filter": "**{STR} The Filter** ( `{}` ) **Added To Your Photo!**"
}

@client.Command(command="SPBw")
async def blackwhite(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "BwPhoto.jpg"
    img = Image.open(photo)
    newimg = ImageOps.grayscale(img)
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=client.getstrings(STRINGS)["bw"])        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()

@client.Command(command="SP(Blur|Contour|Detail|Emboss|Edge|Smooth|Sharpen)")
async def filterphoto(event):
    edit = await event.tryedit(client.STRINGS["wait"])
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
    await client.send_file(event.chat_id, newphoto, caption=client.getstrings(STRINGS)["filter"].format(mode))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()
