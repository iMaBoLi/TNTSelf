from FidoSelf import client
from telethon import functions, types
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}VShot ((\-)?\d*)$")
async def videoshot(event):
    await event.edit(client.get_string("Wait"))
    data = event.pattern_match.group(1)
    if not event.is_reply or not event.reply_message.video:
        return await event.edit(client.get_string("Reply_V"))
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down"))
    file = await event.reply_message.download_media(progress_callback=callback)
    duration = event.reply_message.video.attributes[0].duration
    if str(data).startswith("-"):
        count = int(data.replace("-", ""))
        newdur = duration / count
        files = []
        lastdur = 0
        await event.edit(client.get_string("VideoShot_1").format(count))
        for con in range(count):
            out = f"Shot-{con}.jpg"
            cmd = f"ffmpeg -i {file} -ss {lastdur} -vframes 1 {out}"
            await client.utils.runcmd(cmd)
            files.append(out)
            lastdur += newdur
            await event.edit(client.get_string("VideoShot_2").format(con))
        await event.edit(client.get_string("VideoShot_3").format(count))
        caption = client.get_string("VideoShot_4").format(str(con))
        for shots in list(client.utils.chunks(files, 9)):
            await client.send_file(event.chat_id, shots, caption=caption)
        os.remove(file)
        for file in files:
            os.remove(file)
        await event.delete()
    else:
        if int(data) > duration:
            data = duration
        await event.edit(client.get_string("VideoShot_5").format(data))
        out = f"Shot-{data}.jpg"
        cmd = f"ffmpeg -i {file} -ss {int(data)} -vframes 1 {out}"
        await client.utils.runcmd(cmd)
        caption = client.get_string("VideoShot_6").format(str(data))
        await client.send_file(event.chat_id, out, caption=caption)
        await event.delete()
