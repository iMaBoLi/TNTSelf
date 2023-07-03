from FidoSelf import client
import os

__INFO__ = {
    "Category": "Private",
    "Plugname": "Timer Save",
    "Pluginfo": {
        "Help": "To Save Timer Medias For You!",
        "Commands": {
            "{CMD}TSave <On-Off>": {
                "Help": "To Turn On-Off Timer Save",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Downlaod Timer Medias Has Been {}!**",
    "caption": "**The Timer Media Was Saved!**\n\n**User:** ( {} )\n**Timer:** ( `{}` )",
}

@client.Command(command="TSave (On|Off)")
async def tsave(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("TIMER_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(onlysudo=False)
async def savemedias(event):
    if not event.is_private or event.is_bot: return
    if not event.file or event.checkReply(["Photo", "Video"]): return
    tmode = client.DB.get_key("TIMER_MODE") or "OFF"
    if tmode == "ON" and hasattr(event.media, "ttl_seconds") and event.media.ttl_seconds:
        if event.file.size > client.MAX_SIZE: return
        file = await event.download_media(client.PATH)
        sender = await event.get_sender()
        mention = client.functions.mention(sender)
        ttl = client.functions.convert_time(event.media.ttl_seconds)
        caption = STRINGS["caption"].format(mention, ttl)
        await client.send_file(client.REALM, file, caption=caption)
        os.remove(file)