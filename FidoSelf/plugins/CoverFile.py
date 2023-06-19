from FidoSelf import client
import os

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Cover File",
    "Pluginfo": {
        "Help": "To Set And Add Cover To Files!",
        "Commands": {
            "{CMD}SetCover <Reply(Photo)>": "Set Cover Photo!",
            "{CMD}AddCover <Reply(Music|File)>": "Add Cover Photo To File!",
            "{CMD}GetCover <Reply(Music|File)>": "Get Cover Photo From File!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**The Cover Photo For Files Has Been Saved!**",
    "notsave": "**The Cover Photo Is Not Saved!**",
    "adding": "**Adding Cover To Your File ...**",
    "added": "**The Cover Photo Is Added To Your File!**",
    "notcover": "**The File Has No Cover Photo!**",
    "getcover": "**The Cover Photo For File!**",
}

@client.Command(command="SetCover")
async def setcover(event):
    await event.edit(client.STRINGS["wait"])
    reply = event.checkReply(["Photo"])
    if reply: return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "Cover.png")
    client.DB.set_key("FILE_COVER", info)
    await event.edit(STRINGS["save"])  

@client.Command(command="AddCover")
async def addcover(event):
    await event.edit(client.STRINGS["wait"])
    reply = event.checkReply(["File", "Music"])
    if reply: return await event.edit(reply)
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
    
@client.Command(command="GetCover")
async def getcover(event):
    await event.edit(client.STRINGS["wait"])
    reply = event.checkReply(["File", "Music"])
    if reply: return await event.edit(reply)
    if not event.reply_message.document.thumbs:
        return await event.edit(STRINGS["notcover"])
    cover = await event.reply_message.download_media(client.PATH, thumb=-1)
    await event.respond(STRINGS["getcover"], file=cover)
    os.remove(cover)
    await event.delete()