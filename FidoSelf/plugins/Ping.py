from FidoSelf import client
from datetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Ping",
    "Pluginfo": {
        "Help": "Return Ping Of Self",
        "Commands": {
            "{CMD}ping": "Get Ping!",
        },
    },
}

STRINGS = {
    "bping": "**!!!**",
    "ping": "**PonG!** [ `{ping}` ]",
}

@client.Command(command="Ping", info=__INFO__)
async def ping(event):
    start = datetime.now()
    await event.edit(STRINGS["bping"])
    end = datetime.now()
    tms = (end - start).microseconds / 10000
    ping = round(tms / 3, 2)
    text = STRINGS["ping"]
    text = text.format(ping=ping)
    await event.edit(text)
