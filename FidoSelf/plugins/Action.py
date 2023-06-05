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
                    client.loop.create_task(sendaction(event.chat_id, action))
                return
            else:
                client.loop.create_task(sendaction(event.chat_id, action))
                
async def sendaction(chat_id, action):
    try:
        async with client.action(chat_id, action):
            await asyncio.sleep(5)
    except:
        client.LOGS.error(f"Chat Error": {chat_id}")