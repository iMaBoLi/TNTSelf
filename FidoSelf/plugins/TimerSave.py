from FidoSelf import client
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}TSave (On|Off)$")
async def timersave(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("TIMER_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("TimerSave_1").format(change))

@client.Cmd(sudo=False)
async def dtimers(event):
    mode = client.DB.get_key("TIMER_MODE")
    if event.is_private and event.media and event.photo and event.media.to_dict()["_"] == "MessageMediaPhoto" and event.media.ttl_seconds and mode == "on":
        down = await event.download_media(f"{event.sender_id}.jpg")
        mention = client.mention(await event.get_sender())
        await client.send_file(client.realm, down, caption=client.get_string("TimerSave_2").format(mention, client.utils.convert_time(event.media.ttl_seconds)))
        os.remove(down)
    if event.is_private and event.media and event.video and event.media.to_dict()["_"] == "MessageMediaDocument" and event.media.ttl_seconds and mode == "on":
        down = await event.download_media(f"{event.sender_id}.mp4")
        mention = client.mention(await event.get_sender())
        await client.send_file(client.realm, down, caption=client.get_string("TimerSave_3").format(mention, client.utils.convert_time(event.media.ttl_seconds)))
        os.remove(down)
