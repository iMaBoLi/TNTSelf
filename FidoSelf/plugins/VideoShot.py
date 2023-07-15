from FidoSelf import client
from telethon import functions, types
import os
import glob

__INFO__ = {
    "Category": "Usage",
    "Name": "Video Shot",
    "Info": {
        "Help": "To Take Screen Shot From Your Videos!",
        "Commands": {
            "{CMD}VShot <Time>": {
                 "Help": "To Take Shot From Time",
                "Input": {
                    "<Time>" : "Time For Take",
                },
                "Reply": ["Video"],
            },
            "{CMD}VShot -<Count>": {
                 "Help": "To Take Multi Shots",
                "Input": {
                    "<Count>" : "Count Of Shots",
                },
                "Reply": ["Video"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "taking": "**{STR} Taking** ( `{}` ) **Screen Shot From Your Video ...**",
    "taked": "**{STR} Taked** ( `{}` ) **Screen Shot From Your Video ...**",
    "sending": "**{STR} Sending** ( `{}` ) **Screen Shots ...**",
    "sended": "**{STR} The Screen Shots From Your Video!**",
    "takingdur": "**{STR} Taking Screen Shot From Duration** ( `{}` ) **Of Your Video ...**",
    "takeddur": "**{STR} The Screen Shot From Your Video!**"
}

@client.Command(command="VShot ((\-)?\d*)")
async def videoshot(event):
    await event.edit(client.STRINGS["wait"])
    data = event.pattern_match.group(1)
    if reply:= event.checkReply(["Video"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await client.fast_download(event.reply_message, progress_callback=callback)
    duration = event.reply_message.file.duration
    if str(data).startswith("-"):
        count = int(data.replace("-", ""))
        await event.edit(client.getstrings(STRINGS)["taking"].format(count))
        cmd = f'ffmpeg -i "{file}" -vf fps=0.009 -vframes {count} "downloads/Shot-%01d.png"'
        await client.functions.runcmd(cmd)
        files = glob.glob("downloads/Shot*.png")
        await event.edit(client.getstrings(STRINGS)["sending"].format(len(files)))
        for shots in list(client.functions.chunks(files, 9)):
            await client.send_file(event.chat_id, shots, caption=client.getstrings(STRINGS)["sended"])
        os.remove(file)
        for file in files:
            os.remove(file)
        await event.delete()
    else:
        if int(data) > duration:
            data = duration - 1
        await event.edit(client.getstrings(STRINGS)["takingdur"].format(data))
        outfile = client.PATH + f"Shot-{data}.jpg"
        cmd = f'ffmpeg -i "{file}" -ss {int(data)} -vframes 1 "{outfile}"'
        await client.functions.runcmd(cmd)
        await client.send_file(event.chat_id, out, caption=client.getstrings(STRINGS)["takeddur"])
        os.remove(file)
        os.remove(outfile)
        await event.delete()