from FidoSelf import client
from telethon import functions, types
import asyncio
import random

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Poker",
    "Pluginfo": {
        "Help": "To Setting Send Poker Sticker To Pokers!",
        "Commands": {
            "{CMD}Poker <On-Off>": "Send Poker For This Chat!",
            "{CMD}PokerAll <On-Off>": "Send Poker For All Chats!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "reactall": "**The Poker Mode Has Been {}!**",
    "reactchat": "**The Poker Mode For This Chat Has Been {}!**",
}

@client.Command(command="Poker (On|Off)")
async def Pokerchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    acChats = client.DB.get_key("POKER_CHATS") or []
    chatid = event.chat_id
    if change == "on":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("POKER_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("POKER_CHATS", acChats)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["reactchat"].format(ShowChange))

@client.Command(command="PokerAll (On|Off)")
async def Pokerall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("POKER_ALL", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["reactall"].format(ShowChange))
 
@client.Command(onlysudo=False, alowedits=False)
async def Poker(event):
    if event.is_sudo or event.is_bot or not event.text or "😐" not in event.text: return
    pomode = client.DB.get_key("POKER_ALL") or "off"
    pochats = client.DB.get_key("POKER_CHATS") or []
    if pomode == "on" or event.chat_id in pochats:
        await event.reply("😐")