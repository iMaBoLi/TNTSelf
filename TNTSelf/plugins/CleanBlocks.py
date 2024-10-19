from TNTSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Name": "Clean Blocks",
    "Info": {
        "Help": "To Clean Blocked Users!",
        "Commands": {
            "{CMD}CleanBlocks": {
                "Help": "To Clean Blocks!",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "cleaning": "**{STR} Cleanning** ( `{}` ) **User Of Blocked Users ...**",
    "clean": "**{STR} The** ( `{}` ) **From** ( `{}` ) **Blocked Users Is Cleaned!**",
}

@client.Command(command="CleanBlocks")
async def cleanblocks(event):
    await event.edit(client.STRINGS["wait"])
    blocks = await client(functions.contacts.GetBlockedRequest(offset=0, limit=100))
    blocks = blocks.users
    await event.edit(client.getstrings(STRINGS)["cleaning"].format(len(blocks)))
    count = 0
    for user in blocks:
        unblock = await client(functions.contacts.UnblockRequest(id=user.id))
        if unblock:
            count += 1
    await event.edit(client.getstrings(STRINGS)["clean"].format(count, len(blocks)))