from FidoSelf import client
import asyncio

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
        mode = client.DB.get_key(action.upper() + "_ALL") or "off"
        chats = client.DB.get_key(action.upper() + "_CHATS") or []
        if mode == "on" or event.chat_id in chats:
            async with client.action(event.chat_id, action):
                await asyncio.sleep(5)