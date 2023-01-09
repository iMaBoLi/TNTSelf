from FidoSelf import client
import time
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetCover$")
async def setcover(event):
    await event.edit(client.get_string("Wait"))
    if not event.is_reply or client.mediatype(event.reply_message) != "photo":
        return await event.edit(client.get_string("Reply_P"))
    if not client.backch:
        return await event.edit(client.get_string("LogCh_1"))
    try:
        forward = await event.reply_message.forward_to(int(client.backch))
    except:
        return await event.edit(client.get_string("LogCh_2"))
    client.DB.set_key("FILE_COVER", {"chat_id": client.backch, "msg_id": forward.id})
    await event.edit(client.get_string("CoverFile_1"))  

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddCover$")
async def addcover(event):
    await event.edit(client.get_string("Wait"))
    if not event.is_reply or client.mediatype(event.reply_message) != "file":
        return await event.edit(client.get_string("Reply_P"))
    if event.reply_message.file.size > client.MAX_SIZE:
        return await event.edit(client.get_string("LargeSize").format(client.utils.convert_bytes(client.MAX_SIZE)))
    cover = client.DB.get_key("FILE_COVER") or {}
    if not cover:
        return await event.edit(client.get_string("CoverFile_2"))
    newtime = time.time()
    file_name = event.reply_message.file.name or "---"
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "down", file_name))
    file = await event.reply_message.download_media(progress_callback=callback)
    await event.edit(client.get_string("CoverFile_3"))
    get = await client.get_messages(int(cover["chat_id"]), ids=int(cover["msg_id"]))
    thumb = await get.download_media()
    newtime = time.time()
    callback = lambda start, end: client.loop.create_task(client.progress(event, start, end, newtime, "up"))
    await client.send_file(event.chat_id, file, thumb=thumb, caption=client.get_string("CoverFile_4"), progress_callback=callback)
    os.remove(file)
    os.remove(thumb)
    await event.delete()
