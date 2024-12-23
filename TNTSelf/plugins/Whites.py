from TNTSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "White",
    "Info": {
        "Help": "To Manage Users On White List!",
        "Commands": {
            "{CMD}AddWhite": {
                "Help": "To Add User On White List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelWhite": {
                "Help": "To Delete User From White List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
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
    "notall": "**{STR} The User** ( {} ) **Already In White List!**",
    "add": "**{STR} The User** ( {} ) **Is Added To White List!**",
    "notin": "**{STR} The User** ( {} ) **Is Not In White List!**",
    "del": "**{STR} The User** ( {} ) **Deleted From White List!**",
    "empty": "**{STR} The White List Is Empty!**",
    "list": "**{STR} The White List:**\n\n",
    "aempty": "**{STR} The White List Is Already Empty**",
    "clean": "**{STR} The White List Has Been Cleaned!**"
}

@client.Command(command="AddWhite", userid=True)
async def addwhite(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    whites = event.client.DB.get_key("WHITE_LIST") or []
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid in whites:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    whites.append(event.userid)
    event.client.DB.set_key("WHITE_LIST", whites)
    whites = event.client.DB.get_key("BLACK_LIST") or []
    if event.userid in whites:
        whites.remove(event.userid)
        event.client.DB.set_key("BLACK_LIST", whites)
    await event.edit(client.getstrings(STRINGS)["add"].format(mention))
    
@client.Command(command="DelWhite", userid=True)
async def delwhite(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    whites = event.client.DB.get_key("WHITE_LIST") or []
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid not in whites:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))  
    whites.remove(event.userid)
    event.client.DB.set_key("WHITE_LIST", whites)
    await event.edit(client.getstrings(STRINGS)["del"].format(mention))
    
@client.Command(command="WhiteList")
async def whitelist(event):
    await event.edit(client.STRINGS["wait"])
    whites = event.client.DB.get_key("WHITE_LIST") or []
    if not whites:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, white in enumerate(whites):
        text += f"**{row + 1} -** `{white}`\n"
    await event.edit(text)

@client.Command(command="CleanWhiteList")
async def cleanwhitelist(event):
    await event.edit(client.STRINGS["wait"])
    whites = event.client.DB.get_key("WHITE_LIST") or []
    if not whites:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("WHITE_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])