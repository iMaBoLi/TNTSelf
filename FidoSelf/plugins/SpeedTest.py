from FidoSelf import client
import speedtest
import time

STRINGS = {
    "caption": "**The Speed Test Completed In** ( `{}` )",
}

@client.Command(command="STest")
async def speedt(event):
    await event.edit(client.STRINGS["wait"])
    start = time.time()
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    end = time.time()
    endtime = client.functions.convert_time(end - start)
    caption = STRINGS["caption"].format(endtime)
    await client.send_file(event.chat_id, speed.results.share(), caption=caption)
    await event.delete()