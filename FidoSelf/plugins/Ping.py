from FidoSelf import client
from datetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Name": "Ping",
    "Info": {
        "Help": "To Get Ping Of Your Self!",
        "Commands": {
            "{CMD}Ping": {
                "Help": "To Get Ping",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "bping": "**!!!**",
    "ping": "**❁ PonG !!** ( `{ping}` )",
}

@client.Command(command="Ping")
async def ping(event):
    start = datetime.now()
    await event.edit(client.getstrings(STRINGS)["bping"])
    end = datetime.now()
    tms = (end - start).microseconds / 10000
    ping = round(tms / 3, 2)
    text = client.getstrings(STRINGS)["ping"]
    text = text.format(ping=ping)
    await event.edit(text)