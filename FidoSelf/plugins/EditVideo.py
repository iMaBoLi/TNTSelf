from FidoSelf import client
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Edit Video",
    "Pluginfo": {
        "Help": "To Edit Video And Add Filters To Video!",
        "Commands": {
            "{CMD}SVideo Bw": "Add Black White Filter To Video!",
            "{CMD}SVideo Negative": "Add Negative Filter To Video!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "coning": "**Converting To** ( `{}` ) **...**",
    "caption": "**The Filter** ( `{}` ) **iS Added To Video!**",
}

@client.Command(command="SVideo (Bw|Negative)")
async def editvideo(event):
    await event.edit(client.STRINGS["wait"])
    filter = event.pattern_match.group(1).title()
    reply, mtype = event.checkReply(["Video", "Gif"]):
        return await event.edit(reply)
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    type = "BlackWhite" if filter == "Bw" else "Invert(Negative)"
    await event.edit(STRINGS["coning"].format(type))
    if mtype == "Video":
        outfile = client.PATH + "EditVideo.mp4"
    elif mtype == "Gif":
        outfile = client.PATH + "EditGif.gif"
    if filter == "Bw":
        cmd = f'ffmpeg -i "{file}" -vf format=gray {outfile} -y'
    elif filter == "Negative":
        cmd = f'ffmpeg -i "{file}" -vf lutyuv="y=negval:u=negval:v=negval" {outfile} -y'
    await client.functions.runcmd(cmd)
    caption = STRINGS["caption"].format(type)
    await client.send_file(event.chat_id, outfile, caption=caption, supports_streaming=True)
    os.remove(file)
    os.remove(outfile)
    await event.delete()
