from FidoSelf import client
from telethon import functions, types
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}VShot ((\-)?\d*)$")
async def videoshot(event):
    await event.edit(client.get_string("Wait"))
    data = event.pattern_match.group(1)
    if not event.is_reply or not event.reply_message.video:
        return await event.edit(client.get_string("Reply_V"))
    if str(data).startswith("-"):
        count = int(data.replace("-", ""))
        newtime = time.time()
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down"))
        file = await event.reply_message.download_media(progress_callback=callback)
        duration = event.reply_message.video.attributes[0].duration
        newdur = (duration - 10) / count
        files = []
        lastdur = 5
        for con in range(count):
            out = f"Shot-{con}.jpg"
            cmd = f"ffmpeg -i {file} -ss {lastdur} -vframes 1 {out}"
            await client.utils.runcmd(cmd)
            files.append(out)
            lastdur += newdur
        await client.send_file(event.chat_id, files)
