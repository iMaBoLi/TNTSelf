from FidoSelf import client
from shazamio import Shazam

__INFO__ = {
    "Category": "Usage",
    "Name": "Shazam",
    "Info": {
        "Help": "To Recognize Your Musics In Shazam!",
        "Commands": {
            "{CMD}SShazam": {
                "Help": "To Search Shazam",
                "Reply": ["Music", "Video", "Voice"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notfound": "**{STR} The Music Is Not Find In Shazam!**",
    "caption": "**{STR} The Music In Shazam!**\n\n**{STR} Title:** ( `{}` )\n**{STR} Artist:** ( `{}` )",
}

@client.Command(command="SShazam")
async def searchshazam(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Music", "Video", "Voice"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    shazam = Shazam()
    track = await shazam.recognize_song(file)
    if not track["matches"]:
        return await event.edit(client.getstrings(STRINGS)["notfound"])
    title = track["track"]["title"]
    subtitle = track["track"]["subtitle"]
    thumb = track["track"]["images"]["coverarthq"]
    caption = client.getstrings(STRINGS)["caption"].format(title, subtitle)
    await client.send_file(event.chat_id, thumb, caption=caption)
    os.remove(file)
    await event.delete()