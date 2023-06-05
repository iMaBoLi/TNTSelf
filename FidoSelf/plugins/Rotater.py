from FidoSelf import client
from PIL import Image
import os
import time

STRINGS = {
    "proted": "**The Photo Was Rotated To** ( `{}°` )",
    "vrot": "**Rotating Video To** ( `{}°` ) **...*",
    "vroted": "**The Video Was Rotated To** ( `{}°` )",
}

@client.Command(command="SRotate (\d*)")
async def rotate(event):
    await event.edit(client.STRINGS["wait"])
    darge = int(event.pattern_match.group(1))
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["File", "Music"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["File"] + " - " + medias["Music"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    if mtype == "Photo":
        file = await event.reply_message.download_media()
        newfile = f"RotatedImage-{str(darge)}.jpg"
        img = Image.open(file)
        newimg = img.rotate(darge)
        newimg.save(newfile)
        await event.respond(STRINGS["proted"].format(str(darge)), file=newfile)        
    elif mtype == "Video":
        callback = event.progress(download=True)
        file = await event.reply_message.download_media(progress_callback=callback)
        await event.edit(STRINGS["vrot"].format(str(darge)))
        newfile = f"RotatedVideo-{str(darge)}.mp4"
        cmd = f'ffmpeg -i {file} -vf "rotate={darge}" {newfile}'
        await client.utils.runcmd(cmd)
        newtime = time.time()
        callback = event.progress(upload=True)
        caption = STRINGS["vroted"].format(str(darge))
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(file)
    os.remove(newfile)
    await event.delete()