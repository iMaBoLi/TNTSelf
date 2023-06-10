from FidoSelf import client
from telethon import types
from FidoSelf.functions.youtube import yt_downloader

@client.Command(command="Yt(Video|Music) (.*) (.*)")
async def ytdownload(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    quality = event.pattern_match.group(2)
    link = event.pattern_match.group(3)
    info = await yt_downloader(link, type, quality)
    attributes = [DocumentAttributeVideo(duration=int(info["duration"]), w=720, h=720, supports_streaming=True)]
    media = types.InputMediaUploadedDocument(
        file=inf["OUTFILE"],
        mime_type="video/mp4",
        attributes=attributes,
    )
    callback = event.progress(upload=True)
    await client.send_file(
        event.chat_id,
        file=media,
        thumb=info["THUMBNAIL"],
        progress_callback=callback,
    )