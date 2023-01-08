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
    if not event.is_reply or not event.reply_message.audio:
        return await event.edit(client.get_string("Reply_A"))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    audio = await event.reply_message.download_media(progress_callback=callback)
    attributes = [types.DocumentAttributeAudio(duration=dur)] 
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    caption = client.get_string("EditAudio_1").format(client.utils.convert_time(dur))
    await client.send_file(event.chat_id, audio, caption=caption, progress_callback=callback, attributes=attributes)        
    os.remove(audio)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}SEAudio (.*)\:(.*)$")
async def editaudio(event):
    await event.edit(client.get_string("Wait"))
    title = str(event.pattern_match.group(1))
    performer = str(event.pattern_match.group(2))
    if not event.is_reply or not event.reply_message.audio:
        return await event.edit(client.get_string("Reply_A"))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    audio = await event.reply_message.download_media(progress_callback=callback)
    attributes = [types.DocumentAttributeAudio(title=title, performer=performer)] 
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    caption = client.get_string("EditAudio_2").format(title, performer)
    await client.send_file(event.chat_id, audio, caption=caption, progress_callback=callback, attributes=attributes)        
    os.remove(audio)
    await event.delete()
