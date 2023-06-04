from FidoSelf import client
from telethon import functions

ACTIONS = [
    "typing",
    "game",
    "photo",
    "audio",
    "video",
    "file",
    "sticker",
    "contact",
    "location",
    "record-video",
    "record-audio",
    "record-round",
]

@client.Command(onlysudo=False)
async def action(event):
    if event.is_bot: return
    for action in ACTIONS:
        mode = action.upper() + "_ALL"
        mode = client.DB.get_key(mode) or "off"
        if mode == "on":
            await client.action(event.chat_id, action)
            continue
        mode = action.upper() + "_CHATS"
        chats = client.DB.get_key(mode) or []
        if event.chat_id in chats:
            await client.action(event.chat_id, action)