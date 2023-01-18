from FidoSelf import client
from telethon.tl import types

@client.Command(pattern=f"(?i)^\{client.cmd}S(Dice|Dart|Basket|Foot|Boll|Slot)$")
async def gameemojis(event):
    await event.delete()
    emojis = {
        "Dice": "🎲",
        "Dart": "🎯",
        "Basket": "🏀",
        "Foot": "⚽️",
        "Slot": "🎰",
        "Boll": "🎳",
    }
    emoji = event.pattern_match.group(1).title()
    emoji = emojis[emoji]
    await client.send_file(event.chat_id, types.InputMediaDice(emoji))
