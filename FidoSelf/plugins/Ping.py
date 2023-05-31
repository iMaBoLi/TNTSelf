from FidoSelf import client
from datetime import datetime

STRINGS = {
    "EN": {
        "ping": "**{STR} PonG!** [ `{ping}` ]",
    },
    "FA": {
        "ping": "**{STR} پونگ! [ `{ping}` ]**",
    },
}

@client.Command(
    commands={
        "EN": "Ping",
        "FA": "پینگ",
     }
)
async def ping(event):
    start = datetime.now()
    await event.edit("**!!!**")
    end = datetime.now()
    tms = (end - start).microseconds / 10000
    ping = round(tms / 3, 2)
    text = client.get_string("ping", STRINGS)
    text = text.format(ping=ping)
    await event.edit(text)
