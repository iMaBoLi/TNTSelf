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
    "change": "**{STR} The Name Mode Has Been {}!**",
    "newnot": "**{STR} The Name** ( `{}` ) **Already In Name List!**",
    "newadd": "**{STR} The Name** ( `{}` ) **Added To Name List!**",
    "delnot": "**{STR} The Name** ( `{}` ) **Not In Name List!**",
    "del": "**{STR} The Name** ( `{}` ) **Deleted From Name List!**",
    "empty": "**{STR} The Name List Is Empty!**",
    "list": "**{STR} The Name List:**\n\n",
    "aempty": "**{STR} The Name List Is Already Empty!**",
    "clean": "**{STR} The Name List Is Cleaned!**"
}

@client.Command(command="Name (On|Off)")
async def namemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("NAME_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))
    await namechanger()

@client.Command(command="NewName (.*)")
async def addname(event):
    await event.edit(client.STRINGS["wait"])
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
    await event.edit(client.STRINGS["wait"])
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
    await event.edit(client.STRINGS["wait"])
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
    await event.edit(client.STRINGS["wait"])
    names = client.DB.get_key("NAME_LIST") or []
    if not names:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("NAME_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])