from FidoSelf import client
import os

STRINGS = {
    "save": "**The Cover Photo For Files Has Been Saved!**",
    "notsave": "**The Cover Photo Is Not Saved!**",
    "adding": "**Adding Cover To Your File ...**",
    "added": "**The Cover Photo Is Added To Your File!**",
}

@client.Command(command="SetCover")
async def setcover(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Photo"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Cover.png")
    client.DB.set_key("FILE_COVER", info)
    await event.edit(STRINGS["save"])  

@client.Command(command="AddCover")
async def addcover(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["File", "Music"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["File"] + " - " + medias["Music"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.STRINGS["LargeSize"].format(client.functions.convert_bytes(client.MAX_SIZE)))
    cover = client.PATH + "Cover.png"
    if not os.path.exists(cover):
        return await event.edit(STRINGS["notsave"])
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(client.PATH, progress_callback=callback)
    await event.edit(STRINGS["adding"])
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, file, thumb=cover, caption=STRINGS["added"], progress_callback=callback)
    os.remove(file)
    await event.delete()