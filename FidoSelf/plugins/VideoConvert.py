from FidoSelf import client
from telethon import types
import os

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Video",
    "Pluginfo": {
        "Help": "To Convert Video Note To Video!",
        "Commands": {
            "{CMD}SVideo <Reply(VideoNote)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Practical",
    "Plugname": "VideoNote",
    "Pluginfo": {
        "Help": "To Convert Video To Video Note!",
        "Commands": {
            "{CMD}SVNote <Reply(Video)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="SVideo")
async def videoconvert(event):
    await event.edit(client.STRINGS["wait"])
    reply, mtype = event.checkReply(["VideoNote"])
    if reply: return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    videonote = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=False, supports_streaming=True)]
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, videonote, attributes=attributes, progress_callback=callback)
    os.remove(videonote)
    await event.delete()

@client.Command(command="SVNote")
async def videonotecon(event):
    await event.edit(client.STRINGS["wait"])
    reply, mtype = event.checkReply(["Video"])
    if reply: return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    attributes = [types.DocumentAttributeVideo(duration=event.reply_message.file.duration, w=event.reply_message.file.width, h=event.reply_message.file.height, round_message=True)]
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, video, attributes=attributes, progress_callback=callback)
    os.remove(video)
    await event.delete()
    
@client.Command(command="SVGif")
async def videonotecon(event):
    await event.edit(client.STRINGS["wait"])
    reply, mtype = event.checkReply(["Video"])
    if reply: return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    giffile = client.PATH + "VideoGif.gif"
    os.rename(video, giffile)
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, giffile, progress_callback=callback)
    os.remove(giffile)
    await event.delete()