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
    "EN": {
        "time": "**{STR} Time:** ( `{}` )\n**{STR} Date:** ( `{}` )\n**{STR} Day:** ( `{}` )\n**{STR} Month:** ( `{}` )\n\n**{STR} Date:** ( `{}` )\n**{STR} Day:** ( `{}` )\n**{STR} Month:** ( `{}` )",
    },
    "FA": {
        "time": "**{STR} ساعت:** ( `{}` )\n**{STR} تاریخ:** ( `{}` )\n**{STR} روز:** ( `{}` )\n**{STR} ماه:** ( `{}` )\n\n**{STR} تاریخ:** ( `{}` )\n**{STR} روز:** ( `{}` )\n**{STR} ماه:** ( `{}` )",
    },
}

@client.Command(command="Time")
async def time(event):
    await event.edit(client.STRINGS["wait"])
    link = "https://www.time.ir/Content/media/image/2024/01/202_orig.jpg"
    taghvim = client.PATH + "TaghVim.jpg"
    with open(taghvim, "wb") as f:
        f.write(requests.get(link).content)
    irtime = jdatetime.datetime.now()
    localtime = datetime.datetime.now()
    text = client.getstring(STRINGS, "time").format(
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