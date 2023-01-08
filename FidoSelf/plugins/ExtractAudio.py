from FidoSelf import client
import os
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}SAudio$")
async def exaudio(event):
    await event.edit(client.get_string("Wait"))
    if not event.is_reply or not event.reply_message.video:
        return await event.edit(client.get_string("Reply_V"))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    video = await event.reply_message.download_media(progress_callback=callback)
    await event.edit(client.get_string("ExAudio_1"))
    newfile = f"EcAudio-{video}.mp3"
    cmd = f'ffmpeg -i {video} -vn -acodec copy {newfile}'
    await client.utils.runcmd(cmd)
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    caption = client.get_string("ExAudio_2")
    await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(video)
    os.remove(newfile)
    await event.delete()
