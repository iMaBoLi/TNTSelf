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

@client.Command(onlysudo=False, alowedits=False)
async def action(event):
    if event.is_sudo or event.is_bot: return
    for action in ACTIONS:
        acMode = client.DB.get_key(action.upper() + "_ALL") or "off"
        acChats = client.DB.get_key(action.upper() + "_CHATS") or []
        if acMode == "on" or event.chat_id in acChats:
            if action == "bandari":
                client.loop.create_task(sendrandomaction(event.chat_id))
            else:
                client.loop.create_task(sendaction(event.chat_id, action))
                
async def sendaction(chat_id, action):
    async with client.action(chat_id, action):
        await asyncio.sleep(3)

async def sendrandomaction(chat_id):
    for action in ACTIONS[1:]:
        async with client.action(chat_id, action):
            await asyncio.sleep(1)