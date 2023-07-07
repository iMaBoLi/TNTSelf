from FidoSelf import client
from telethon.tl import types

__INFO__ = {
    "Category": "Funs",
    "Name": "Emojis",
    "Info": {
        "Help": "To Send Emoji Games In Chats!",
        "Commands": {
            "{CMD}SDice": None,
            "{CMD}SDart": None,
            "{CMD}SBasket": None,
            "{CMD}SFoot": None,
            "{CMD}SBoll": None,
            "{CMD}SSlot": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="S(Dice|Dart|Basket|Foot|Boll|Slot)")
async def gameemojis(event):
    await event.delete()
    emojis = {
        "Dice": "🎲",
        "Dart": "🎯",
        "Basket": "🏀",
        "Foot": "⚽️",
        "Boll": "🎳",
        "Slot": "🎰",
    }
    emoji = event.pattern_match.group(1).title()
    emoji = emojis[emoji]
    await client.send_file(event.chat_id, types.InputMediaDice(emoji))
