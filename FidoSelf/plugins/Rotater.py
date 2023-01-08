from FidoSelf import client
from PIL import Image
import os
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}SRotate (\d*)$")
async def rotate(event):
    await event.edit(client.get_string("Wait"))
    darge = int(event.pattern_match.group(1))
    if event.is_reply and event.reply_message.photo:
        photo = await event.reply_message.download_media()
        newfile = f"RotatedImage-{str(darge)}.jpg"
        img = Image.open(photo)
        newimg = img.rotate(darge)
        newimg.save(newfile)
        await event.respond(client.get_string("Rotater_1").format(str(darge)), file=newfile)        
        os.remove(photo)
        os.remove(newfile)
        await event.delete()
    elif event.is_reply and event.reply_message.video:
        if event.reply_message.file.size > client.MAX_SIZE:
            return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
        newtime = time.time()
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down"))
        video = await event.reply_message.download_media(progress_callback=callback)
        await event.edit(client.get_string("Rotater_2").format(str(darge)))
        newfile = f"RotatedVideo-{str(darge)}.mp4"
        cmd = f'ffmpeg -i {video} -vf "rotate={darge}" {newfile}'
        await client.utils.runcmd(cmd)
        newtime = time.time()
        callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
        caption = client.get_string("Rotater_3").format(str(darge))
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
        os.remove(video)
        os.remove(newfile)
        await event.delete()
    else:
        await event.edit(client.get_string("Reply_PV"))
