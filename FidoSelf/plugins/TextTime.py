from FidoSelf import client

__INFO__ = {
    "Category": "Account",
    "Plugname": "Text Time",
    "Pluginfo": {
        "Help": "To Save Your Texts For Time In Photo!",
        "Commands": {
            "{CMD}NewTtime <Text>": None,
            "{CMD}DelTtime <Text>": None,
            "{CMD}TtimeList": None,
            "{CMD}CleanTtimeList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "newnot": "**The Text Time** ( `{}` ) **Already In Text Time List!**",
    "newadd": "**The Text Time** ( `{}` ) **Added To Text Time List!**",
    "delnot": "**The Text Time** ( `{}` ) **Not In Text Time List!**",
    "del": "**The Text Time** ( `{}` ) **Deleted From Text Time List!**",
    "empty": "**The Text Time List Is Empty!**",
    "list": "**The Text Time List:**\n\n",
    "aempty": "**The Text Time List Is Already Empty!**",
    "clean": "**The Text Time List Is Cleaned!**",
}

@client.Command(command="NewTtime ([\s\S]*)")
async def addttime(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    newttime = str(event.pattern_match.group(1))
    if newttime in ttimes:
        return await event.edit(STRINGS["newnot"].format(newttime))  
    ttimes.append(newttime)
    client.DB.set_key("TEXT_TIMES", ttimes)
    await event.edit(STRINGS["newadd"].format(newttime))
    
@client.Command(command="DelTtime ([\s\S]*)")
async def delttime(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    newttime = str(event.pattern_match.group(1))
    if newttime not in ttimes:
        return await event.edit(STRINGS["delnot"].format(newttime))  
    ttimes.remove(newttime)
    client.DB.set_key("TEXT_TIMES", ttimes)
    await event.edit(STRINGS["del"].format(newttime))

@client.Command(command="TtimeList")
async def ttimelist(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    if not ttimes:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    for row, ttime in enumerate(ttimes):
        text += f"**{row + 1} -** `{ttime}`\n"
    await event.edit(text)

@client.Command(command="CleanTtimeList")
async def cleanttimes(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    if not ttimes:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("TEXT_TIMES")
    await event.edit(STRINGS["clean"])