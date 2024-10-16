from TNTSelf import client
import os

__INFO__ = {
    "Category": "Convert",
    "Name": "Filter Video",
    "Info": {
        "Help": "To Convert Video And Add Filters To Video!",
        "Commands": {
            "{CMD}SVBw": None,
            "{CMD}SVNegative": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "coning": "**{STR} Adding** ( `{}` ) **Filter To Video ...**",
    "caption": "**{STR} The Filter** ( `{}` ) **iS Added To Video!**"
}

@client.Command(command="SV(Bw|Negative)")
async def editvideo(event):
    await event.edit(client.STRINGS["wait"])
    vfilter = event.pattern_match.group(1).title()
    if reply:= event.checkReply(["Video"]):
        return await event.edit(reply)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    addfilter = "BlackWhite" if vfilter == "Bw" else "Negative"
    await event.edit(client.getstrings(STRINGS)["coning"].format(addfilter))
    outfile = client.PATH + f"FilterVideo-{str(vfilter)}.mp4"
    if vfilter == "Bw":
        cmd = f'ffmpeg -i "{file}" -vf format=gray {outfile} -y'
    elif vfilter == "Negative":
        cmd = f'ffmpeg -i "{file}" -vf lutyuv="y=negval:u=negval:v=negval" {outfile} -y'
    await client.functions.runcmd(cmd)
    callback = event.progress(upload=True)
    caption = client.getstrings(STRINGS)["caption"].format(addfilter)
    await client.send_file(event.chat_id, outfile, caption=caption, supports_streaming=True, progress_callback=callback)
    os.remove(file)
    os.remove(outfile)
    await event.delete()
