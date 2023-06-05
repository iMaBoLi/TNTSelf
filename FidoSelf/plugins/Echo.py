from FidoSelf import client

STRINGS = {
    "notall": "**The User** ( {} ) **Already In Echo List!**",
    "add": "**The User** ( {} ) **Is Added To Echo List!**",
    "notin": "**The User** ( {} ) **Is Not In Echo List!**",
    "del": "**The User** ( {} ) **Deleted From Echo List!**",
    "empty": "**The Echo List Is Empty!**",
    "list": "**The Echo List:**\n\n",
    "aempty": "**The Echo List Is Already Empty**",
    "clean": "**The Echo List Has Been Cleaned!**",
}

@client.Command(command="AddEcho ?(.*)?")
async def addecho(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    echos = client.DB.get_key("ECHOS") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
    if userid in echos:
        return await event.edit(STRINGS["notall"].format(mention))
    echos.append(userid)
    client.DB.set_key("ECHOS", echos)
    whites = client.DB.get_key("WHITES") or []
    if userid in whites:
        whites.remove(userid)
        client.DB.set_key("WHITES", whites)
    await event.edit(STRINGS["add"].format(mention))
    
@client.Command(command="DelEcho ?(.*)?")
async def delecho(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    echos = client.DB.get_key("ECHOS") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
    if userid not in echos:
        return await event.edit(STRINGS["notin"].format(mention))  
    echos.remove(userid)
    client.DB.set_key("ECHOS", echos)
    await event.edit(STRINGS["del"].format(mention))
    
@client.Command(command="EchoList")
async def echolist(event):
    await event.edit(client.STRINGS["wait"])
    echos = client.DB.get_key("ECHOS") or []
    if not echos:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for echo in echos:
        text += f"**{row} -** `{echo}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanEchoList")
async def cleanecholist(event):
    await event.edit(client.STRINGS["wait"])
    echos = client.DB.get_key("ECHOS") or []
    if not echos:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("ECHOS")
    await event.edit(STRINGS["clean"])
    
@client.Command(onlysudo=False, alowedits=False)
async def echo(event):
    echos = client.DB.get_key("ECHOS") or []
    if event.sender_id in echos:
        message = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(message)
