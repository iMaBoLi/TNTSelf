from FidoSelf import client
import image_slicer
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SSlice (\d*)$")
async def sliceimage(event):
    await event.edit(client.get_string("Wait"))
    tile = event.pattern_match.group(1)
    if event.is_reply and event.reply_message.photo:
        photo = await event.reply_message.download_media("SliceImage.jpg")
        tiles = image_slicer.slice(photo, int(tile))
        photos = [str(tile).split(" - ")[1].replace(">", "") for tile in tiles]
        for phs in list(client.utils.chunks(photos, 9)):
            await event.respond(client.get_string("ImageSlicer_1").format(len(photos)), file=phs)
        await event.delete()
        os.remove(photo)
        for ph in photos:
            os.remove(ph)
    else:
        await event.edit(client.get_string("Reply_P"))
