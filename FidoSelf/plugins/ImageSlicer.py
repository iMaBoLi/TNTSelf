from FidoSelf import client
import image_slicer

@client.Cmd(pattern=f"(?i)^\{client.cmd}Slice (\d*)$")
async def ssticker(event):
    await event.edit(f"**{client.str} Processing . . .**")
    tile = event.pattern_match.group(1)
    if event.is_reply and event.reply_message.photo:
        photo = await event.reply_message.download_media()
        tiles = image_slicer.slice(photo, int(tile))
        photos = [str(tile).split(" - ")[1].replace(">", "") for tile in tiles]
        for phs in list(client.utils.chunks(photos))
            await event.respond(f"**{client.str} The Photo Was Sliced To** ( `{len(photos)}` ) **Tiles!**")
        return await event.delete()
    await event.edit(f"**{client.str} Please Reply To Photo!**")
