from FidoSelf import client

__INFO__ = {
    "Category": "Time",
    "Plugname": "Name Time",
    "Pluginfo": {
        "Help": "To Save Your Names For Time In Name And Turn On-Off!",
        "Commands": {
            "{CMD}Name <On-Off>": None,
            "{CMD}NewName <Text>": None,
            "{CMD}DelName <Text>": None,
            "{CMD}NameList": None,
            "{CMD}CleanNameList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "newnot": "**The Name** ( `{}` ) **Already In Name List!**",
    "newadd": "**The Name** ( `{}` ) **Added To Name List!**",
    "delnot": "**The Name** ( `{}` ) **Not In Name List!**",
    "del": "**The Name** ( `{}` ) **Deleted From Name List!**",
    "empty": "**The Name List Is Empty!**",
    "list": "**The Name List:**\n\n",
    "aempty": "**The Name List Is Already Empty!**",
    "clean": "**The Name List Is Cleaned!**",
}

@client.Command(command="NewName (.*)")
async def addname(event):
    await event.edit(client.STRINGS["wait"])
    names = client.DB.get_key("NAMES") or []
    newname = str(event.pattern_match.group(1))
    if newname in names:
        return await event.edit(STRINGS["newnot"].format(newname))  
    names.append(newname)
    client.DB.set_key("NAMES", names)
    await event.edit(STRINGS["newadd"].format(newname))
    
@client.Command(command="DelName (.*)")
async def delname(event):
    await event.edit(client.STRINGS["wait"])
    names = client.DB.get_key("NAMES") or []
    newname = str(event.pattern_match.group(1))
    if newname not in names:
        return await event.edit(STRINGS["delnot"].format(newname))  
    names.remove(newname)
    client.DB.set_key("NAMES", names)
    await event.edit(STRINGS["del"].format(newname))

@client.Command(command="NameList")
async def namelist(event):
    await event.edit(client.STRINGS["wait"])
    names = client.DB.get_key("NAMES") or []
    if not names:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for name in names:
        text += f"**{row} -** `{name}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanNameList")
async def cleannames(event):
    await event.edit(client.STRINGS["wait"])
    names = client.DB.get_key("NAMES") or []
    if not names:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("NAMES")
    await event.edit(STRINGS["clean"])