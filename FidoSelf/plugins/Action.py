from FidoSelf import client
from telethon import events
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
            "{CMD}ActionList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Manage",
    "Plugname": "Copy Action",
    "Pluginfo": {
        "Help": "To Setting Copy Chat Actions And Send Action!",
        "Commands": {
            "{CMD}CAction <On-Off>": None,
            "{CMD}CActionAll <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "actionall": "**The Send Chat Action Has Been {}!**",
    "actionchat": "**The Send Chat Action For This Chat Has Been {}!**",
    "notact": "**The Action** ( `{}` ) **Is Not Available!**",
    "setact": "**The Send Action Mode Was Set To** ( `{}` )",
    "actions": "**The Action List:**\n\n",
}

@client.Command(command="Action (On|Off)")
async def actionchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = client.DB.get_key("ACTION_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("ACTION_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("ACTION_CHATS", acChats)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["actionchat"].format(ShowChange))

@client.Command(command="ActionAll (On|Off)")
async def actionall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ACTION_ALL", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["actionall"].format(ShowChange))

@client.Command(command="SetAction (.*)")
async def setaction(event):
    await event.edit(client.STRINGS["wait"])
    acmode = event.pattern_match.group(1).lower()
    if acmode not in client.functions.ACTIONS:
        return await event.edit(STRINGS["notact"].format(acmode))
    client.DB.set_key("ACTION_TYPE", acmode)
    await event.edit(STRINGS["setact"].format(acmode.title()))

@client.Command(command="ActionList")
async def actionlist(event):
    await event.edit(client.STRINGS["wait"])
    text = STRINGS["actions"]
    for lang in client.functions.ACTIONS:
        text += f"• `{lang.title()}`\n"
    await event.edit(text)

@client.Command(command="CAction (On|Off)")
async def copyactionchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = client.DB.get_key("COPYACTION_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("COPYACTION_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("COPYACTION_CHATS", acChats)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["copyactionchat"].format(ShowChange))

@client.Command(command="CActionAll (On|Off)")
async def copyactionall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("COPYACTION_ALL", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["copyactionall"].format(ShowChange))

@client.Command(onlysudo=False, allowedits=False)
async def action(event):
    if event.is_sudo or event.is_bot: return
    acMode = client.DB.get_key("ACTION_ALL") or "OFF"
    acChats = client.DB.get_key("ACTION_CHATS") or []
    acType = client.DB.get_key("ACTION_TYPE") or "random"
    if not acType: return
    if acMode == "ON" or event.chat_id in acChats:
        if acType == "bandari":
            client.loop.create_task(sendrandomaction(event.chat_id))
        elif acType == "random":
            RType = random.choice(client.functions.ACTIONS[2:])
            client.loop.create_task(sendaction(event.chat_id, RType))
        else:
            client.loop.create_task(sendaction(event.chat_id, acType))

@client.on(events.UserUpdate)
async def handler(event):
    if event.user_id == client.me.id: return
    cacMode = client.DB.get_key("COPYACTION_ALL") or "OFF"
    cacChats = client.DB.get_key("COPYACTION_CHATS") or []
    if cacMode == "ON" or event.chat_id in cacChats:
        if event.typing:
            client.loop.create_task(sendaction(event.chat_id, "typing"))
            

async def sendaction(chat_id, action):
    async with client.action(chat_id, action.lower()):
        await asyncio.sleep(3)

async def sendrandomaction(chat_id):
    for action in client.functions.ACTIONS[2:]:
        async with client.action(chat_id, action):
            await asyncio.sleep(1)