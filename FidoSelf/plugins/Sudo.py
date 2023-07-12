from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Sudo",
    "Info": {
        "Help": "To Manage Users On Sudo List!",
        "Commands": {
            "{CMD}AddSudo": {
                "Help": "To Add User On Sudo List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelSudo": {
                "Help": "To Delete User From Sudo List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}SudoList": {
                "Help": "To Getting Sudo List",
           },
            "{CMD}CleanSudoList": {
                "Help": "To Cleaning Sudo List",
           },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**{STR} The User** ( {} ) **Already In Sudo List!**",
    "add": "**{STR} The User** ( {} ) **Is Added To Sudo List!**",
    "notin": "**{STR} The User** ( {} ) **Is Not In Sudo List!**",
    "del": "**{STR} The User** ( {} ) **Deleted From Sudo List!**",
    "empty": "**{STR} The Sudo List Is Empty!**",
    "list": "**{STR} The Sudo List:**\n\n",
    "aempty": "**{STR} The Sudo List Is Already Empty**",
    "clean": "**{STR} The Sudo List Has Been Cleaned!**"
}

@client.Command(command="AddSudo", userid=True)
async def addsudo(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    sudos = client.DB.get_key("SUDO_USERS") or []
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid in sudos:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    sudos.append(event.userid)
    client.DB.set_key("SUDO_USERS", sudos)
    await event.edit(client.getstrings(STRINGS)["add"].format(mention))
    
@client.Command(command="DelSudo", userid=True)
async def delsudo(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    sudos = client.DB.get_key("SUDO_USERS") or []
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    if event.userid not in sudos:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))  
    sudos.remove(event.userid)
    client.DB.set_key("SUDO_USERS", sudos)
    await event.edit(client.getstrings(STRINGS)["del"].format(mention))
    
@client.Command(command="SudoList")
async def sudolist(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    sudos = client.DB.get_key("SUDO_USERS") or []
    if not sudos:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for sudo in sudos:
        text += f"**{row} -** `{sudo}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanSudoList")
async def cleansudolist(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    sudos = client.DB.get_key("SUDO_USERS") or []
    if not sudos:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("SUDO_USERS")
    await event.edit(client.getstrings(STRINGS)["clean"])