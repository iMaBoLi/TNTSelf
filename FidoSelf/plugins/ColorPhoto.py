from FidoSelf import client
from PIL import Image, ImageOps
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Color Photo",
    "Pluginfo": {
        "Help": "To Convert Photo And Add Color Filters To Photo!",
        "Commands": {
            "{CMD}SRed <Reply(Photo)>": None,
            "{CMD}SBlue <Reply(Photo)>": None,
            "{CMD}SGreen <Reply(Photo)>": None,
            "{CMD}SYellow <Reply(Photo)>": None,
            "{CMD}SPurple <Reply(Photo)>": None,
            "{CMD}SOrange <Reply(Photo)>": None,
            "{CMD}SPink <Reply(Photo)>": None,
            "{CMD}SGray <Reply(Photo)>": None,
            "{CMD}SGold <Reply(Photo)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "color": "**The Color** ( `{}` ) **Added To Your Photo!**",
}

@client.Command(command="S(Red|Blue|Green|Yellow|Purple|Orange|Pink|Gray|Gold)")
async def colorphoto(event):
    await event.edit(client.STRINGS["wait"])
    color = event.pattern_match.group(1).title()
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + f"ColorPhoto-{str(color)}.jpg"
    img = Image.open(photo).convert("L")
    newimg = ImageOps.colorize(img, black=color.lower(), white="white")
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["color"].format(color))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()