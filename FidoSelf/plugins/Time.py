from FidoSelf import client
import datetime
import jdatetime

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
    irtime = jdatetime.datetime.now()
    localtime = datetime.datetime.now()
    text = STRINGS["time"].format(
        irtime.strftime("%H:%M"),
        irtime.strftime("%Y") + "/" + irtime.strftime("%m") + "/" + irtime.strftime("%d"),
        irtime.strftime("%A"),
        irtime.strftime("%B"),
        localtime.strftime("%H:%M"),
        localtime.strftime("%Y") + "/" + localtime.strftime("%m") + "/" + localtime.strftime("%d"),
        localtime.strftime("%A"),
        localtime.strftime("%B"),
    )
    await event.edit(text)