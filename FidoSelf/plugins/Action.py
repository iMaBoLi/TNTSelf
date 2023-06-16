from FidoSelf import client
import asyncio
import random

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Action",
    "Pluginfo": {
        "Help": "To Setting Send Chat Actions And Set Mode!",
        "Commands": {
            "{CMD}Action <On-Off>": "Action For This Chat!",
            "{CMD}ActionAll <On-Off>": "Action For All Chats!",
            "{CMD}SetAction <Mode>": "Set Action Mode!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "actionall": "**The Send Chat Action Has Been {}!**",
    "actionchat": "**The Send Chat Action For This Chat Has Been {}!**",
    "notact": "**The Action** ( `{}` ) **Is Not Available!**",
    "setact": "**The Send Action Mode Was Set To** ( `{}` )",
}

@client.Command(command="Action (On|Off)")
async def actionchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    acChats = client.DB.get_key("ACTION_CHATS") or []
    chatid = event.chat_id
    if change == "on":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("ACTION_CHATS", acChats)
    else
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("ACTION_CHATS", acChats)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["actionchat"].format(ShowChange))

@client.Command(command="ActionAll (On|Off)")
async def actionall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("ACTION_ALL", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["actionall"].format(ShowChange))

@client.Command(command="SetAction (.*)")
async def setaction(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).lower()
    if mode not in client.functions.ACTIONS:
        return await event.edit(STRINGS["notact"].format(mode))
    client.DB.set_key("ACTION_TYPE", mode)
    await event.edit(STRINGS["setact"].format(mode.title()))

@client.Command(onlysudo=False, alowedits=False)
async def action(event):
    if event.is_sudo or event.is_bot: return
    acMode = client.DB.get_key("ACTION_ALL") or "off"
    acChats = client.DB.get_key("ACTION_CHATS") or []
    acType = client.DB.get_key("ACTION_TYPE") or "bold"
    if not acType: return
    if acMode == "on" or event.chat_id in acChats:
        if acType == "bandari":
            client.loop.create_task(sendrandomaction(event.chat_id))
        elif acType == "random":
            RType = random.choice(client.functions.ACTIONS[2:])
            client.loop.create_task(sendaction(event.chat_id, RType))
        else:
            client.loop.create_task(sendaction(event.chat_id, acType))
                
async def sendaction(chat_id, action):
    async with client.action(chat_id, action.lower()):
        await asyncio.sleep(3)

async def sendrandomaction(chat_id):
    for action in client.functions.ACTIONS[2:]:
        async with client.action(chat_id, action):
            await asyncio.sleep(1)