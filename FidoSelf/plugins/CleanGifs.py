from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Name": "Clean Gifs",
    "Info": {
        "Help": "To Clean Recent Saved Gifs!",
        "Commands": {
            "{CMD}CGifs": {
                "Help": "To Delete All Gifs",
            },
            "{CMD}CGifs <Count>": {
                "Help": "To Delete Some Gifs",
                "Input": {
                    "<Count>": "Number Of Gifs",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "cleaning": "**{STR} The Saved Gifs Is Cleaning ...** ( `{}` )",
    "cleaned": "**{STR} The Number Of** ( `{}` ) **From Your Saved Gifs Has Been Cleaned!**",
}

@client.Command(command="CGifs ?(\d*)?")
async def cleangifs(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    number = event.pattern_match.group(1)
    result = await client(functions.messages.GetSavedGifsRequest(hash=0))
    gifcount = number if number else len(result.gifs)
    await edit.edit(client.getstrings(STRINGS)["cleaning"].format(gifcount))
    count = 0
    for gif in result.gifs:
        gifid = types.InputDocument(id=gif.id, access_hash=gif.access_hash, file_reference=gif.file_reference)
        await client(functions.messages.SaveGifRequest(id=gifid, unsave=True))
        count += 1
        if number and count >= number:
            break
    await edit.edit(client.getstrings(STRINGS)["cleaned"].format(count))