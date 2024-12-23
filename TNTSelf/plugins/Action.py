from TNTSelf import client
from telethon import events
import asyncio
import random

__INFO__ = {
    "Category": "Practical",
    "Name": "Action",
    "Info": {
        "Help": "To Setting Send Chat Actions!",
        "Commands": {
            "{CMD}Action <On-Off>": {
                "Help": "To Turn On-Off Action In This Chat!"
            },
            "{CMD}ActionAll <On-Off>": {
                "Help": "To Turn On-Off Action For All Chats!"
            },
            "{CMD}SetAction <Mode>": ""
                "Help": "To Set Action Mode",
                "Input": {
                    "<CMD>": "Mode For Set",
                },
                "Vars": [action.title() for action in client.functions.ACTIONS]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)
__INFO__ = {
    "Category": "Practical",
    "Name": "Copy Action",
    "Info": {
        "Help": "To Setting Copy Chat Actions!",
        "Commands": {
            "{CMD}CAction <On-Off>": {
                "Help": "To Turn On-Off Copy Action In This Chat!"
            },
            "{CMD}CActionAll <On-Off>": {
                "Help": "To Turn On-Off Copy Action For All Chats!"
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "actionall": "**{STR} The Send Chat Action Has Been {}!**",
    "actionchat": "**{STR} The Send Chat Action For This Chat Has Been {}!**",
    "notact": "**{STR} The Action** ( `{}` ) **Is Not Available!**",
    "setact": "**{STR} The Send Action Mode Was Set To** ( `{}` )",
    "copyactionall": "**{STR} The Copy Chat Action Has Been {}!**",
    "copyactionchat": "**{STR} The Copy Chat Action For This Chat Has Been {}!**"
}

@client.Command(command="Action (On|Off)")
async def actionchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = event.client.DB.get_key("ACTION_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            event.client.DB.set_key("ACTION_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            event.client.DB.set_key("ACTION_CHATS", acChats)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["actionchat"].format(showchange))

@client.Command(command="ActionAll (On|Off)")
async def actionall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("ACTION_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["actionall"].format(showchange))

@client.Command(command="SetAction (.*)")
async def setaction(event):
    await event.edit(client.STRINGS["wait"])
    acmode = event.pattern_match.group(1).lower()
    if acmode not in client.functions.ACTIONS:
        return await event.edit(client.getstrings(STRINGS)["notact"].format(acmode))
    event.client.DB.set_key("ACTION_TYPE", acmode)
    await event.edit(client.getstrings(STRINGS)["setact"].format(acmode.title()))

@client.Command(command="CAction (On|Off)")
async def copyactionchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = event.client.DB.get_key("COPYACTION_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            event.client.DB.set_key("COPYACTION_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            event.client.DB.set_key("COPYACTION_CHATS", acChats)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["copyactionchat"].format(showchange))

@client.Command(command="CActionAll (On|Off)")
async def copyactionall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("COPYACTION_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["copyactionall"].format(showchange))

@client.Command(onlysudo=False, allowedits=False)
async def action(event):
    if event.is_sudo or event.is_bot: return
    acMode = event.client.DB.get_key("ACTION_MODE") or "OFF"
    acChats = event.client.DB.get_key("ACTION_CHATS") or []
    acType = event.client.DB.get_key("ACTION_TYPE") or "random"
    if not acType: return
    if acMode == "ON" or event.chat_id in acChats:
        if acType == "bandari":
            event.client.loop.create_task(sendbandariaction(event))
        elif acType == "random":
            RType = random.choice(client.functions.ACTIONS[2:])
            event.client.loop.create_task(sendaction(event, RType))
        else:
            event.client.loop.create_task(sendaction(event, acType))

@client.on(events.UserUpdate)
async def copyaction(event):
    if event.user_id == event.client.me.id: return
    cacMode = event.client.DB.get_key("COPYACTION_MODE") or "OFF"
    cacChats = event.client.DB.get_key("COPYACTION_CHATS") or []
    if cacMode == "ON" or event.chat_id in cacChats:
        ACTIONS = {
            "typing": event.typing,
            "game": event.playing,
            "photo": event.photo,
            "audio": event.audio,
            "video": event.video,
            "file": event.document,
            "sticker": event.sticker,
            "contact": event.contact,
            "location": event.geo,
            "record-video": event.recording,
            "record-audio": event.recording,
            "record-round": event.round,
        }
        for action in ACTIONS:
            if ACTIONS[action]:
                event.client.loop.create_task(sendaction(event, action))

async def sendaction(event, action):
    async with event.client.action(event.chat_id, action.lower()):
        await asyncio.sleep(3)

async def sendbandariaction(event):
    for action in client.functions.ACTIONS[2:]:
        async with event.client.action(event.chat_id, action):
            await asyncio.sleep(1)