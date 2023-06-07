from FidoSelf import client
from telethon import types
from moviepy.editor import VideoFileClip
import time
import os

@client.Command(command="SV(Note|Normal|Gif)")
async def videoconvert(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    mtype = client.functions.mediatype(event.reply_message)
    if mtype in ["Video", "VideoNote", "Gif"]
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    if mode == "Normal" and mtype in ["VideoNote", "Gif"]:
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=False, supports_streaming=True)]
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
        os.remove(video)
        await event.delete()
    elif mode == "Note" and mtype in ["Video", "Gif"]:
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
        attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=True)]
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
        os.remove(video)
        await event.delete()
    elif mode == "Gif" and mtype in ["VideoNote", "Video"]:
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
        newfile = client.PATH + video + ".gif"
        videoClip = VideoFileClip(video)
        videoClip.write_gif(newfile)
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, newfile, progress_callback=callback)
        os.remove(newfile)
        os.remove(video)
        await event.delete()
    else:
        medias = client.STRINGS["replyMedia"]
        rtype = medias[mtype]
        if mode == "Normal":
            media = medias["Gif"] + " - " + medias["VideoNote"]
        elif mode == "Note":
            media = medias["Video"] + " - " + medias["Gif"]
        elif mode == "Gif":
            media = medias["Video"] + " - " + medias["VideoNote"]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)