from FidoSelf import client
from PIL import Image

@client.Cmd(pattern=f"(?i)^\{client.cmd}Ssticker$")
async def ssticker(event):
    await event.edit(client.get_string("Wait").format(client.str))
    if event.reply_message and event.reply_message.photo:
        photo = await event.reply_message.download_media()
        img = Image.open(photo)
        img.save("sticker.webp", format="webp")
        await event.respond(file="sticker.webp")        
        os.remove(photo)
        os.remove("sticker.webp")
        return await event.delete()
    await event.edit(f"**{client.str} Please Reply To Photo!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}Sphoto$")
async def sphoto(event):
    await event.edit(client.get_string("Wait").format(client.str))
    if event.reply_message and event.reply_message.sticker:
        sticker = await event.reply_message.download_media()
        img = Image.open(sticker)
        img.save("photo.jpg", format="jpeg")
        await event.respond(file="photo.jpg")        
        os.remove(sticker)
        os.remove("photo.jpg")
        return await event.delete()
    await event.edit(f"**{client.str} Please Reply To Sticker!**")
