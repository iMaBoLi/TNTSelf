from TNTSelf import client
import datetime
import jdatetime
import requests
import os

__INFO__ = {
    "Category": "Tools",
    "Name": "Time",
    "Info": {
        "Help": "To Get Time And Date Information!",
        "Commands": {
            "{CMD}Time": {
                "Help": "To Get Full Time",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "time": "**{STR} Time:** ( `{}` )\n**{STR} Date:** ( `{}` )\n**{STR} Day:** ( `{}` )\n**{STR} Month:** ( `{}` )\n\n**{STR} Local:**\n**{STR} Date:** ( `{}` )\n**{STR} Day:** ( `{}` )\n**{STR} Month:** ( `{}` )",
}

@client.Command(command="Time")
async def time(event):
    await event.edit(client.STRINGS["wait"])
    link = "https://www.time.ir/Content/media/image/2024/01/202_orig.jpg"
    taghvim = event.client.PATH + "TaghVim.jpg"
    with open(taghvim, "wb") as f:
        f.write(requests.get(link).content)
    irtime = jdatetime.datetime.now()
    localtime = datetime.datetime.now()
    text = client.getstrings(STRINGS)["time"].format(
        irtime.strftime("%H:%M"),
        irtime.strftime("%Y") + "/" + irtime.strftime("%m") + "/" + irtime.strftime("%d"),
        irtime.strftime("%A"),
        irtime.strftime("%B"),
        localtime.strftime("%Y") + "/" + localtime.strftime("%m") + "/" + localtime.strftime("%d"),
        localtime.strftime("%A"),
        localtime.strftime("%B"),
    )
    await event.respond(text, file=taghvim)
    await event.delete()
    os.remove(taghvim)