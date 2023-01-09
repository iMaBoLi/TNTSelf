from FidoSelf import client
from telethon import functions, types
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}VShot ((\-)?\d*)$")
async def videoshot(event):
    await event.edit(client.get_string("Wait"))
    data = event.pattern_match.group(1)
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Video"]
        rtype = medias[mtype]
        return await event.edit(client.get_string("ReplyMedia_Main").format(rtype, media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    file = await event.reply_message.download_media(progress_callback=callback)
    duration = event.reply_message.file.duration
    if str(data).startswith("-"):
        count = int(data.replace("-", ""))
        newdur = duration / count
        if newdur < 1:
            newdur = 1
            count = duration
        files = []
        lastdur = 0
        await event.edit(client.get_string("VideoShot_1").format(count))
        for con in range(count):
            out = f"Shot-{con}.jpg"
            cmd = f"ffmpeg -i {file} -ss {lastdur} -vframes 1 {out}"
            await client.utils.runcmd(cmd)
            files.append(out)
            lastdur += newdur
            if con == 0 or ((con + 1) % 3) == 0:
                await event.edit(client.get_string("VideoShot_2").format(con + 1))
        await event.edit(client.get_string("VideoShot_3").format(count))
        caption = client.get_string("VideoShot_4").format(count)
        for shots in list(client.utils.chunks(files, 9)):
            await client.send_file(event.chat_id, shots, caption=caption)
        os.remove(file)
        for file in files:
            os.remove(file)
        await event.delete()
    else:
        if int(data) > duration:
            data = duration - 1
        await event.edit(client.get_string("VideoShot_5").format(data))
        out = f"Shot-{data}.jpg"
        cmd = f"ffmpeg -i {file} -ss {int(data)} -vframes 1 {out}"
        await client.utils.runcmd(cmd)
        caption = client.get_string("VideoShot_6").format(str(data))
        await client.send_file(event.chat_id, out, caption=caption)
        os.remove(file)
        os.remove(out)
        await event.delete()
