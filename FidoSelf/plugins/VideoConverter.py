from FidoSelf import client
from telethon import types
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SV(Note|Normal|Gif)$")
async def videoconverter(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    mtype = client.mediatype(event.reply_message)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    video = await event.reply_message.download_media(progress_callback=callback)
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    if mode == "Normal" and mtype in ["VideoNote", "Gif"]:
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=False, supports_streaming=True)]
        await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
    elif mode == "Note" and mtype in ["Video", "Gif"]:
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=True)]
        await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
    elif mode == "Gif" and mtype in ["VideoNote", "Video"]:
        newfile = video + ".gif"
        os.rename(video, newfile)
        await client.send_file(event.chat_id, newfile, progress_callback=callback)
        os.remove(newfile)
    else:
        medias = client.get_string("ReplyMedia")
        rtype = medias[mtype]
        if mode == "Normal":
            media = medias["Gif"] + " - " + medias["VideoNote"]
        elif mode == "Note":
            media = medias["Video"] + " - " + medias["Gif"]
        elif mode == "Gif":
            media = medias["Video"] + " - " + medias["VideoNote"]
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    os.remove(video)
    await event.delete()
