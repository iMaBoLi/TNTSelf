from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "White",
    "Info": {
        "Help": "To Manage Users On White List!",
        "Commands": {
            "{CMD}AddWhite": {
                "Help": "To Add User On White List",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelWhite": {
                "Help": "To Delete User From White List",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}WhiteList": {
                "Help": "To Getting White List",
           },
            "{CMD}CleanWhiteList": {
                "Help": "To Cleaning White List",
           },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**The User** ( {} ) **Already In White List!**",
    "add": "**The User** ( {} ) **Is Added To White List!**",
    "notin": "**The User** ( {} ) **Is Not In White List!**",
    "del": "**The User** ( {} ) **Deleted From White List!**",
    "empty": "**The White List Is Empty!**",
    "list": "**The White List:**\n\n",
    "aempty": "**The White List Is Already Empty**",
    "clean": "**The White List Has Been Cleaned!**",
}

@client.Command(command="AddWhite ?(.*)?")
async def addwhite(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    whites = client.DB.get_key("WHITES") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid in whites:
        return await event.edit(STRINGS["notall"].format(mention))
    whites.append(userid)
    client.DB.set_key("WHITES", whites)
    whites = client.DB.get_key("BLACKS") or []
    if userid in whites:
        whites.remove(userid)
        client.DB.set_key("BLACKS", whites)
    await event.edit(STRINGS["add"].format(mention))
    
@client.Command(command="DelWhite ?(.*)?")
async def delwhite(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    whites = client.DB.get_key("WHITES") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in whites:
        return await event.edit(STRINGS["notin"].format(mention))  
    whites.remove(userid)
    client.DB.set_key("WHITES", whites)
    await event.edit(STRINGS["del"].format(mention))
    
@client.Command(command="WhiteList")
async def whitelist(event):
    await event.edit(client.STRINGS["wait"])
    whites = client.DB.get_key("WHITES") or []
    if not whites:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for white in whites:
        text += f"**{row} -** `{white}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanWhiteList")
async def cleanwhitelist(event):
    await event.edit(client.STRINGS["wait"])
    whites = client.DB.get_key("WHITES") or []
    if not whites:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("WHITES")
    await event.edit(STRINGS["clean"])