from FidoSelf import client
import os

@client.Cmd(sudo=False)
async def dtimermedias(event):
    mode = client.DB.get_key("TIMER_MODE")
    mtype = client.mediatype(event)
    if event.is_private and mode == "on" and mtype in ["Photo", "Video"] and event.media.ttl_seconds:
        file = await event.download_media()
        sender = await event.get_sender()
        mention = client.mention(sender)
        ttl = client.utils.convert_time(event.media.ttl_seconds)
        await client.send_file(client.realm, file, caption=client.get_string("TimerSave").format(mention, ttl))
        os.remove(file)
