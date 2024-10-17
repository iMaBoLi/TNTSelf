from TNTSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Account",
    "Name": "MyStickers",
    "Info": {
        "Help": "To Get List Of Your Stickers!",
        "Commands": {
            "{CMD}MyStickers": {
                "Help": "To Get Stickers",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "get": "**{STR} Getting List Of Your Stickers ...**",
    "not": "**{STR} The List Of Your Stickers Is Empty!**",
    "stickers": "**{STR} The List Of Your Stickers:**\n\n",
}

@client.Command(command="MyStickers")
async def mystickers(event):
    await event.edit(client.STRINGS["wait"])
    await event.edit(client.getstrings(STRINGS)["get"])
    stickers = await client(functions.messages.GetMyStickersRequest(offset_id=0, limit=100))
    if stickers.count == 0:
        return await event.edit(client.getstrings(STRINGS)["not"])
    text = client.getstrings(STRINGS)["stickers"]
    row = 1
    for sticker in stickers.sets:
        link = f"https://t.me/addstickers/{sticker.set.short_name}"
        link = f"[{sticker.set.title}]({link})"
        text += f"**{row} -** {link}\n"
        row += 1
    await event.edit(text)