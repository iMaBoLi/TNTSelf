from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Rank",
    "Info": {
        "Help": "To Manage Rank Of Users In Self!",
        "Commands": {
            "{CMD}SetRank <Rank> <Reply>": None,
            "{CMD}DelRank <Reply|Userid|Username>": None,
            "{CMD}GetRank <Reply|Userid|Username>": None,
            "{CMD}RankList": None,
            "{CMD}CleanRankList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setrank": "**{STR} The Rank Of User** ( {} ) **Was Set To** ( `{}` )",
    "notrank": "**{STR} The Rank For User** ( {} ) **Is Not Saved!**",
    "delrank": "**{STR} The Rank Of User** ( {} ) **Has Been Deleted!**",
    "getrank": "**{STR} The Rank Of User** ( {} ) **Is** ( `{}` )",
    "empty": "**{STR} The Rank List Is Empty!**",
    "ranklist": "**{STR} The Ranks List:**\n\n",
    "aempty": "**{STR} The Rank List Is Already Empty**",
    "clean": "**{STR} The Rank List Has Been Cleaned!**"
}

@client.Command(command="SetRank (.*)")
async def setrank(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid()
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    rank = event.pattern_match.group(1)
    ranks = client.DB.get_key("RANK_LIST") or {}
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    ranks.update({userid: rank})
    client.DB.set_key("RANK_LIST", ranks)
    await event.edit(client.getstrings(STRINGS)["setrank"].format(mention, rank))
    
@client.Command(command="DelRank ?(.*)?")
async def delrank(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    ranks = client.DB.get_key("RANK_LIST") or {}
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in ranks:
        return await event.edit(client.getstrings(STRINGS)["notrank"].format(mention))  
    del ranks[userid]
    client.DB.set_key("RANK_LIST", ranks)
    await event.edit(client.getstrings(STRINGS)["delrank"].format(mention))
    
@client.Command(command="GetRank ?(.*)?")
async def getrank(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["user"]["all"])
    ranks = client.DB.get_key("RANK_LIST") or {}
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in ranks:
        return await event.edit(client.getstrings(STRINGS)["notrank"].format(mention))  
    rank = ranks[userid]
    await event.edit(client.getstrings(STRINGS)["getrank"].format(mention, rank))
    
@client.Command(command="RankList")
async def ranklist(event):
    await event.edit(client.STRINGS["wait"])
    ranks = client.DB.get_key("RANK_LIST") or {}
    if not ranks:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["ranklist"]
    row = 1
    for rank in ranks:
        text += f"**{row} -** `{rank}` - `{ranks[rank]}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanRankList")
async def cleanranklist(event):
    await event.edit(client.STRINGS["wait"])
    ranks = client.DB.get_key("RANK_LIST") or {}
    if not ranks:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("RANK_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])