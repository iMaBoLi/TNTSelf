from TNTSelf import client
from telethon import types
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Extract Audio",
    "Info": {
        "Help": "To Extraxt Audio From Video!",
        "Commands": {
            "{CMD}ExAudio": {
                "Help": "To Exctract Audio",
                "Reply": ["Video"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "exing": "**{STR} Extracting Audio From Video ...**",
    "notaudio": "**{STR} The Video Is Haven't Audio To Extract!**",
    "exaudio": "**{STR} The Audio Was Extracted From Video!**"
}

@client.Command(command="ExAudio")
async def exaudio(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Video"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await client.fast_download(event.reply_message, progress_callback=callback)
    await event.edit(client.getstrings(STRINGS)["exing"])
    vduration = int(event.reply_message.file.duration)
    audiofile = client.PATH + "ExtractAudio.acc"
    cmd = f"ffmpeg -i {video} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {audiofile}"
    await client.functions.runcmd(cmd)
    if not os.path.exists(audiofile):
        return await event.edit(client.getstrings(STRINGS)["notaudio"])
    voicefile = client.PATH + "ExtractAudio.ogg"
    os.rename(audiofile, voicefile)
    attributes = [types.DocumentAttributeAudio(duration=vduration, voice=True)]
    callback = event.progress(upload=True)
    uploadfile = await client.fast_upload(voicefile, progress_callback=callback)
    await client.send_file(event.chat_id, uploadfile, caption=client.getstrings(STRINGS)["exaudio"], attributes=attributes)        
    os.remove(video)
    os.remove(voicefile)
    await event.delete()
