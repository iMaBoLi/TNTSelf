from FidoSelf import client
import os
import time

__INFO__ = {
    "Category": "Usage",
    "Name": "Trim Video",
    "Info": {
        "Help": "To Trim Your Video Files!",
        "Commands": {
            "{CMD}VTrim <Sec>-<Sec>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Usage",
    "Name": "Trim Audio",
    "Info": {
        "Help": "To Trim Your Music Files!",
        "Commands": {
            "{CMD}ATrim <Sec>-<Sec>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "trvid": "**{STR} Triming Video From** ( `{}` ) **To** ( `{}` ) **...**",
    "trdvid": "**{STR} The Video Was Trimed From** ( `{}` ) **To** ( `{}` )",
    "traud": "**{STR} Triming Audio From** ( `{}` ) **To** ( `{}` ) **...**",
    "trdaud": "**{STR} The Audio Was Trimed From** ( `{}` ) **To** ( `{}` )"
}

@client.Command(command="VTrim (\d*)\-(\d*)")
async def trimvideo(event):
    await event.edit(client.STRINGS["wait"])
    start = int(event.pattern_match.group(1))
    end = int(event.pattern_match.group(2))
    if reply:= event.checkReply(["Video"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    if end > event.reply_message.file.duration:
        end = event.reply_message.file.duration
    if start >= end:
        start = end - event.reply_message.file.duration 
    await event.edit(client.getstrings(STRINGS)["trvid"].format(start, end))
    newfile = client.PATH + f"TrimedVideo-{start}-{end}.mp4"
    cmd = f'ffmpeg -i "{file}" -preset ultrafast -ss {start} -to {end} -codec copy -map 0 "{newfile}" -y'
    await client.functions.runcmd(cmd)
    callback = event.progress(upload=True)
    caption = client.getstrings(STRINGS)["trdvid"].format(start, end)
    await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(newfile)
    os.remove(file)
    await event.delete()
    
@client.Command(command="ATrim (\d*)\-(\d*)")
async def trimaudio(event):
    await event.edit(client.STRINGS["wait"])
    start = int(event.pattern_match.group(1))
    end = int(event.pattern_match.group(2))
    if reply:= event.checkReply(["Music"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    if end > event.reply_message.file.duration:
        end = event.reply_message.file.duration
    if start >= end:
        start = end - event.reply_message.file.duration 
    await event.edit(client.getstrings(STRINGS)["trvid"].format(start, end))
    newfile = client.PATH + f"TrimedAudio-{start}-{end}.mp3"
    cmd = f'ffmpeg -i "{file}" -preset ultrafast -ss {start} -to {end} -vn -acodec copy "{newfile}" -y'
    await client.functions.runcmd(cmd)
    callback = event.progress(upload=True)
    caption = client.getstrings(STRINGS)["trdvid"].format(start, end)
    await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(newfile)
    os.remove(file)
    await event.delete()