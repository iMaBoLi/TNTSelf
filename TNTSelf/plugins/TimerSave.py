from TNTSelf import client
import os

__INFO__ = {
    "Category": "Pv",
    "Name": "Timer Save",
    "Info": {
        "Help": "To Save Timer Medias In Your Pv!",
        "Commands": {
            "{CMD}TSave <On-Off>": {
                "Help": "To Turn On-Off Timer Media Save",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Downlaod Timer Medias Has Been {}!**",
    "caption": "**{STR} The Timer Media Was Saved!**\n\n**User:** ( {} )\n**Timer:** ( `{}` )"
}

@client.Command(command="TSave (On|Off)")
async def tsave(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("TIMER_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(onlysudo=False)
async def timermedias(event):
    if not event.is_private or event.is_sudo or event.is_bot: return
    if not event.media: return
    tmode = event.client.DB.get_key("TIMER_MODE") or "OFF"
    if tmode == "ON" and event.media.to_dict()["_"] != "MessageMediaWebPage" and hasattr(event.media, "ttl_seconds") and event.media.ttl_seconds:
        sender = await event.get_sender()
        mention = client.functions.mention(sender)
        ttl = client.functions.convert_time(event.media.ttl_seconds)
        caption = client.getstrings(STRINGS)["caption"].format(mention, ttl)
        try:
            file = await event.download_media(client.PATH)
            await event.client.send_file(client.REALM, file, caption=caption)
            os.remove(file)
        except:
            pass