from FidoSelf import client
from telethon.tl import types

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Dice|Dart|Basket|Roll|Foot)$")
async def gameemojis(event):
    await event.delete()
    emojis = {
        "Dice": "🎲",
        "Dart": "🎯",
        "Basket": "🏀",
        "Roll": "🎰",
        "Foot": "⚽️",
        "Nem": "🎳",
    }
    emoji = event.pattern_match.group(1).title()
    emoji = emojis[emoji]
    await client.send_file(event.chat_id, types.InputMediaDice(emoji))
