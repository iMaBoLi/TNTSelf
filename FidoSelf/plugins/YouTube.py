from FidoSelf import client
from telethon import types
import os

STRINGS = {
    "linkinv": "**The Entered Youtube Link Is Invalid!**",
    "downingvid": "**Downloadig Video** ( `{}` ) **...**",
    "downingaud": "**Downloadig Audio** ( `{}` ) **...**",
    "caption": "**Title:** ( `{}` )\n**Uploader:** ( `{}` )\n**Views:** ( `{}` )\n**Duration:** ( `{}` )\n**Description:** ( `{}` )",
}

@client.Command(command="Yt(Video|Music) (.*)")
async def ytdownload(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    link = event.pattern_match.group(2)
    if not client.functions.YOUTUBE_REGEX.search(link):
        return await event.edit(client.STRINGS["linkinv"])
    ytinfo = client.functions.yt_info(link)
    if type == "video":
        await event.edit(STRINGS["downingvid"].format(ytinfo["title"]))
        info = await client.functions.yt_downloader(link, type, "720")
        duration = int(ytinfo["duration"])
        attributes = [types.DocumentAttributeVideo(duration=duration, w=720, h=720, supports_streaming=True)]
    else:
        await event.edit(STRINGS["downingaud"].format(ytinfo["title"]))
        info = await client.functions.yt_downloader(link, type, "320k")
        duration = int(ytinfo["duration"])
        title = ytinfo["title"]
        performer = ytinfo["uploader"]
        attributes = [types.DocumentAttributeAudio(duration=duration, title=title, performer=performer)]
    description = str(ytinfo["description"])[:100]
    caption = STRINGS["caption"].format(ytinfo["title"], ytinfo["uploader"], ytinfo["view_count"], ytinfo["duration_string"], description)
    callback = event.progress(upload=True)
    await client.send_file(
        event.chat_id,
        file=info["OUTFILE"],
        thumb=info["THUMBNAIL"],
        attributes=attributes,
        caption=caption,
        progress_callback=callback,
    )
    os.remove(info["OUTFILE"])
    os.remove(info["THUMBNAIL"])
    await event.delete()