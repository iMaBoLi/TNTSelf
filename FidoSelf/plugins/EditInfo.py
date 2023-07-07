from FidoSelf import client
from telethon import types
import music_tag
import os
import time

__INFO__ = {
    "Category": "Usage",
    "Name": "Edit Duration",
    "Info": {
        "Help": "To Edit Duration Of Music And Videos!",
        "Commands": {
            "{CMD}SDuration <Sec> <Reply(Music|Video)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Usage",
    "Name": "Music Info",
    "Info": {
        "Help": "To Edit Title And Performer For Music!",
        "Commands": {
            "{CMD}SMusic <Title>:<Name>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "adur": "**The Duration Of This Audio Was Changed To** ( `{}` )",
    "vdur": "**The Duration Of This Video Was Changed To** ( `{}` )",
    "atilper": "**The Title And Performer Of This Audio Was Changed To** ( `{}` ) **And** ( `{}` )"
}

@client.Command(command="SDuration (\d*)")
async def setduration(event):
    await event.edit(client.STRINGS["wait"])
    dur = int(event.pattern_match.group(1))
    if dur > 2147483647: dur = 2147483647
    if reply:= event.checkReply(["Video", "Music"]):
        return await event.edit(reply)
    mtype = event.reply_message.mediatype()
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(progress_callback=callback)
    if mtype == "Music":
        attributes = [types.DocumentAttributeAudio(duration=dur, title=event.reply_message.file.title, performer=event.reply_message.file.performer)] 
    elif mtype == "Video":
        attributes = [types.DocumentAttributeVideo(duration=dur, w=event.reply_message.file.width, h=event.reply_message.file.height)]
    caption = STRINGS["adur"] if mtype == "Music" else STRINGS["adur"]
    caption = caption.format(client.functions.convert_time(dur))
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, file, caption=caption, progress_callback=callback, attributes=attributes)        
    os.remove(file)
    await event.delete()

@client.Command(command="SMusic (.*)\:(.*)")
async def editaudio(event):
    await event.edit(client.STRINGS["wait"])
    performer = str(event.pattern_match.group(1))
    title = str(event.pattern_match.group(2))
    if reply:= event.checkReply(["Music"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    audio = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    load = music_tag.load_file(audio)
    load["artist"] = performer
    load["albumartist"] = performer
    load["tracktitle"] = title
    load["album"] = title
    newfile = client.PATH + performer + "-" + title + ".mp3"
    load.save(newfile)
    thumb = None
    if event.reply_message.document.thumbs:
        thumb = await event.reply_message.download_media(thumb=-1)
        #load["artwork"] == open(thumb, "rb").read()
    attributes = [types.DocumentAttributeAudio(duration=event.reply_message.file.duration, title=title, performer=performer)] 
    caption = STRINGS["atilper"].format(performer, title)
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, newfile, caption=caption, thumb=thumb, progress_callback=callback, attributes=attributes)        
    os.remove(audio)
    os.remove(newfile)
    if thumb:
        os.remove(thumb)
    await event.delete()