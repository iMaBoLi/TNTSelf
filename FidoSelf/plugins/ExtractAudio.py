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
    "exing": "**{STR} Extracting Audio From Video ...**",
    "exed": "**{STR} The Audio Was Extracted From Video!**"
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
    await event.edit(client.getstrings(STRINGS)["exing"])
    vname = video.split("/")[-1]
    audiofile = client.PATH + f"ExAudio-{vname}.mp3"
    cmd = f"ffmpeg -i {video} -vn -acodec copy {audiofile}"
    await client.functions.runcmd(cmd)
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, audiofile, caption=client.getstrings(STRINGS)["exed"], progress_callback=callback)        
    os.remove(video)
    os.remove(audiofile)
    await event.delete()
