from FidoSelf import client
import os

STRINGS = {
    "coning": "**Converting To** ( `{}` ) **...**",
    "caption": "**The Filter** ( `{}` ) **iS Added To Video!**",
}

@client.Command(command="SVideo (Bw|Inv)")
async def editvideo(event):
    await event.edit(client.STRINGS["wait"])
    filter = event.pattern_match.group(1).title()
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Video", "Gif"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Video"] + " - " + medias["Gif"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
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
    elif filter == "Inv":
        cmd = f'ffmpeg -i "{file}" -vf lutyuv="y=negval:u=negval:v=negval" {outfile} -y'
    await client.functions.runcmd(cmd)
    caption = STRINGS["caption"].format(type)
    await client.send_file(event.chat_id, outfile, caption=caption, supports_streaming=True)
    os.remove(file)
    os.remove(outfile)
    await event.delete()
