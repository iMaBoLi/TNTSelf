from FidoSelf import client

__INFO__ = {
    "Category": "Pv",
    "Name": "Pv Mute",
    "Info": {
        "Help": "To Manage Users On MutePv List!",
        "Commands": {
            "{CMD}AddMutePv <Reply|Userid|Username>": None,
            "{CMD}DelMutePv <Reply|Userid|Username>": None,
            "{CMD}MutePvList": None,
            "{CMD}CleanMutePvList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**{STR} The User** ( {} ) **Already In MutePv List!**",
    "add": "**{STR} The User** ( {} ) **Is Added To MutePv List!**",
    "notin": "**{STR} The User** ( {} ) **Is Not In MutePv List!**",
    "del": "**{STR} The User** ( {} ) **Deleted From MutePv List!**",
    "empty": "**{STR} The MutePv List Is Empty!**",
    "list": "**{STR} The MutePv List:**\n\n",
    "aempty": "**{STR} The MutePv List Is Already Empty**",
    "clean": "**{STR} The MutePv List Has Been Cleaned!**"
}

@client.Command(command="AddMutePv ?(.*)?")
async def addmutepv(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid in mutepvs:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    mutepvs.append(userid)
    client.DB.set_key("MUTEPV_USERS", mutepvs)
    whites = client.DB.get_key("WHITE_LIST") or []
    if userid in whites:
        whites.remove(userid)
        client.DB.set_key("WHITE_LIST", whites)
    await event.edit(client.getstrings(STRINGS)["add"].format(mention))
    
@client.Command(command="DelMutePv ?(.*)?")
async def delmutepv(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in mutepvs:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))  
    mutepvs.remove(userid)
    client.DB.set_key("MUTEPV_USERS", mutepvs)
    await event.edit(client.getstrings(STRINGS)["del"].format(mention))
    
@client.Command(command="MutePvList")
async def mutepvlist(event):
    await event.edit(client.STRINGS["wait"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    if not mutepvs:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for mutepv in mutepvs:
        text += f"**{row} -** `{mutepv}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanMutePvList")
async def cleanmutepvlist(event):
    await event.edit(client.STRINGS["wait"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    if not mutepvs:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("MUTEPV_USERS")
    await event.edit(client.getstrings(STRINGS)["clean"])
    
@client.Command(onlysudo=False, allowedits=False)
async def pvmuter(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mutes = client.DB.get_key("MUTEPV_USERS") or []
    if event.sender_id in mutes:
        await event.delete()