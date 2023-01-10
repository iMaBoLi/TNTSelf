from FidoSelf import client
from telethon import types
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Music|Voice)$")
async def audioconverter(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).title()
    mtype = client.mediatype(event.reply_message)
    if mode == "Music" and mtype in ["Voice"]:
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
        callback = event.progress(download=True)
        voice = await event.reply_message.download_media(progress_callback=callback)
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, voice, progress_callback=callback, voice_note=False)
        os.remove(voice)
    elif mode == "Voice" and mtype in ["Music"]:
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
        callback = event.progress(download=True)
        audio = await event.reply_message.download_media(progress_callback=callback)
        callback = event.progress(upload=True)
        await client.send_file(event.chat_id, audio, progress_callback=callback, voice_note=True)
        os.remove(audio)
    else:
        medias = client.get_string("ReplyMedia")
        media = medias["Voice"] if mode == "Music" else medias["Music"]
        if mtype == "Empty":
            await event.edit(client.get_string("ReplyMedia_Not").format(media))
        else: 
            await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
    await event.delete()
