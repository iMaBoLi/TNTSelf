from FidoSelf import client
import os

__INFO__ = {
    "Category": "Private",
    "Plugname": "Timer Save",
    "Pluginfo": {
        "Help": "To Save Timer Medias For You!",
        "Commands": {
            "{CMD}DTimer <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Downlaod Timer Medias Has Been {}!**",
    "caption": "**The Timer Media Was Saved!**\n\n**User:** ( `{}` )\n**Timer:** ( `{}` )",
}

@client.Command(command="DTimer (On|Off)")
async def dtimermode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("TIMER_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

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