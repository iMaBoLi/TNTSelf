from TNTSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Name": "My Stickers",
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
    "not": "**{STR} The List Of Your Stickers Is Empty!**",
    "stickers": "**{STR} The List Of Your Stickers:**\n\n",
}

@client.Command(command="MyStickers")
async def mystickers(event):
    await event.edit(client.STRINGS["wait"])
    stickers = await client(functions.messages.GetMyStickersRequest(offset_id=0, limit=50))
    if stickers.count == 0:
        return await event.edit(client.getstrings(STRINGS)["not"])
    text = client.getstrings(STRINGS)["stickers"]
    row = 1
    for sticker in stickers.sets:
        link = f"https://t.me/addstickers/{sticker.set.short_name}"
        link = f"[{sticker.set.title}]({link})"
        text += f"**{row} -** {link} ( `{sticker.set.count}` )\n"
        row += 1
    await event.edit(text)