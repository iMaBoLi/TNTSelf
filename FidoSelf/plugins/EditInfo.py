from FidoSelf import client
from telethon import types
import os
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}SDur (\d*)$")
async def setduration(event):
    await event.edit(client.get_string("Wait"))
    dur = int(event.pattern_match.group(1))
    if dur >= 2147483647:
        dur = 2147483647
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video", "Music"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Video"] + " - " + medias["Music"]
        rtype = medias[mtype]
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    file = await event.reply_message.download_media(progress_callback=callback)
    if event.reply_message.audio:
        attributes = [types.DocumentAttributeAudio(duration=dur, title=event.reply_message.file.title, performer=event.reply_message.file.performer)] 
    elif event.reply_message.video:
        attributes = [types.DocumentAttributeVideo(duration=dur, w=event.reply_message.file.width, h=event.reply_message.file.height)]
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    if event.reply_message.audio:
        caption = client.get_string("EditInfo_1").format(client.utils.convert_time(dur))
    elif event.reply_message.video:
        caption = client.get_string("EditInfo_2").format(client.utils.convert_time(dur))
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
        rtype = medias[mtype]
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    audio = await event.reply_message.download_media(progress_callback=callback)
    attributes = [types.DocumentAttributeAudio(duration=event.reply_message.file.duration, title=title, performer=performer)] 
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    caption = client.get_string("EditInfo_3").format(title, performer)
    await client.send_file(event.chat_id, audio, caption=caption, progress_callback=callback, attributes=attributes)        
    os.remove(audio)
    await event.delete()
