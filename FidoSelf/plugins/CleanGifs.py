from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Name": "Clean Gifs",
    "Info": {
        "Help": "To Delete Recent Saved Gifs!",
        "Commands": {
            "{CMD}CGifs": {
                "Help": "To Delete Gifs",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "cleaning": "**{STR} The Saved Gifs Is Cleaning ...** ( `{}` )",
    "cleaned": "**{STR} The Number Of** ( `{}` ) **From Your Saved Gifs Was Deleted!**",
}

@client.Command(command="CGifs")
async def cleangifs(event):
    await event.edit(client.STRINGS["wait"])
    result = await client(functions.messages.GetSavedGifsRequest(hash=0))
    await event.edit(client.getstrings(STRINGS)["cleaning"].format(len(result.gifs)))
    count = 0
    for gif in result.gifs:
        gifid = types.InputDocument(id=gif.id, access_hash=gif.access_hash, file_reference=gif.file_reference)
        await client(functions.messages.SaveGifRequest(id=gifid, unsave=True))
        count += 1
    await event.edit(client.getstrings(STRINGS)["cleaned"].format(count))
