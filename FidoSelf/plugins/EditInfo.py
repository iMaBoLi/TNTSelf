from FidoSelf import client
from telethon import types
import os
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}SDur (\d*)$")
async def setduration(event):
    await event.edit(client.get_string("Wait"))
    dur = int(event.pattern_match.group(1))
    if dur > 2147483647: dur = 2147483647
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video", "Music"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Video"] + " - " + medias["Music"]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        else:
            return await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(progress_callback=callback)
    if mtype == "Music":
        attributes = [types.DocumentAttributeAudio(duration=dur, title=event.reply_message.file.title, performer=event.reply_message.file.performer)] 
    elif mtype == "Video":
        attributes = [types.DocumentAttributeVideo(duration=dur, w=event.reply_message.file.width, h=event.reply_message.file.height)]
    if mtype == "Music":
        caption = client.get_string("EditInfo_1").format(client.utils.convert_time(dur))
    elif mtype == "Video":
        caption = client.get_string("EditInfo_2").format(client.utils.convert_time(dur))
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, file, caption=caption, progress_callback=callback, attributes=attributes)        
    os.remove(file)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}SEAudio (.*)\:(.*)$")
async def editaudio(event):
    await event.edit(client.get_string("Wait"))
    title = str(event.pattern_match.group(1))
    performer = str(event.pattern_match.group(2))
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Music"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Music"]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        else:
            return await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    audio = await event.reply_message.download_media(progress_callback=callback)
    attributes = [types.DocumentAttributeAudio(duration=event.reply_message.file.duration, title=title, performer=performer)] 
    caption = client.get_string("EditInfo_3").format(title, performer)
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, audio, caption=caption, progress_callback=callback, attributes=attributes)        
    os.remove(audio)
    await event.delete()
