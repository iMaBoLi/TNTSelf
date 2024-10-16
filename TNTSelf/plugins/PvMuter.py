from TNTSelf import client

__INFO__ = {
    "Category": "Pv",
    "Name": "Pv Mute",
    "Info": {
        "Help": "To Manage Users On MutePv List!",
        "Commands": {
            "{CMD}AddMutePv": {
                "Help": "To Add User On MutePv List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelMutePv": {
                "Help": "To Delete User From MutePv List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}MutePvList": {
                "Help": "To Getting MutePv List",
            },
            "{CMD}CleanMutePvList": {
                "Help": "To Clean MutePv List",
            },
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

@client.Command(command="AddMutePv", userid=True)
async def addmutepv(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid in mutepvs:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    mutepvs.append(event.userid)
    client.DB.set_key("MUTEPV_USERS", mutepvs)
    await event.edit(client.getstrings(STRINGS)["add"].format(mention))
    
@client.Command(command="DelMutePv", userid=True)
async def delmutepv(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid not in mutepvs:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))  
    mutepvs.remove(event.userid)
    client.DB.set_key("MUTEPV_USERS", mutepvs)
    await event.edit(client.getstrings(STRINGS)["del"].format(mention))
    
@client.Command(command="MutePvList")
async def mutepvlist(event):
    await event.edit(client.STRINGS["wait"])
    mutepvs = client.DB.get_key("MUTEPV_USERS") or []
    if not mutepvs:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, mutepv in enumerate(mutepvs):
        text += f"**{row + 1} -** `{mutepv}`\n"
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
        event.checkSpam(bantime=0, block=True)
        await event.delete()