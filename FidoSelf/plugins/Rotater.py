from FidoSelf import client
from PIL import Image
import os

STRINGS = {
    "proted": "**The Photo Was Rotated To** ( `{}°` )",
    "vrot": "**Rotating Video To** ( `{}°` ) **...**",
    "vroted": "**The Video Was Rotated To** ( `{}°` )",
}

@client.Command(command="SRotate (\d*)")
async def rotate(event):
    await event.edit(client.STRINGS["wait"])
    darge = int(event.pattern_match.group(1))
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo", "Video"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"] + " - " + medias["Video"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    if mtype == "Photo":
        file = await event.reply_message.download_media(client.PATH)
        newfile = client.PATH + f"RotatedImage-{str(darge)}.jpg"
        img = Image.open(file)
        newimg = img.rotate(darge)
        newimg.save(newfile)
        await event.respond(STRINGS["proted"].format(str(darge)), file=newfile)        
    elif mtype == "Video":
        callback = event.progress(download=True)
        file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
        await event.edit(STRINGS["vrot"].format(str(darge)))
        newfile = client.PATH + f"RotatedVideo-{str(darge)}.mp4"
        cmd = f'ffmpeg -i {file} -vf "rotate={darge}" {newfile}'
        await client.functions.runcmd(cmd)
        callback = event.progress(upload=True)
        caption = STRINGS["vroted"].format(str(darge))
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(file)
    os.remove(newfile)
    await event.delete()