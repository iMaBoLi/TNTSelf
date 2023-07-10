from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Name": "Clean Stickers",
    "Info": {
        "Help": "To Clean Recent Saved Stickers!",
        "Commands": {
            "{CMD}CStickers": {
                "Help": "To Delete All Stickers",
            },
            "{CMD}CStickers <Count>": {
                "Help": "To Delete Some Stickers",
                "Input": {
                    "<Count>": "Number Of Stickers",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "cleaning": "**{STR} The Saved Stickers Is Cleaning ...**",
    "cleaned": "**{STR} The Saved Stickers Has Been Cleaned!**",
}

@client.Command(command="CStickers")
async def cleanstickers(event):
    await event.edit(client.STRINGS["wait"])
    await event.edit(client.getstrings(STRINGS)["cleaning"])
    await client(functions.messages.ClearRecentStickersRequest(attached=True))
    await event.edit(client.getstrings(STRINGS)["cleaned"])