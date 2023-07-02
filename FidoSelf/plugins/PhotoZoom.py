from FidoSelf import client
from PIL import Image, ImageOps

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Zoom Photo",
    "Pluginfo": {
        "Help": "To Zoom On Photo!",
        "Commands": {
            "{CMD}SZoom <Num>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "zoom": "**The Zoom On Photo In** ( `{}` ) **Border Completed!**",
}

@client.Command(command="SZoom (\d*)")
async def zoomphoto(event):
    await event.edit(client.STRINGS["wait"])
    zoom = int(event.pattern_match.group(1))
    reply, _ = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "ZoomPhoto.jpg"
    img = Image.open(photo)
    newimg = ImageOps.crop(img, border=zoom)
    newimg.save(newphoto)
    await client.send_file(event.chat_id, newphoto, caption=STRINGS["zoom"].format(zoom))        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()