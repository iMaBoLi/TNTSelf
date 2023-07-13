from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Name": "Clean Stickers",
    "Info": {
        "Help": "To Clean Recent Saved Stickers!",
        "Commands": {
            "{CMD}CStickers": {
                "Help": "To Clean Stickers",
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
    await client(functions.messages.ClearRecentStickersRequest(attached=False))
    await event.edit(client.getstrings(STRINGS)["cleaned"])