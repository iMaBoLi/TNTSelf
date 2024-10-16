from FidoSelf import client
import time

__INFO__ = {
    "Category": "Manage",
    "Name": "Until",
    "Info": {
        "Help": "To Manage Saved Untils In Self!",
        "Commands": {
            "{CMD}NewUntil <Name>": {
                "Help": "To Create New Until",
                "Input": {
                    "<Name>": "Name For Until",
                },
            },
            "{CMD}DelUntil <Name>": {
                "Help": "To Delete Saved Until",
                "Input": {
                    "<Name>": "Name For Until",
                },
            },
            "{CMD}GetUntil <Name>": {
                "Help": "To Getting Saved Until",
                "Input": {
                    "<Name>": "Name For Until",
                },
            },
            "{CMD}UntilList": {
                "Help": "To Getting Until List",
            },
            "{CMD}CleanUntilList": {
                "Help": "To Cleaning Until List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**{STR} The Until White Name** ( {} ) **Already In Until List!**",
    "full": "**{STR} The Until List Is Full!**",
    "add": "**{STR} The Until White Name** ( {} ) **For** ( `{}` ) **Is Added To Until List!**",
    "notin": "**{STR} The Until White Name** ( {} ) **Is Not In Until List!**",
    "del": "**{STR} The Until White Name** ( {} ) **Deleted From Until List!**",
    "get": "**{STR} Until Name:** ( `{}` )\n\n( `{}` )",
    "empty": "**{STR} The Until List Is Empty!**",
    "list": "**{STR} The Until List:**\n\n",
    "aempty": "**{STR} The Until List Is Already Empty**",
    "clean": "**{STR} The Until List Has Been Cleaned!**"
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

@client.Command(command="NewUntil (.*)\\\:(.*)\\\-(.*)\\\-(.*)")
async def adduntil(event):
    await event.edit(client.STRINGS["wait"])
    nuntil = event.pattern_match.group(1)
    dayuntil = int(event.pattern_match.group(2))
    horuntil = int(event.pattern_match.group(3))
    minuntil = int(event.pattern_match.group(4))
    untils = client.DB.get_key("UNTIL_LIST") or {}
    if len(untils) > 20:
        return await event.edit(client.getstrings(STRINGS)["full"])
    if nuntil in untils:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(nuntil))
    dayuntil = dayuntil * 86400
    horuntil = horuntil * 3600
    minuntil = minuntil * 60
    alluntil = dayuntil + horuntil + minuntil
    newuntil = time.time() + alluntil
    untils.update({nuntil: newuntil})
    client.DB.set_key("UNTIL_LIST", untils)
    await event.edit(client.getstrings(STRINGS)["add"].format(nuntil, convert_time(alluntil)))
    
@client.Command(command="DelUntil (.*)")
async def deluntil(event):
    await event.edit(client.STRINGS["wait"])
    nuntil = event.pattern_match.group(1)
    untils = client.DB.get_key("UNTIL_LIST") or {}
    if nuntil not in untils:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(nuntil))  
    del untils[nuntil]
    client.DB.set_key("UNTIL_LIST", untils)
    await event.edit(client.getstrings(STRINGS)["del"].format(nuntil))

@client.Command(command="GetUntil (.*)")
async def getuntil(event):
    await event.edit(client.STRINGS["wait"])
    nuntil = event.pattern_match.group(1)
    untils = client.DB.get_key("UNTIL_LIST") or {}
    if nuntil not in untils:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(nuntil))  
    start = untils[nuntil]
    end = time.time()
    newuntil = convert_time(start - end)
    await event.edit(client.getstrings(STRINGS)["get"].format(nuntil, newuntil))

@client.Command(command="UntilList")
async def untillist(event):
    await event.edit(client.STRINGS["wait"])
    untils = client.DB.get_key("UNTIL_LIST") or {}
    if not untils:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, until in enumerate(untils):
        start = untils[until]
        end = time.time()
        tuntil = convert_time(start - end)
        text += f"**{row + 1} -** `{until}` -> ( `{tuntil}` )\n\n"
    await event.edit(text)

@client.Command(command="CleanUntilList")
async def cleanuntillist(event):
    await event.edit(client.STRINGS["wait"])
    untils = client.DB.get_key("UNTIL_LIST") or {}
    if not untils:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("UNTIL_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])