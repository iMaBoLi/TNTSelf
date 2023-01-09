from FidoSelf import client
import os
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}STrim (\d*)\-(\d*)$")
async def trimaudio(event):
    await event.edit(client.get_string("Wait"))
    saudio = int(event.pattern_match.group(1))
    eaudio = int(event.pattern_match.group(2))
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
    if eaudio > event.reply_message.file.duration:
        eaudio = event.reply_message.file.duration
    if saudio >= eaudio:
        saudio = eaudio - 30
    await event.edit(client.get_string("TrimAudio_1").format(saudio, eaudio))
    newfile = f"TrimedAudio-{saudio}-{eaudio}.mp3"
    cmd = f'ffmpeg -i "{audio}" -preset ultrafast -ss {saudio} -to {eaudio} -vn -acodec copy "{newfile}" -y'
    await client.utils.runcmd(cmd)
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    caption = client.get_string("TrimAudio_2").format(saudio, eaudio)
    await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(audio)
    os.remove(newfile)
    await event.delete()
