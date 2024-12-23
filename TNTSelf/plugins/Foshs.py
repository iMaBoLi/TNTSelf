from TNTSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Foshs",
    "Info": {
        "Help": "To Setting Your Foshs List",
        "Commands": {
            "{CMD}AddFosh <Text>": {
                "Help": "To Add Fosh",
                "Input": {
                    "<Text>": "Text For Add",
                },
            },
            "{CMD}DelFosh <Text>": {
                "Help": "To Delete Fosh",
                "Input": {
                    "<Text>": "Text For Delete",
                },
            },
            "{CMD}FoshList": {
                "Help": "To Get Fosh List",
            },
            "{CMD}CleanFoshList": {
                "Help": "To Clean Fosh List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "newadd": "**{STR} The Foshs** ( `{}` ) **Added To Fosh List!**",
    "delnot": "**{STR} The Fosh** ( `{}` ) **Not In Fosh List!**",
    "del": "**{STR} The Fosh** ( `{}` ) **Deleted From Fosh List!**",
    "empty": "**{STR} The Fosh List Is Empty!**",
    "list": "**{STR} The Fosh List:**\n\n",
    "aempty": "**{STR} The Fosh List Is Already Empty!**",
    "clean": "**{STR} The Fosh List Is Cleaned!**"
}

FOSH_LIMIT = 500

@client.Command(command="NewFosh (.*)")
async def addfosh(event):
    await event.edit(client.STRINGS["wait"])
    foshs = event.client.DB.get_key("FOSH_LIST") or []
    newfoshs = str(event.pattern_match.group(1))
    newfoshs = newfoshs.split(",")[:50]
    if len(foshs) >= FOSH_LIMIT:
        return await event.edit(client.getstrings(STRINGS)["limadd"].format(FOSH_LIMIT))
    newfoshs = newfoshs if len(foshs) + len(newfoshs) <= FOSH_LIMIT else newfoshs[:FOSH_LIMIT - len(foshs)]
    for fosh in newfoshs:
        foshs.append(fosh)
    event.client.DB.set_key("FOSH_LIST", foshs)
    await event.edit(client.getstrings(STRINGS)["newadd"].format(newfoshs))
    
@client.Command(command="DelFosh (.*)")
async def delfosh(event):
    await event.edit(client.STRINGS["wait"])
    foshs = event.client.DB.get_key("FOSH_LIST") or []
    newfosh = str(event.pattern_match.group(1))
    if newfosh not in foshs:
        return await event.edit(client.getstrings(STRINGS)["delnot"].format(newfosh))  
    foshs.remove(newfosh)
    event.client.DB.set_key("FOSH_LIST", foshs)
    await event.edit(client.getstrings(STRINGS)["del"].format(newfosh))

@client.Command(command="FoshList")
async def foshlist(event):
    await event.edit(client.STRINGS["wait"])
    foshs = event.client.DB.get_key("FOSH_LIST") or []
    if not foshs:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for fosh in foshs:
        text += f"`{fosh}` - "
    text = text[:-3]
    await event.edit(text)

@client.Command(command="CleanFoshList")
async def cleanfoshs(event):
    await event.edit(client.STRINGS["wait"])
    foshs = event.client.DB.get_key("FOSH_LIST") or []
    if not foshs:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("FOSH_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])