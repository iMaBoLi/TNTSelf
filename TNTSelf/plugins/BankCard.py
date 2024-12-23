from TNTSelf import client

__INFO__ = {
    "Category": "Funs",
    "Name": "Bank Card",
    "Info": {
        "Help": "To Save Your Bank Card In Self And Get Information!",
        "Commands": {
            "{CMD}SetCard '<Number>' <Name>": {
               "Help": "To Set Card Info",
                "Input": {
                    "<Number>" : "Your Card Number",
                    "<Name>" : "Your Name In Card",
                },
            },
            "{CMD}DelCard": {
               "Help": "To Delete Card Info",
            },
            "{CMD}Card": {
               "Help": "To Get Saved Card Info",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setcard": "**{STR} The Bank Card Saved!**\n\n**{STR} Card Number:** ( `{}` )\n**{STR} Card Name:** ( `{}` )",
    "delcard": "**{STR} The Saved Bank Card Was Deleted!**",
    "notcard": "**{STR} The Bank Card Is Not Saved!**",
    "card": "**{STR} Card Number:** ( `{}` )\n\n**{STR} Card Name:** ( `{}` )",
}

@client.Command(command="SetCard \\'(.*)\\' (.*)")
async def setcard(event):
    await event.edit(client.STRINGS["wait"])
    cnumber = str(event.pattern_match.group(1))
    cname = str(event.pattern_match.group(2))
    newcard = {"NUMBER": cnumber, "NAME": cname}
    event.client.DB.set_key("BANK_CARD", newcard)
    await event.edit(client.getstrings(STRINGS)["setcard"].format(cnumber, cname))
    
@client.Command(command="DelCard")
async def delcard(event):
    await event.edit(client.STRINGS["wait"])
    event.client.DB.set_key("BANK_CARD", {})
    await event.edit(client.getstrings(STRINGS)["delcard"])

@client.Command(command="Card")
async def getcard(event):
    card = event.client.DB.get_key("BANK_CARD") or {}
    if not card:
        return await event.edit(client.getstrings(STRINGS)["notcard"])
    text = client.getstrings(STRINGS)["card"].format(card["NUMBER"], card["NAME"])
    await event.edit(text)