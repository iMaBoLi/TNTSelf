from FidoSelf import client
from telethon import types
from moviepy.editor import VideoFileClip
import time
import os

@client.Command(pattern=f"(?i)^\{client.cmd}SV(Note|Normal|Gif)$")
async def videoconvert(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    mtype = client.mediatype(event.reply_message)
    if mode == "Normal" and mtype in ["VideoNote", "Gif"]:
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(progress_callback=callback)
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=False, supports_streaming=True)]
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
        os.remove(video)
        await event.delete()
    elif mode == "Note" and mtype in ["Video", "Gif"]:
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(progress_callback=callback)
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=True)]
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
        os.remove(video)
        await event.delete()
    elif mode == "Gif" and mtype in ["VideoNote", "Video"]:
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(progress_callback=callback)
        newfile = video + ".gif"
        videoClip = VideoFileClip(video)
        videoClip.write_gif(newfile)
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, newfile, progress_callback=callback)
        os.remove(newfile)
        os.remove(video)
        await event.delete()
    else:
        medias = client.get_string("ReplyMedia")
        if mode == "Normal":
            media = medias["Gif"] + " - " + medias["VideoNote"]
        elif mode == "Note":
            media = medias["Video"] + " - " + medias["Gif"]
        elif mode == "Gif":
            media = medias["Video"] + " - " + medias["VideoNote"]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        else:      
            return await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
