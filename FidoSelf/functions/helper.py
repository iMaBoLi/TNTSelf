from self import client
import asyncio
import time
import math

async def edit_reply(event, text=None, **kwargs):
    result = await event.edit(text=text, **kwargs)
    if not result:
        result = await event.reply(text=text, **kwargs)
    return result

async def down_media(event, message, **kwargs):
    start = time.time()
    file_name = None
    if message.media:
        file_name = message.media.document.attributes[-1].file_name
    callback = lambda current, total: asyncio.get_event_loop().create_task(progress(event, current, total, start, "down", file_name=file_name))
    return await client.download_media(message, progress_callback=callback, **kwargs)

async def progress(event, current, total, start, type, file_name=None):
    if type == "down":
        type = "Downloading . . ."
    elif type == "up":
        type = "Uploading . . ."
    now = time.time()
    diff = time.time() - start
    if round(diff % 7.00) == 0 or current == total:
        perc = current * 100 / total
        speed = current / diff
        eta = round((total - current) / speed) * 1000
        strs = "".join("●" for i in range(math.floor(perc / 5)))
        text = f"""
`{client.str} {type}`\n\n
`[ {strs} ]{round(perc, 2)}%`\n\n
**{client.str} File Name:** ( `{file_name or "---"}` )\n
**{client.str} Size:** ( `{client.utils.convert_bytes(current)}` **Of** `{client.utils.convert_bytes(total)}` )\n
**{client.str} Speed:** ( `{client.utils.convert_bytes(speed)}` )\n
**{client.str} ETA:** ( `{client.utils.convert_time(eta) or "---"}` )
"""
        await event.edit(text)

def media_type(event):
    if not event:
        return None
    if event.photo:
        return "photo"
    elif event.video and not event.gif and not event.video_note:
        return "video"
    elif event.video and event.gif:
        return "gif"
    elif event.video and event.video_note:
        return "video note"
    elif event.audio:
        return "audio"
    elif event.voice:
        return "voice"
    elif event.sticker and event.sticker.mime_type == "image/webp":
        return "sticker"
    elif event.sticker and event.sticker.mime_type == "application/x-tgsticker":
        return "animated sticker"
    return None

def mention(info):
    if info.username:
        return "@" + info.username
    return f"[{info.first_name}](tg://user?id={info.id})"
