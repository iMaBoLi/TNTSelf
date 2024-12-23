from TNTSelf import client
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

@client.Command(command="S(Dice|Dart|Basket|Foot|Boll|Slot) ?(1|2|3|4|5|6)?")
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
    number = event.pattern_match.group(2)
    emoji = emojis[emoji]
    send = await event.client.send_file(event.chat_id, types.InputMediaDice(emoji))
    if number:
        sendnumber = send.media.value
        while sendnumber != int(number):
            await send.delete()
            send = await event.client.send_file(event.chat_id, types.InputMediaDice(emoji))
            sendnumber = send.media.value