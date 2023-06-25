from FidoSelf import client
import time

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Timer",
    "Pluginfo": {
        "Help": "To Manage Saved Timers In Self!",
        "Commands": {
            "{CMD}NewTimer <Name>": None,
            "{CMD}DelTimer <Name>": None,
            "{CMD}GetTimer <Name>": None,
            "{CMD}TimerList": None,
            "{CMD}CleanTimerList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**The Timer White Name** ( {} ) **Already In Timer List!**",
    "add": "**The Timer White Name** ( {} ) **Is Added To Timer List!**",
    "notin": "**The Timer White Name** ( {} ) **Is Not In Timer List!**",
    "del": "**The Timer White Name** ( {} ) **Deleted From Timer List!**",
    "get": "**Timer Name:** ( `{}` )\n\n( `{}` )",
    "empty": "**The Timer List Is Empty!**",
    "list": "**The Timer List:**\n\n",
    "aempty": "**The Timer List Is Already Empty**",
    "clean": "**The Timer List Has Been Cleaned!**",
}

def convert_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    result = (
            ((str(days) + " Day, ") if days else "")
            + ((str(hours) + " Hours, ") if hours else "")
            + ((str(minutes) + " Min, ") if minutes else "")
            + ((str(seconds) + " Sec") if seconds else "")
        )
    if result.endswith(":"):
        return result[:-1]
    return result

@client.Command(command="NewTimer (.*)")
async def addtimer(event):
    await event.edit(client.STRINGS["wait"])
    ntimer = event.pattern_match.group(1)
    timers = client.DB.get_key("TIMERS") or {}
    if ntimer in timers:
        return await event.edit(STRINGS["notall"].format(ntimer))
    timers.update({ntimer: time.time()})
    client.DB.set_key("TIMERS", timers)
    await event.edit(STRINGS["add"].format(ntimer))
    
@client.Command(command="DelTimer (.*)")
async def deltimer(event):
    await event.edit(client.STRINGS["wait"])
    ntimer = event.pattern_match.group(1)
    timers = client.DB.get_key("TIMERS") or {}
    if ntimer not in timers:
        return await event.edit(STRINGS["notin"].format(ntimer))  
    del timers[ntimer]
    client.DB.set_key("TIMERS", timers)
    await event.edit(STRINGS["del"].format(ntimer))

@client.Command(command="GetTimer (.*)")
async def gettimer(event):
    await event.edit(client.STRINGS["wait"])
    ntimer = event.pattern_match.group(1)
    timers = client.DB.get_key("TIMERS") or {}
    if ntimer not in timers:
        return await event.edit(STRINGS["notin"].format(ntimer))  
    start = timers[ntimer]
    end = time.time()
    newtimer = convert_time(end - start)
    await event.edit(STRINGS["get"].format(ntimer, newtimer))

@client.Command(command="TimerList")
async def timerlist(event):
    await event.edit(client.STRINGS["wait"])
    timers = client.DB.get_key("TIMERS") or {}
    if not timers:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    for row, timer in enumerate(timers):
        text += f"**{row + 1} -** ( `{timer}` )\n"
    await event.edit(text)

@client.Command(command="CleanTimerList")
async def cleantimerlist(event):
    await event.edit(client.STRINGS["wait"])
    timers = client.DB.get_key("TIMERS") or {}
    if not timers:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("TIMERS")
    await event.edit(STRINGS["clean"])