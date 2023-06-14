from FidoSelf import client
import asyncio

@client.Command(onlysudo=False, alowedits=False)
async def action(event):
    if event.is_sudo or event.is_bot: return
    acMode = client.DB.get_key("ACTION_ALL") or "off"
    acChats = client.DB.get_key("ACTION_CHATS") or []
    if acMode == "on" or event.chat_id in acChats:
        acType = client.DB.get_key("ACTION_TYPE") or []
        if acType == "bandari":
            client.loop.create_task(sendrandomaction(event.chat_id))
        else:
            client.loop.create_task(sendaction(event.chat_id, acType))
                
async def sendaction(chat_id, action):
    async with client.action(chat_id, action.lower()):
        await asyncio.sleep(3)

async def sendrandomaction(chat_id):
    for action in client.functions.ACTIONS[1:]:
        async with client.action(chat_id, action):
            await asyncio.sleep(1)