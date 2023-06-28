from FidoSelf import client
from jdatetime import datetime

__INFO__ = {
    "Category": "Setting",
    "Plugname": "Time",
    "Pluginfo": {
        "Help": "To Get Time And Date!",
        "Commands": {
            "{CMD}Time": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "time": "**Time Info:**\n\n**Time:** ( `{}` )\n**Date:** ( `{}` )\n**Day:** ( `{}` )\n**Month:** ( `{}` )\n",
}

@client.Command(command="Time")
async def time(event):
    await event.edit(client.STRINGS["wait"])
    jtime = datetime.now()
    time = jtime.strftime("%H:%M")
    date = jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d")
    day = jtime.strftime("%A")
    month = jtime.strftime("%B")
    text = STRINGS["time"].format(time, date, day, month)
    await event.edit(text)