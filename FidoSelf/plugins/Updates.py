from FidoSelf import client
import os

@client.Cmd(sudo=False)
async def dtimers(event):
    mode = client.DB.get_key("TIMER_MODE")
    mtype = client.mediatype(event)
    if event.is_private and mtype in ["Photo", "Video"] and event.media.ttl_seconds and mode == "on":
        file = await event.download_media()
        sender = await event.get_sender()
        mention = client.mention(sender)
        await client.send_file(client.realm, file, caption=client.get_string("TimerSave_1").format(mention, client.utils.convert_time(event.media.ttl_seconds)))
        os.remove(file)
