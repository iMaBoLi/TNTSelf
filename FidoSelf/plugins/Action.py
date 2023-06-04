from FidoSelf import client
import asyncio

ACTIONS = [
    "bandari",
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
    for action in ACTIONS:
        mode = client.DB.get_key(action.upper() + "_ALL") or "off"
        chats = client.DB.get_key(action.upper() + "_CHATS") or []
        if mode == "on" or event.chat_id in chats:
            if action == "bandari":
                for action in ACTIONS[1:]:
                    async with client.action(event.chat_id, action):
                        client.loop.create_task(asyncio.sleep(3))
                return
            else:
                async with client.action(event.chat_id, action):
                    client.loop.create_task(asyncio.sleep(3))