from FidoSelf import client

STRINGS = {
    "newnot": "**The Text Time** ( `{}` ) **Already In TextTime List!**",
    "newadd": "**The Text Time** ( `{}` ) **Added To TextTime List!**",
    "delnot": "**The Text Time** ( `{}` ) **Not In TextTime List!**",
    "del": "**The Text Time** ( `{}` ) **Deleted From TextTime List!**",
    "empty": "**The Text Time List Is Empty!**",
    "list": "**The Text Time List:**\n\n",
    "aempty": "**The Text Time List Is Already Empty!**",
    "clean": "**The Text Time List Is Cleaned!**",
}

@client.Command(command="NewTextTime ([\s\S]*)")
async def addttime(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    newttime = str(event.pattern_match.group(1))
    if newttime in ttimes:
        return await event.edit(STRINGS["newnot"].format(newttime))  
    ttimes.append(newttime)
    client.DB.set_key("TEXT_TIMES", ttimes)
    await event.edit(STRINGS["newadd"].format(newttime))
    
@client.Command(command="DelTextTime ([\s\S]*)")
async def delttime(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    newttime = str(event.pattern_match.group(1))
    if newttime not in ttimes:
        return await event.edit(STRINGS["delnot"].format(newttime))  
    ttimes.remove(newttime)
    client.DB.set_key("TEXT_TIMES", ttimes)
    await event.edit(STRINGS["del"].format(newttime))

@client.Command(command="TextTimeList")
async def ttimelist(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    if not ttimes:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for ttime in ttimes:
        text += f"**{row} -** `{ttime}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanTextTimeList")
async def cleanttimes(event):
    await event.edit(client.STRINGS["wait"])
    ttimes = client.DB.get_key("TEXT_TIMES") or []
    if not ttimes:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("TEXT_TIMES")
    await event.edit(STRINGS["clean"])