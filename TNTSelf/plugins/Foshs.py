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
    "empty": "**{STR} The Fosh List Is Empty!**",
    "list": "**{STR} The Fosh List:**\n\n",
    "aempty": "**{STR} The Fosh List Is Already Empty!**",
    "clean": "**{STR} The Fosh List Is Cleaned!**"
}

FOSH_LIMIT = 500

@client.Command(command="AddFosh (.*)")
async def addfosh(event):
    await event.edit(client.STRINGS["wait"])
    foshs = event.client.DB.get_key("FOSH_LIST") or []
    newfosh = str(event.pattern_match.group(1))
    newfoshs = newfoshs.split(",")[:50]
    if len(foshs) >= FOSH_LIMIT:
        return await event.edit(client.getstrings(STRINGS)["limadd"].format(FOSH_LIMIT))
    newfoshs = newfoshs if len(foshs) + len(newfoshs) <= FOSH_LIMIT else newfoshs[:FOSH_LIMIT - len(foshs)]
    addfoshs = ""
    for fosh in newfoshs:
        foshs.append(fosh)
        addfoshs += f"{fosh} - "
    event.client.DB.set_key("FOSH_LIST", foshs)
    addfoshs = addfoshs[:-3]
    await event.edit(client.getstrings(STRINGS)["newadd"].format(addfoshs))

@client.Command(command="FoshList")
async def foshlist(event):
    await event.edit(client.STRINGS["wait"])
    foshs = event.client.DB.get_key("FOSH_LIST") or client.functions.FOSHS
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