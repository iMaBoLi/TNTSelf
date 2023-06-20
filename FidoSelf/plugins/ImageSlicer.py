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
    reply, mtype = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
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
