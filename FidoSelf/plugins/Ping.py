from FidoSelf import client
from datetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Name": "Ping",
    "Info": {
        "Help": "To Check Bot And Get Ping!",
        "Commands": {
            "{CMD}Ping": {
                "Help": "To Check Self",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "bping": "**!!!**",
    "ping": "**{STR} PonG !!** ( `{}` )"
}

@client.Command(command="Ping")
async def ping(event):
    start = datetime.now()
    await event.edit(client.getstrings(STRINGS)["bping"])
    end = datetime.now()
    tms = (end - start).microseconds / 10000
    ping = round(tms / 3, 2)
    text = client.getstrings(STRINGS)["ping"]
    text = text.format(ping)
    await event.edit(text)