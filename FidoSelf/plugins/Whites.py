from FidoSelf import client

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
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    whites = client.DB.get_key("WHITES") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
    if userid in whites:
        return await event.edit(STRINGS["notall"].format(mention))
    whites.append(userid)
    client.DB.set_key("WHITES", whites)
    whites = client.DB.get_key("WHITES") or []
    if userid in whites:
        whites.remove(userid)
        client.DB.set_key("WHITES", whites)
    await event.edit(client.get_string("Whites_2").format(mention))
    
@client.Command(command="DelWhite ?(.*)?")
async def delwhite(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    whites = client.DB.get_key("WHITES") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
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