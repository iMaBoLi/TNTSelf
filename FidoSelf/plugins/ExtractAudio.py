from FidoSelf import client
import os

STRINGS = {
    "exing": "**Extracting Audio From Video ...**",
    "exed": "**The Audio Was Extracted From Video!**",
}

@client.Command(command="ExAudio")
async def exaudio(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Video"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    await event.edit(STRINGS["exing"])
    newfile = client.PATH + f"ExAudio-{video}.mp3"
    cmd = f"ffmpeg -i '{video}' -map 0:a -codec:a libopus -b:a 100k -vbr on {}"
    callback = event.progress(upload=True)
    caption = STRINGS["exed"]
    await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(video)
    os.remove(newfile)
    await event.delete()
