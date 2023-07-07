from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Black",
    "Info": {
        "Help": "To Manage Users On Black List!",
        "Commands": {
            "{CMD}AddBlack": {
                "Help": "To Add User On Black List",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelBlack": {
                "Help": "To Delete User From Black List",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
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
    "notall": "**The User** ( {} ) **Already In Black List!**",
    "add": "**The User** ( {} ) **Is Added To Black List!**",
    "notin": "**The User** ( {} ) **Is Not In Black List!**",
    "del": "**The User** ( {} ) **Deleted From Black List!**",
    "empty": "**The Black List Is Empty!**",
    "list": "**The Black List:**\n\n",
    "aempty": "**The Black List Is Already Empty**",
    "clean": "**The Black List Has Been Cleaned!**",
}

@client.Command(command="AddBlack ?(.*)?")
async def addblack(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    blacks = client.DB.get_key("BLACKS") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid in blacks:
        return await event.edit(STRINGS["notall"].format(mention))
    blacks.append(userid)
    client.DB.set_key("BLACKS", blacks)
    whites = client.DB.get_key("WHITES") or []
    if userid in whites:
        whites.remove(userid)
        client.DB.set_key("WHITES", whites)
    await event.edit(STRINGS["add"].format(mention))
    
@client.Command(command="DelBlack ?(.*)?")
async def delblack(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    blacks = client.DB.get_key("BLACKS") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in blacks:
        return await event.edit(STRINGS["notin"].format(mention))  
    blacks.remove(userid)
    client.DB.set_key("BLACKS", blacks)
    await event.edit(STRINGS["del"].format(mention))
    
@client.Command(command="BlackList")
async def blacklist(event):
    await event.edit(client.STRINGS["wait"])
    blacks = client.DB.get_key("BLACKS") or []
    if not blacks:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for black in blacks:
        text += f"**{row} -** `{black}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanBlackList")
async def cleanblacklist(event):
    await event.edit(client.STRINGS["wait"])
    blacks = client.DB.get_key("BLACKS") or []
    if not blacks:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("BLACKS")
    await event.edit(STRINGS["clean"])