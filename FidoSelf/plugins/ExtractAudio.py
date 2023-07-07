from FidoSelf import client
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
    "exing": "**Extracting Audio From Video ...**",
    "exed": "**The Audio Was Extracted From Video!**",
}

@client.Command(command="ExAudio")
async def exaudio(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Video"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    video = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    await event.edit(STRINGS["exing"])
    newfile = client.PATH + f"ExAudio-{video}.acc"
    cmd = f"ffmpeg -i {video} -ab 160k -ac 2 -ar 44100 -vn {newfile}"
    callback = event.progress(upload=True)
    caption = STRINGS["exed"]
    await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(video)
    os.remove(newfile)
    await event.delete()
