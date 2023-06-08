from FidoSelf import client
from telethon.tl.types import DocumentAttributeVideo
import cv2
import os

STRINGS = {
    "notfind": "**The Cover Photo Is Not Finded!**",
    "coning": "**The Audio Was Converted To Video!**",
}

@client.Command(command="CMusic")
async def circlemusic(event):
    await event.edit(STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Music"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Music"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    audio = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    try:
        cover = await event.reply_message.download_media(thumb=-1)
    except:
        cover = client.PATH + "Cover.png"
        if not os.path.exists(cover):
            return await event.edit(STRINGS["notfind"])
    await event.edit(STRINGS["coning"])
    thumb = client.PATH + "CircleThumb.jpg"
    img = cv2.imread(cover)
    output = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
    cv2.imwrite(thumb, output)
    outfile = client.PATH + "CircleVideo.mp4"
    cmd = f'ffmpeg -i "{thumb}" -i "{audio}" -preset ultrafast -c:a libmp3lame -ab 64 {outfile} -y'
    await client.functions.runcmd(cmd)
    duration = event.reply_message.file.duration
    attributes=[DocumentAttributeVideo(duration=duration, w=512, h=512)]
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, outfile, thumb=thumb, attributes=attributes, progress_callback=callback)
    os.remove(audio)
    os.remove(thumb)
    os.remove(outfile)
    if "Cover.png" not in str(cover):
        os.remove(cover)
    await event.delete()