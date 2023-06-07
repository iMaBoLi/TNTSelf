from FidoSelf import client
import os
import time

STRINGS = {
    "trvid": "**Triming Video From** ( `{}` ) **To** ( `{}` ) **...**",
    "trdvid": "**The Video Was Trimed From** ( `{}` ) **To** ( `{}` )",
    "traud": "**Triming Audio From** ( `{}` ) **To** ( `{}` ) **...**",
    "trdaud": "**The Audio Was Trimed From** ( `{}` ) **To** ( `{}` )",
}

@client.Command(command="STrim (\d*)\-(\d*)")
async def trimmedia(event):
    await event.edit(client.STRINGS["wait"])
    ss = int(event.pattern_match.group(1))
    ee = int(event.pattern_match.group(2))
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video", "Music"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Video"] + " - " + medias["Music"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    if ee > event.reply_message.file.duration:
        ee = event.reply_message.file.duration
    if ss >= ee:
        ss = ee - event.reply_message.file.duration 
    if mtype == "Video":
        await event.edit(STRINGS["trvid"].format(ss, ee))
        newfile = client.PATH + f"TrimedVideo-{ss}-{ee}.mp4"
        cmd = f'ffmpeg -i "{file}" -preset ultrafast -ss {ss} -to {ee} -codec copy -map 0 "{newfile}" -y'
        await client.functions.runcmd(cmd)
        callback = event.progress(upload=True)
        caption = STRINGS["trdvid"].format(ss, ee)
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    elif mtype == "Music":
        await event.edit(STRINGS["traud"].format(ss, ee))
        newfile = client.PATH + f"TrimedAudio-{ss}-{ee}.mp3"
        cmd = f'ffmpeg -i "{file}" -preset ultrafast -ss {ss} -to {ee} -vn -acodec copy "{newfile}" -y'
        await client.functions.runcmd(cmd)
        callback = event.progress(upload=True)
        caption = STRINGS["trdaud"].format(ss, ee)
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(newfile)
    os.remove(file)
    await event.delete()
