from FidoSelf import client
from PIL import Image

@client.Cmd(pattern=f"(?i)^\{client.cmd}SRotate (\d*)$")
async def ssticker(event):
    await event.edit(client.get_string("Wait"))
    darge = int(event.pattern_match.group(1))
    if event.reply_message and event.reply_message.photo:
        return await event.edit(client.get_string("Reply_P"))
    photo = await event.reply_message.download_media()
    newfile = f"RotatedImage-{str(darge)}.jpg"
    img = Image.open(photo)
    newimg = img.rotate(darge)
    newimg.save(newfile)
    await event.respond(client.get_string("Rotater_1").format(str(darge)), file=newfile)        
    os.remove(photo)
    os.remove(newfile)
    await event.delete()
