from FidoSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Rotater",
    "Info": {
        "Help": "To Rotate Your Photo And Videos!",
        "Commands": {
            "{CMD}SRotate <Num>": {
                "Help": "To Rotate Video Or Photo",
                "Input": {
                    "<Num>": "Number For Rotate ( 1-360 )",
                },
                "Reply": ["Photo", "Video"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "proted": "**{STR} The Photo Was Rotated To** ( `{}°` )",
    "vrot": "**{STR} Rotating Video To** ( `{}°` ) **...**",
    "vroted": "**{STR} The Video Was Rotated To** ( `{}°` )"
}

@client.Command(command="SRotate (\d*)")
async def rotate(event):
    await event.edit(client.STRINGS["wait"])
    darge = int(event.pattern_match.group(1))
    if reply:= event.checkReply(["Video", "Photo"]):
        return await event.edit(reply)
    mtype = event.reply_message.mediatype()
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    if mtype == "Photo":
        file = await event.reply_message.download_media(client.PATH)
        newfile = client.PATH + f"RotatedImage-{str(darge)}.jpg"
        img = Image.open(file)
        newimg = img.rotate(darge)
        newimg.save(newfile)
        await event.respond(client.getstrings(STRINGS)["proted"].format(str(darge)), file=newfile)        
    elif mtype == "Video":
        callback = event.progress(download=True)
        file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
        await event.edit(client.getstrings(STRINGS)["vrot"].format(str(darge)))
        newfile = client.PATH + f"RotatedVideo-{str(darge)}.mp4"
        cmd = f'ffmpeg -i {file} -vf "rotate={darge}" {newfile}'
        await client.functions.runcmd(cmd)
        callback = event.progress(upload=True)
        caption = client.getstrings(STRINGS)["vroted"].format(str(darge))
        await client.send_file(event.chat_id, newfile, caption=caption, progress_callback=callback)        
    os.remove(file)
    os.remove(newfile)
    await event.delete()