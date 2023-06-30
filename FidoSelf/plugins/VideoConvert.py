from FidoSelf import client
from telethon import types
from moviepy.editor import VideoFileClip
import time
import os

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Video Convert",
    "Pluginfo": {
        "Help": "To Convert Your Videos And Gifs!",
        "Commands": {
            "{CMD}SVNormal <Reply(Gif|VNote)>": "Convert To Normal Video!",
            "{CMD}SVGif <Reply(Video|VNote)>": "Convert To Gif!",
            "{CMD}SVNote <Reply(Video|Gif)>": "Convert To Video Note!",
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="SV(Note|Normal|Gif)")
async def videoconvert(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).title()
    reply, mtype = event.checkReply(["Video", "Gif", "VideoNote"])
    if reply: return await event.edit(reply)
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
    elif mode == "Gif" and mtype in ["Video", "VideoNote"]:
        callback = event.progress(download=True)
        video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
        newfile = video + ".gif"
        videoClip = VideoFileClip(video)
        videoClip.write_gif(newfile)
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, newfile, progress_callback=callback)
        os.remove(newfile)
        os.remove(video)
        await event.delete()
    else:
        if mode == "Normal":
            reply = event.checkReply(["Gif", "VideoNote"])
            await event.edit(reply)
        elif mode == "Note":
            reply = event.checkReply(["Video", "Gif"])
            await event.edit(reply)
        elif mode == "Gif":
            reply = event.checkReply(["Video", "VideoNote"])
            await event.edit(reply)