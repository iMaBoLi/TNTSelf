from FidoSelf import client
from moviepy.editor import VideoFileClip
import os
import time

@client.Command(pattern=f"(?i)^\{client.cmd}STrim (\d*)\-(\d*)$")
async def trimmedia(event):
    await event.edit(client.get_string("Wait"))
    ss = int(event.pattern_match.group(1))
    ee = int(event.pattern_match.group(2))
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video", "Music"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Video"] + " - " + medias["Music"]
        rtype = medias[mtype]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(progress_callback=callback)
    if ee > event.reply_message.file.duration:
        ee = event.reply_message.file.duration
    if ss >= ee:
        ss = ee - event.reply_message.file.duration 
    if mtype == "Video":
        await event.edit(client.get_string("TrimMedia_1").format(ss, ee))
        newfile = f"TrimedVideo-{ss}-{ee}.mp4"
        clip = VideoFileClip(file).cutout(ss, ee)
        clip.write_videofile(newfile)
        callback = event.progress(upload=True)
        caption = client.get_string("TrimMedia_2").format(ss, ee)
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
        os.remove(newfile)
    elif mtype == "Music":
        await event.edit(client.get_string("TrimMedia_3").format(ss, ee))
        newfile = f"TrimedAudio-{ss}-{ee}.mp3"
        cmd = f'ffmpeg -i "{file}" -preset ultrafast -ss {ss} -to {ee} -vn -acodec copy "{newfile}" -y'
        await client.utils.runcmd(cmd)
        callback = event.progress(upload=True)
        caption = client.get_string("TrimMedia_4").format(ss, ee)
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
        os.remove(newfile)
    os.remove(file)
    await event.delete()
