from self import client, START_TIME
import time

@client.Cmd(pattern=f"(?i)^\{client.cmd}ping$")
async def ping(event):
    start = time.time()
    await event.edit(f"**{client.str} Pong‌!!**")
    end = time.time()
    ms = round(((end - start) * 1000), 2)
    uptime = client.utils.convert_time(time.time() - START_TIME)
    await event.edit(f"**{client.str} Ping:** ( `{ms}` )\n**{client.str} Uptime:** ( `{uptime}` )")

@client.Cmd(pattern=f"(?i)^\{client.cmd}bot$")
async def ping(event):
    await event.edit(f"**{client.str}** [I\'m](tg://user?id={client.me.id}) **Never Lose !**")
