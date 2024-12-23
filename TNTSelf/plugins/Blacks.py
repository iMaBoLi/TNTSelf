from TNTSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Black",
    "Info": {
        "Help": "To Manage Users On Black List!",
        "Commands": {
            "{CMD}AddBlack": {
                "Help": "To Add User On Black List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelBlack": {
                "Help": "To Delete User From Black List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}BlackList": {
                "Help": "To Getting Black List",
           },
            "{CMD}CleanBlackList": {
                "Help": "To Cleaning Black List",
           },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**{STR} The User** ( {} ) **Already In Black List!**",
    "add": "**{STR} The User** ( {} ) **Is Added To Black List!**",
    "notin": "**{STR} The User** ( {} ) **Is Not In Black List!**",
    "del": "**{STR} The User** ( {} ) **Deleted From Black List!**",
    "empty": "**{STR} The Black List Is Empty!**",
    "list": "**{STR} The Black List:**\n\n",
    "aempty": "**{STR} The Black List Is Already Empty**",
    "clean": "**{STR} The Black List Has Been Cleaned!**"
}

@client.Command(command="AddBlack", userid=True)
async def addblack(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    blacks = event.client.DB.get_key("BLACK_LIST") or []
    info = await event.client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid in blacks:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    blacks.append(event.userid)
    event.client.DB.set_key("BLACK_LIST", blacks)
    whites = event.client.DB.get_key("WHITE_LIST") or []
    if event.userid in whites:
        whites.remove(event.userid)
        event.client.DB.set_key("WHITE_LIST", whites)
    await event.edit(client.getstrings(STRINGS)["add"].format(mention))
    
@client.Command(command="DelBlack", userid=True)
async def delblack(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    blacks = event.client.DB.get_key("BLACK_LIST") or []
    info = await event.client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid not in blacks:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))  
    blacks.remove(event.userid)
    event.client.DB.set_key("BLACK_LIST", blacks)
    await event.edit(client.getstrings(STRINGS)["del"].format(mention))
    
@client.Command(command="BlackList")
async def blacklist(event):
    await event.edit(client.STRINGS["wait"])
    blacks = event.client.DB.get_key("BLACK_LIST") or []
    if not blacks:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, black in enumerate(blacks):
        text += f"**{row + 1} -** `{black}`\n"
    await event.edit(text)

@client.Command(command="CleanBlackList")
async def cleanblacklist(event):
    await event.edit(client.STRINGS["wait"])
    blacks = event.client.DB.get_key("BLACK_LIST") or []
    if not blacks:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("BLACK_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])