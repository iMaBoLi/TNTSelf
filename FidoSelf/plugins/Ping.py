from FidoSelf import client
from datetime import datetime
import os

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Ping",
    "Pluginfo": {
        "Help": "Return Ping Of Your Self!",
        "Commands": {
            "{CMD}Ping": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "bping": "**!!!**",
    "ping": "**PonG!!** [ `{ping}` ]",
}

@client.Command(command="Ping")
async def ping(event):
    start = datetime.now()
    await event.edit(STRINGS["bping"])
    end = datetime.now()
    tms = (end - start).microseconds / 10000
    ping = round(tms / 3, 2)
    text = STRINGS["ping"]
    text = text.format(ping=ping)
    await event.edit(text)
    
@client.Command(command="Restart")
async def restart(event):
    await event.edit(client.STRINGS["wait"])
    await event.edit("**• Bot Restarted!**")
    os.system("python3 -m FidoSelf")