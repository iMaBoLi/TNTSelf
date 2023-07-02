from FidoSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Convert Photo",
    "Pluginfo": {
        "Help": "To Convert Your Photo Formats!",
        "Commands": {
            "{CMD}ToPhoto <Reply(Sticker)>": None,
            "{CMD}ToSticker <Reply(Photo)>": None,
            "{CMD}ToJPG <Reply(Photo-PNG)>": None,
            "{CMD}ToPNG <Reply(Photo-JPG)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="ToPhoto")
async def tophoto(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Sticker"]):
        return await event.edit(reply)
    sticker = await event.reply_message.download_media(client.PATH)
    photo = client.PATH + "StickerToPhoto.jpg"
    img = Image.open(sticker)
    img.save(photo, format="jpeg")  
    await client.send_file(event.chat_id, photo)
    os.remove(sticker)
    os.remove(photo)
    await event.delete()

@client.Command(command="ToSticker")
async def tosticker(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    sticker = client.PATH + "PhotoToSticker.webp"
    img = Image.open(photo)
    img.save(sticker, format="webp")  
    await client.send_file(event.chat_id, sticker)
    os.remove(photo)
    os.remove(sticker)
    await event.delete()

@client.Command(command="ToJPG")
async def tojpg(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["PNG Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "PngToJpg.jpg"
    img = Image.open(photo)
    img.save(newphoto, format="jpeg")  
    await client.send_file(event.chat_id, newphoto)
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()
    
@client.Command(command="ToPNG")
async def topng(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["JPG Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + "JpgToPng.png"
    img = Image.open(photo)
    img.save(newphoto, format="png")  
    await client.send_file(event.chat_id, newphoto)
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()