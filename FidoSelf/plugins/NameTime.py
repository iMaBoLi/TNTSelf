from FidoSelf import client
from .ManageTime import namechanger

__INFO__ = {
    "Category": "Time",
    "Name": "Name Time",
    "Info": {
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
    "change": "**The Name Mode Has Been {}!**",
    "newnot": "**The Name** ( `{}` ) **Already In Name List!**",
    "newadd": "**The Name** ( `{}` ) **Added To Name List!**",
    "delnot": "**The Name** ( `{}` ) **Not In Name List!**",
    "del": "**The Name** ( `{}` ) **Deleted From Name List!**",
    "empty": "**The Name List Is Empty!**",
    "list": "**The Name List:**\n\n",
    "aempty": "**The Name List Is Already Empty!**",
    "clean": "**The Name List Is Cleaned!**",
}

@client.Command(command="Name (On|Off)")
async def namemode(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("NAME_MODE", change)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))
    await namechanger()

@client.Command(command="NewName (.*)")
async def addname(event):
    await event.edit(client.getstrings()["wait"])
    names = client.DB.get_key("NAME_LIST") or []
    newname = str(event.pattern_match.group(1))
    if newname in names:
        return await event.edit(client.getstrings(STRINGS)["newnot"].format(newname))  
    names.append(newname)
    client.DB.set_key("NAME_LIST", names)
    await event.edit(client.getstrings(STRINGS)["newadd"].format(newname))
    await namechanger()
    
@client.Command(command="DelName (.*)")
async def delname(event):
    await event.edit(client.getstrings()["wait"])
    names = client.DB.get_key("NAME_LIST") or []
    newname = str(event.pattern_match.group(1))
    if newname not in names:
        return await event.edit(client.getstrings(STRINGS)["delnot"].format(newname))  
    names.remove(newname)
    client.DB.set_key("NAME_LIST", names)
    await event.edit(client.getstrings(STRINGS)["del"].format(newname))
    await namechanger()

@client.Command(command="NameList")
async def namelist(event):
    await event.edit(client.getstrings()["wait"])
    names = client.DB.get_key("NAME_LIST") or []
    if not names:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for name in names:
        text += f"**{row} -** `{name}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanNameList")
async def cleannames(event):
    await event.edit(client.getstrings()["wait"])
    names = client.DB.get_key("NAME_LIST") or []
    if not names:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("NAME_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])