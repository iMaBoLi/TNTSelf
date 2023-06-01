from FidoSelf import client
import image_slicer
import os

STRINGS = {
    "wait": "**Please Wait ...",
    "slice": "**The Photo Was Sliced To** ( `{}` ) **Tiles!**",
}

@client.Command(command="Slice (\d*)")
async def sliceimage(event):
    await event.edit(STRINGS["wait"])
    tile = event.pattern_match.group(1)
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Photo"]
        rtype = medias[mtype]
        return await event.edit(client.get_string("ReplyMedia")["Main"].format(rtype, media))
    photo = await event.reply_message.download_media("SliceImage.jpg")
    tiles = image_slicer.slice(photo, int(tile))
    photos = [str(tile).split(" - ")[1].replace(">", "") for tile in tiles]
    text = client.get_string("slice", STRINGS)
    for phs in list(client.utils.chunks(photos, 9)):
        await event.respond(text.format(len(photos)), file=phs)
    os.remove(photo)
    for ph in photos:
        os.remove(ph)
    await event.delete
