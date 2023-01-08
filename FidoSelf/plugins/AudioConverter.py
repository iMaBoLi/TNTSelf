from FidoSelf import client
from telethon import types
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Audio|Voice)$")
async def audioconverter(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    if not event.is_reply or not (event.reply_message.audio or event.reply_message.voice):
        return await event.edit(client.get_string("Reply_AV"))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    audio = await event.reply_message.download_media(progress_callback=callback)
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up", file_name))
    voice = False if mode == "Audio" else True
    await client.send_file(event.chat_id, audio, progress_callback=callback, voice_note=voice)
    os.remove(audio)
    await event.delete()
