from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Vip",
    "Info": {
        "Help": "To Manage Users On Vip List!",
        "Commands": {
            "{CMD}AddVip": {
                "Help": "To Add User On Vip List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelVip": {
                "Help": "To Delete User From Vip List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}VipList": {
                "Help": "To Getting Vip List",
           },
            "{CMD}CleanVipList": {
                "Help": "To Cleaning Vip List",
           },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**The User** ( {} ) **Already In Vip List!**",
    "add": "**The User** ( {} ) **Is Added To Vip List!**",
    "notin": "**The User** ( {} ) **Is Not In Vip List!**",
    "del": "**The User** ( {} ) **Deleted From Vip List!**",
    "empty": "**The Vip List Is Empty!**",
    "list": "**The Vip List:**\n\n",
    "aempty": "**The Vip List Is Already Empty**",
    "clean": "**The Vip List Has Been Cleaned!**",
}

@client.Command(command="AddVip ?(.*)?")
async def addvip(event):
    await event.edit(client.getstrings()["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.getstrings()["user"]["all"])
    vips = client.DB.get_key("VIP_USERS") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid in vips:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    vips.append(userid)
    client.DB.set_key("VIP_USERS", vips)
    await event.edit(client.getstrings(STRINGS)["add"].format(mention))
    
@client.Command(command="DelVip ?(.*)?")
async def delvip(event):
    await event.edit(client.getstrings()["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.getstrings()["user"]["all"])
    vips = client.DB.get_key("VIP_USERS") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in vips:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))  
    vips.remove(userid)
    client.DB.set_key("VIP_USERS", vips)
    await event.edit(client.getstrings(STRINGS)["del"].format(mention))
    
@client.Command(command="VipList")
async def viplist(event):
    await event.edit(client.getstrings()["wait"])
    vips = client.DB.get_key("VIP_USERS") or []
    if not vips:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for vip in vips:
        text += f"**{row} -** `{vip}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanVipList")
async def cleanviplist(event):
    await event.edit(client.getstrings()["wait"])
    vips = client.DB.get_key("VIP_USERS") or []
    if not vips:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("VIP_USERS")
    await event.edit(client.getstrings(STRINGS)["clean"])