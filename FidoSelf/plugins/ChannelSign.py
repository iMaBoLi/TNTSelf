from FidoSelf import client
from telethon import events, functions
from jdatetime import datetime
import aiocron
import random

__INFO__ = {
    "Category": "Groups",
    "Name": "Channel Sign",
    "Info": {
        "Help": "To Manage Sign Text For Your Channel Posts!",
        "Commands": {
            "{CMD}ChSign <On-Off>": {
                "Help": "To Turn On-Off Channel Sign Message",
            },
            "{CMD}SetChSign <Text>": {
                "Help": "To Set Channel Sign Message",
                "Input": {
                    "<Text>": "Sign Text",
                },
            },
            "{CMD}DelChSign": {
                "Help": "To Delete Channel Sign Message",
            },
            "{CMD}ChSignList": {
                "Help": "To Getting Channel Sign List",
            },
            "{CMD}CleanChSignList": {
                "Help": "To Cleaning Channel Sign List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Channel Sign Mode Has Been {}!**",
    "setchsign": "**{STR} The Sign Message For This Channel Was Set To** ( `{}` )",
    "notsave": "**{STR} The Sign Message For This Channel Is Not Saved!**",
    "delchsign": "**{STR} The Sign Message For This Channel Has Been Removed!**",
    "empty": "**{STR} The Channel Sign List Is Empty!**",
    "list": "**{STR} The Channel Sign List:**\n\n",
    "aempty": "**{STR} The Channel Sign List Is Already Empty**",
    "clean": "**{STR} The Channel Sign List Has Been Cleaned!**"
}

@client.Command(command="ChSign (On|Off)")
async def chsignmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("CHSIGN_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="SetChSign ([\s\S]*)")
async def setchsign(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_ch:
        return await event.edit(client.STRINGS["only"]["Channel"])
    signtext = event.pattern_match.group(1)
    chsigns = client.DB.get_key("CHSIGN_CHATS") or {}
    chsigns.update({event.chat_id: signtext})
    client.DB.set_key("CHSIGN_CHATS", chsigns)
    await event.edit(client.getstrings(STRINGS)["setchsign"].format(signtext))
    
@client.Command(command="DelChSign")
async def delchsign(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_ch:
        return await event.edit(client.STRINGS["only"]["Channel"])
    chsigns = client.DB.get_key("CHSIGN_CHATS") or {}
    if event.chat_id not in chsigns:
        return await event.edit(client.getstrings(STRINGS)["notsave"])  
    del chsigns[event.chat_id]
    client.DB.set_key("CHSIGN_CHATS", chsigns)
    await event.edit(client.getstrings(STRINGS)["delchsign"])
    
@client.Command(command="ChSignList")
async def chsignlist(event):
    await event.edit(client.STRINGS["wait"])
    chsigns = client.DB.get_key("CHSIGN_CHATS") or {}
    if not chsigns:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for chsign in chsigns:
        text += f"**{row} -** `{chsign}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanChSignList")
async def cleanchsignlist(event):
    await event.edit(client.STRINGS["wait"])
    chsigns = client.DB.get_key("CHSIGN_CHATS") or {}
    if not chsigns:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("CHSIGN_CHATS")
    await event.edit(client.getstrings(STRINGS)["clean"])
    
@client.Command(onlysudo=False)
async def autochsign(event):
    if not event.is_ch: return
    chsignmode = client.DB.get_key("CHSIGN_MODE") or "OFF"
    chats = client.DB.get_key("CHSIGN_CHATS") or {}
    if chsignmode == "ON" and event.chat_id in chats:
        signtext = chats[event.chat_id]
        newtext = signtext if not event.text else event.text + "\n\n" + signtext
        await event.edit(newtext)