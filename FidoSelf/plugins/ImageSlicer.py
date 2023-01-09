from FidoSelf import client
import image_slicer
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SSlice (\d*)$")
async def sliceimage(event):
    await event.edit(client.get_string("Wait"))
    tile = event.pattern_match.group(1)
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Photo"]
        rtype = medias[mtype]
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    photo = await event.reply_message.download_media("SliceImage.jpg")
    tiles = image_slicer.slice(photo, int(tile))
    photos = [str(tile).split(" - ")[1].replace(">", "") for tile in tiles]
    for phs in list(client.utils.chunks(photos, 9)):
        await event.respond(client.get_string("ImageSlicer_1").format(len(photos)), file=phs)
    os.remove(photo)
    for ph in photos:
        os.remove(ph)
    await event.delete()
