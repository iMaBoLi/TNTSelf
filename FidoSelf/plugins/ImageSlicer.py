from FidoSelf import client
import image_slicer
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Image Slicer",
    "Pluginfo": {
        "Help": "To Get Slices Images To Tiles!",
        "Commands": {
            "{CMD}Slice <Count>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "slice": "**The Photo Was Sliced To** ( `{}` ) **Tiles!**",
}

@client.Command(command="Slice (\d*)")
async def sliceimage(event):
    await event.edit(client.STRINGS["wait"])
    tile = event.pattern_match.group(1)
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    photo = await event.reply_message.download_media(client.PATH)
    tiles = image_slicer.slice(photo, int(tile))
    photos = [str(tile).split(" - ")[1].replace(">", "") for tile in tiles]
    text = STRINGS["slice"].format(len(photos))
    for phs in list(client.functions.chunks(photos, 9)):
        await event.respond(text, file=phs)
    os.remove(photo)
    for ph in photos:
        os.remove(ph)
    await event.delete()
