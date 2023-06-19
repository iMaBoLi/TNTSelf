from FidoSelf import client
from telethon import functions, types
import time
import os

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Video Shot",
    "Pluginfo": {
        "Help": "To Get Screen Shot From Your Videos!",
        "Commands": {
            "{CMD}VShot <Time>": "To Get Shot From a Time!",
            "{CMD}VShot -<Count>": "To Get Shots From Times As Required!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "taking": "**Taking** ( `{}` ) **Screen Shot From Your Video ...**",
    "taked": "**Taked** ( `{}` ) **Screen Shot From Your Video ...**",
    "sending": "**Sending** ( `{}` ) **Screen Shots ...**",
    "sended": "**Taked** ( `{}` ) **Screen Shot From Your Video!**",
    "takingdur": "**Taking Screen Shot From Duration** ( `{}` ) **From Your Video ...**",
    "takeddur": "**Taked Screen Shot From Duration** ( `{}` ) **From Your Video!**",
}

@client.Command(command="VShot ((\-)?\d*)")
async def videoshot(event):
    await event.edit(client.STRINGS["wait"])
    data = event.pattern_match.group(1)
    reply = event.checkReply(["Video"])
    if reply: return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    duration = event.reply_message.file.duration
    if str(data).startswith("-"):
        count = int(data.replace("-", ""))
        newdur = duration / count
        if newdur < 1:
            newdur = 1
            count = duration
        files = []
        lastdur = 0
        await event.edit(STRINGS["taking"].format(count))
        for con in range(count):
            out = client.PATH + f"Shot-{con}.jpg"
            cmd = f"ffmpeg -i {file} -ss {lastdur} -vframes 1 {out}"
            await client.functions.runcmd(cmd)
            files.append(out)
            lastdur += newdur
            if con == 0 or ((con + 1) % 3) == 0:
                await event.edit(STRINGS["taked"].format(con + 1))
        await event.edit(STRINGS["sending"].format(count))
        caption = STRINGS["sended"].format(count)
        for shots in list(client.functions.chunks(files, 9)):
            await client.send_file(event.chat_id, shots, caption=caption)
        os.remove(file)
        for file in files:
            os.remove(file)
        await event.delete()
    else:
        if int(data) > duration:
            data = duration - 1
        await event.edit(STRINGS["takingdur"].format(data))
        out = client.PATH + f"Shot-{data}.jpg"
        cmd = f"ffmpeg -i {file} -ss {int(data)} -vframes 1 {out}"
        await client.functions.runcmd(cmd)
        caption = STRINGS["takeddur"].format(str(data))
        await client.send_file(event.chat_id, out, caption=caption)
        os.remove(file)
        os.remove(out)
        await event.delete()