from FidoSelf import client
import time

__INFO__ = {
    "Category": "Manage",
    "Name": "Timer",
    "Info": {
        "Help": "To Manage Saved Timers In Self!",
        "Commands": {
            "{CMD}NewTimer <Name>": {
                "Help": "To Create New Timer",
                "Input": {
                    "<Name>": "Name For Timer",
                },
            },
            "{CMD}DelTimer <Name>": {
                "Help": "To Delete Saved Timer",
                "Input": {
                    "<Name>": "Name For Timer",
                },
            },
            "{CMD}GetTimer <Name>": {
                "Help": "To Getting Saved Timer",
                "Input": {
                    "<Name>": "Name For Timer",
                },
            },
            "{CMD}TimerList": {
                "Help": "To Getting Timer List",
            },
            "{CMD}CleanTimerList": {
                "Help": "To Cleaning Timer List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**{STR} The Timer White Name** ( {} ) **Already In Timer List!**",
    "add": "**{STR} The Timer White Name** ( {} ) **Is Added To Timer List!**",
    "notin": "**{STR} The Timer White Name** ( {} ) **Is Not In Timer List!**",
    "del": "**{STR} The Timer White Name** ( {} ) **Deleted From Timer List!**",
    "get": "**{STR} Timer Name:** ( `{}` )\n\n( `{}` )",
    "empty": "**{STR} The Timer List Is Empty!**",
    "list": "**{STR} The Timer List:**\n\n",
    "aempty": "**{STR} The Timer List Is Already Empty**",
    "clean": "**{STR} The Timer List Has Been Cleaned!**"
}

def convert_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    result = (
            ((str(days) + " Day, ") if days else "")
            + ((str(hours) + " Hour, ") if hours else "")
            + ((str(minutes) + " Minute, ") if minutes else "")
            + ((str(seconds) + " Seconde") if seconds else "")
        )
    if result.endswith(", "):
        return result[:-2]
    return result

@client.Command(command="NewTimer (.*)")
async def addtimer(event):
    await event.edit(client.STRINGS["wait"])
    ntimer = event.pattern_match.group(1)
    timers = client.DB.get_key("TIMER_LIST") or {}
    if ntimer in timers:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(ntimer))
    timers.update({ntimer: time.time()})
    client.DB.set_key("TIMER_LIST", timers)
    await event.edit(client.getstrings(STRINGS)["add"].format(ntimer))
    
@client.Command(command="DelTimer (.*)")
async def deltimer(event):
    await event.edit(client.STRINGS["wait"])
    ntimer = event.pattern_match.group(1)
    timers = client.DB.get_key("TIMER_LIST") or {}
    if ntimer not in timers:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(ntimer))  
    del timers[ntimer]
    client.DB.set_key("TIMER_LIST", timers)
    await event.edit(client.getstrings(STRINGS)["del"].format(ntimer))

@client.Command(command="GetTimer (.*)")
async def gettimer(event):
    await event.edit(client.STRINGS["wait"])
    ntimer = event.pattern_match.group(1)
    timers = client.DB.get_key("TIMER_LIST") or {}
    if ntimer not in timers:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(ntimer))  
    start = timers[ntimer]
    end = time.time()
    newtimer = convert_time(end - start)
    await event.edit(client.getstrings(STRINGS)["get"].format(ntimer, newtimer))

@client.Command(command="TimerList")
async def timerlist(event):
    await event.edit(client.STRINGS["wait"])
    timers = client.DB.get_key("TIMER_LIST") or {}
    if not timers:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, timer in enumerate(timers):
        text += f"**{row + 1} -** `{timer}`\n"
    await event.edit(text)

@client.Command(command="CleanTimerList")
async def cleantimerlist(event):
    await event.edit(client.STRINGS["wait"])
    timers = client.DB.get_key("TIMER_LIST") or {}
    if not timers:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("TIMER_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])