from TNTSelf import client
from datetime import datetime
import time

__INFO__ = {
    "Category": "Setting",
    "Name": "Ping",
    "Info": {
        "Help": "To Check Bot And Get Ping And Uptime!",
        "Commands": {
            "{CMD}Ping": {
                "Help": "To Check Self And Uptime",
            },
        },
    },
}
#client.functions.AddInfo(__INFO__)

STRINGS = {
    "ping": "**{STR} PonG !!** ( `{}` )\n**{STR} Uptime:** ( `{}` )",
}

@client.Command(command="Ping")
async def ping(event):
    start = datetime.now()
    await event.edit(client.STRINGS["wait"])
    end = datetime.now()
    tms = (end - start).microseconds / 1000
    ping = round(tms / 3, 2)
    uptime = time.time() - client.START_TIME
    uptime = client.functions.convert_time(uptime)
    await event.edit(client.getstrings(STRINGS)["ping"].format(ping, uptime))