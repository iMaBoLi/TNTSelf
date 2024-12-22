from TNTSelf import TLclient
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
TLclient.functions.AddInfo(__INFO__)

STRINGS = {
    "ping": "**{STR} PonG !!** ( `{}` )\n**{STR} Uptime:** ( `{}` )",
}

@TLclient.Command(command="Ping")
async def ping(event):
    start = datetime.now()
    await event.edit(TLclient.STRINGS["wait"])
    end = datetime.now()
    tms = (end - start).microseconds / 1000
    ping = round(tms / 3, 2)
    uptime = time.time() - TLclient.START_TIME
    uptime = TLclient.functions.convert_time(uptime)
    await event.edit(TLclient.getstrings(STRINGS)["ping"].format(ping, uptime))