from FidoSelf import client
import os

STRINGS = {
    "caption": "**The Filter** ( `{}` ) **iS Added To Gif!**",
}

@client.Command(command="SGif (Bw|Inv)")
async def editgif(event):
    await event.edit(client.STRINGS["wait"])
    filter = event.pattern_match.group(1).title()
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Gif"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Gif"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    callback = event.progress(download=True)
    gif = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    outfile = client.PATH + "EditGif.gif"
    if filter == "Bw":
        cmd = f'ffmpeg -i "{gif}" -vf format=gray {outfile} -y'
        type = "BlackWhite"
    elif filter == "Inv":
        cmd = f'ffmpeg -i "{gif}" -vf lutyuv="y=negval:u=negval:v=negval" {outfile} -y'
        type = "Invert(Negative)"
    await client.functions.runcmd(cmd)
    caption = STRINGS["caption"].format(type)
    await client.send_file(event.chat_id, outfile, caption=caption, supports_streaming=True)
    os.remove(gif)
    os.remove(outfile)
    await event.delete()