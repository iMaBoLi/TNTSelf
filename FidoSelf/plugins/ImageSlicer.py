from FidoSelf import client
import image_slicer
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SSlice (\d*)$")
async def sliceimage(event):
    await event.edit(f"**{client.str} Processing . . .**")
    tile = event.pattern_match.group(1)
    if event.is_reply and event.reply_message.photo:
        photo = await event.reply_message.download_media("SliceImage.jpg")
        tiles = image_slicer.slice(photo, int(tile))
        photos = [str(tile).split(" - ")[1].replace(">", "") for tile in tiles]
        for phs in list(client.utils.chunks(photos, 9)):
            await event.respond(f"**{client.str} The Photo Was Sliced To** ( `{len(photos)}` ) **Tiles!**", file=phs)
        await event.delete()
        os.remove(photo)
        for ph in photos:
            os.remove(ph)
    else:
        await event.edit(f"**{client.str} Please Reply To Photo!**")
