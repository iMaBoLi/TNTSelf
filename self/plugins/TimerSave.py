from self import client
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}TSave (On|Off)$")
async def timersave(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("TIMER_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Download Timers Photo adn Video Mode Has Been {change}!**")

@client.Cmd(sudo=False)
async def dtimers(event):
    mode = client.DB.get_key("TIMER_MODE") or "off"
    if event.is_private and event.media and event.photo and event.media.to_dict()["_"] == "MessageMediaPhoto" and event.media.ttl_seconds and mode == "on":
        down = await event.download_media(f"{event.sender_id}.jpg")
        mention = client.mention(await event.get_sender())
        await client.send_file(client.realm, down, caption=f"**{client.str} The Photo Has Been Downloaded!**\n\n**{client.str} User:** ( {mention} )\n**{client.str} Timer:** ( `{client.utils.convert_time(event.media.ttl_seconds)}` )")
        os.remove(down)
    if event.is_private and event.media and event.video and event.media.to_dict()["_"] == "MessageMediaDocument" and event.media.ttl_seconds and mode == "on":
        down = await event.download_media(f"{event.sender_id}.mp4")
        mention = client.mention(await event.get_sender())
        await client.send_file(client.realm, down, caption=f"**{client.str} The Video Has Been Downloaded!**\n\n**{client.str} User:** ( {mention} )\n**{client.str} Timer:** ( `{client.utils.convert_time(event.media.ttl_seconds)}` )")
        os.remove(down)
