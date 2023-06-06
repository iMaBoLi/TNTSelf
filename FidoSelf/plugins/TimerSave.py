from FidoSelf import client
import os

STRINGS = {
    "caption": "**The Timer Media Was Saved!**\n\n**User:** ( `{}` )\n**Timer:** ( `{}` )",
}

@client.Command(onlysudo=False)
async def dtimermedias(event):
    mode = client.DB.get_key("TIMER_MODE")
    mtype = client.functions.mediatype(event)
    if event.is_private and mode == "on" and mtype in ["Photo", "Video"] and event.media.ttl_seconds:
        file = await event.download_media(client.PATH)
        sender = await event.get_sender()
        mention = client.functions.mention(sender)
        ttl = client.functions.convert_time(event.media.ttl_seconds)
        caption = STRINGS["caption"].format(mention, ttl)
        await client.send_file(client.REALM, file, caption=caption)
        os.remove(file)