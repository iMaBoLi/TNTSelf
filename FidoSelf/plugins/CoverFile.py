from FidoSelf import client
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetCover$")
async def setcover(event):
    await event.edit(client.get_string("Wait"))
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Photo"]:
        medias = client.get_string("ReplyMedia")
        media = medias["Photo"]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        return await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
    res, info = await event.reply_message.save()
    if not res:
        return await event.edit(info)
    client.DB.set_key("FILE_COVER", info)
    await event.edit(client.get_string("CoverFile_1"))  

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddCover$")
async def addcover(event):
    await event.edit(client.get_string("Wait"))
    mtype = client.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["File", "Music"]:
        medias = client.get_string("ReplyMedia")
        media = medias["File"] + " - " + medias["Music"]
        if mtype == "Empty":
            return await event.edit(client.get_string("ReplyMedia_Not").format(media))
        return await event.edit(client.get_string("ReplyMedia_Main").format(medias[mtype], media))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    cover = client.DB.get_key("FILE_COVER") or {}
    if not cover:
        return await event.edit(client.get_string("CoverFile_2"))
    callback = event.progress(download=True)
    file = await event.reply_message.download_media(progress_callback=callback)
    await event.edit(client.get_string("CoverFile_3"))
    message = await client.get_messages(int(cover["chat_id"]), ids=int(cover["msg_id"]))
    thumb = await message.download_media()
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, file, thumb=thumb, caption=client.get_string("CoverFile_4"), progress_callback=callback)
    os.remove(file)
    os.remove(thumb)
    await event.delete()
