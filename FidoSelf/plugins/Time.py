from FidoSelf import client
from datetime import datetime
from jdatetime import datetime as jdate

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
    "time": "**Time:** ( `{}` )\n**Date:** ( `{}` )\n**Day:** ( `{}` )\n**Month:** ( `{}` )\n\n**Local Time:**\n**Time:** ( `{}` )\n**Date:** ( `{}` )\n**Day:** ( `{}` )\n**Month:** ( `{}` )\n",
}

@client.Command(command="Time")
async def time(event):
    await event.edit(client.STRINGS["wait"])
    jtime = jdate.now()
    time = jtime.strftime("%H:%M")
    date = jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d")
    day = jtime.strftime("%A")
    month = jtime.strftime("%B")
    time = datetime.now()
    ltime = time.strftime("%H:%M")
    ldate = time.strftime("%Y") + "/" + time.strftime("%m") + "/" + time.strftime("%d")
    lday = time.strftime("%A")
    lmonth = time.strftime("%B")
    text = STRINGS["time"].format(time, date, day, month, ltime, ldate, lday, lmonth)
    await event.edit(text)