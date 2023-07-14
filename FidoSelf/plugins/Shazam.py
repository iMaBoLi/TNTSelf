from FidoSelf import client
from shazamio import Shazam

__INFO__ = {
    "Category": "Usage",
    "Name": "Shazam",
    "Info": {
        "Help": "To Recognize Your Musics In Shazam!",
        "Commands": {
            "{CMD}SShazam": {
                "Help": "To Set Duration",
                "Reply": ["Video", "Music", "Voice"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "caption": "**{STR} The Music In Shazam Is Finded!**\n\n**{STR} Title:** ( `{}` )",
}

@client.Command(command="SShazam")
async def searchshazam(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Video", "Music", "Voice"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    shazam = Shazam()
    track = await shazam.recognize_song(file)
    title = track["track"]["share"]["subject"]
    thumb = track["track"]["images"]["background"]
    caption = STRINGS["caption"].format(title)
    await client.send_file(event.chat_id, thumb, caption=caption)
    os.remove(file)
    await event.delete()