from TNTSelf import client
from .ManageTime import biochanger

__INFO__ = {
    "Category": "Time",
    "Bio": "Bio Time",
    "Info": {
        "Help": "To Setting Your Bio Times",
        "Commands": {
            "{CMD}Bio <On-Off>": {
                "Help": "To Turn On-Off Bio Mode",
            },
            "{CMD}NewBio <Text>": {
                "Help": "To Add Bio",
                "Input": {
                    "<Text>": "Text For Add",
                },
            },
            "{CMD}DelBio <Text>": {
                "Help": "To Delete Bio",
                "Input": {
                    "<Text>": "Text For Delete",
                },
            },
            "{CMD}BioList": {
                "Help": "To Get Bio List",
            },
            "{CMD}CleanBioList": {
                "Help": "To Clean Bio List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Bio Mode Has Been {}!**",
    "newnot": "**{STR} The Bio** ( `{}` ) **Already In Bio List!**",
    "newadd": "**{STR} The Bio** ( `{}` ) **Added To Bio List!**",
    "delnot": "**{STR} The Bio** ( `{}` ) **Not In Bio List!**",
    "del": "**{STR} The Bio** ( `{}` ) **Deleted From Bio List!**",
    "empty": "**{STR} The Bio List Is Empty!**",
    "list": "**{STR} The Bio List:**\n\n",
    "aempty": "**{STR} The Bio List Is Already Empty!**",
    "clean": "**{STR} The Bio List Is Cleaned!**"
}

@client.Command(command="Bio (On|Off)")
async def biomode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("BIO_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))
    await biochanger()

@client.Command(command="NewBio (.*)")
async def addbio(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIO_LIST") or []
    newbio = str(event.pattern_match.group(1))
    if newbio in bios:
        return await event.edit(client.getstrings(STRINGS)["newnot"].format(newbio))  
    bios.append(newbio)
    client.DB.set_key("BIO_LIST", bios)
    await event.edit(client.getstrings(STRINGS)["newadd"].format(newbio))
    await biochanger()
    
@client.Command(command="DelBio (.*)")
async def delbio(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIO_LIST") or []
    newbio = str(event.pattern_match.group(1))
    if newbio not in bios:
        return await event.edit(client.getstrings(STRINGS)["delnot"].format(newbio))  
    bios.remove(newbio)
    client.DB.set_key("BIO_LIST", bios)
    await event.edit(client.getstrings(STRINGS)["del"].format(newbio))
    await biochanger()

@client.Command(command="BioList")
async def biolist(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIO_LIST") or []
    if not bios:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, bio in enumerate(bios):
        text += f"**{row + 1} -** `{bio}`\n"
    await event.edit(text)

@client.Command(command="CleanBioList")
async def cleanbios(event):
    await event.edit(client.STRINGS["wait"])
    bios = client.DB.get_key("BIO_LIST") or []
    if not bios:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("BIO_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])