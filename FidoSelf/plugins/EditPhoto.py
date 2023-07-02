from FidoSelf import client
from PIL import Image, ImageOps
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE_MORE, EMBOSS, SMOOTH_MORE, SHARPEN
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Bw Photo",
    "Pluginfo": {
        "Help": "To Convert Photo To Black White!",
        "Commands": {
            "{CMD}SBw": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Tools",
    "Plugname": "Filter Photo",
    "Pluginfo": {
        "Help": "To Convert Photo Add Filters To Photo!",
        "Commands": {
            "{CMD}FPhoto Blur": None,
            "{CMD}FPhoto Contour": None,
            "{CMD}FPhoto Detail": None,
            "{CMD}FPhoto Emboss": None,
            "{CMD}FPhoto Edge": None,
            "{CMD}FPhoto Smooth": None,
            "{CMD}FPhoto Sharpen": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Tools",
    "Plugname": "Color Photo",
    "Pluginfo": {
        "Help": "To Convert Photo And Add Color Filters To Photo!",
        "Commands": {
            "{CMD}SRed": None,
            "{CMD}SBlue": None,
            "{CMD}SGreen": None,
            "{CMD}SYellow": None,
            "{CMD}SPurple": None,
            "{CMD}SOrange": None,
            "{CMD}SPink": None,
            "{CMD}SGray": None,
            "{CMD}SGold": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "bw": "**The Photo Converted To Black White!**",
    "filter": "**The Filter** ( `{}` ) **Added To Your Photo!**",
    "color": "**The Color** ( `{}` ) **Added To Your Photo!**",
}

@client.Command(command="SBw")
async def blackwhite(event):
    await event.edit(client.STRINGS["wait"])
    color = event.pattern_match.group(1).title()
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "BwPhoto.jpg"
    img = Image.open(photo)
    newimg = img.convert("1")
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["bw"])        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()

MODES = {
    "Blur": BLUR,
    "Contour": CONTOUR,
    "Detail": DETAIL,
    "Emboss": EMBOSS,
    "Edge": EDGE_ENHANCE_MORE,
    "Smooth": SMOOTH_MORE,
    "Sharpen": SHARPEN,
}
Pattern = ""
for mode in MODES:
    Pattern += mode + "|"
Pattern = Pattern[:-1]

@client.Command(command=f"FPhoto ({Pattern})")
async def filterphoto(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + f"FilterPhoto-{str(mode)}.jpg"
    img = Image.open(photo)
    newimg = img.filter(MODES[mode])
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["filter"].format(mode))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()

@client.Command(command="S(Red|Blue|Green|Yellow|Purple|Orange|Pink|Gray|Gold)")
async def colorphoto(event):
    await event.edit(client.STRINGS["wait"])
    color = event.pattern_match.group(1).title()
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + f"ColorPhoto-{str(color)}.jpg"
    img = Image.open(photo).convert("L")
    newimg = ImageOps.colorize(img, black=color.lower(), white="white")
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["color"].format(color))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()