from FidoSelf import client
import aiocron
import time
import asyncio

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Auto",
    "Pluginfo": {
        "Help": "To Setting Send Auto Messages To Chats!",
        "Commands": {
            "{CMD}Auto <On-Off>": None,
            "{CMD}AutoAll <On-Off>": None,
            "{CMD}SetAuto <Mode>": None,
            "{CMD}SetAutoSleep <1-60min>"
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Send Auto Message Has Been {}!**",
    "notall": "**The Chat** ( {} ) **Already In Auto List!**",
    "addchat": "**The Chat** ( {} ) **Is Added To Auto List!**",
    "notin": "**The Chat** ( {} ) **Is Not In Auto List!**",
    "delchat": "**The Chat** ( {} ) **Deleted From Auto List!**",
    "empty": "**The Auto List Is Empty!**",
    "list": "**The Auto List:**\n\n",
    "aempty": "**The Auto List Is Already Empty**",
    "clean": "**The Auto List Has Been Cleaned!**",
    "nosleep": "**The Auto Sleep Must Be Between** ( `{}` ) **And** ( `{}` )",
    "setsleep": "**The Auto Sleep Was Set To** ( `{}` )",
    "saveauto": "**The Auto Message Was Saved!**",
    "notauto": "**The Auto Message Is Not Saved!**",
}

@client.Command(command="Auto (On|Off)")
async def autoall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("AUTO_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="AddAuto ?(.*)?")
async def addauto(event):
    await event.edit(client.STRINGS["wait"])
    result, chatid = await event.chatid(event.pattern_match.group(1))
    if not result and str(chatid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not chatid:
        return await event.edit(client.STRINGS["getid"]["UC"])
    autos = client.DB.get_key("AUTO_CHATS") or {}
    if chatid in autos:
        return await event.edit(STRINGS["notall"].format(chatid))
    autos.update({chatid: time.time()})
    client.DB.set_key("AUTO_CHATS", autos)
    await event.edit(STRINGS["addchat"].format(chatid))
    
@client.Command(command="DelAuto ?(.*)?")
async def delauto(event):
    await event.edit(client.STRINGS["wait"])
    result, chatid = await event.chatid(event.pattern_match.group(1))
    if not result and str(chatid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not chatid:
        return await event.edit(client.STRINGS["getid"]["UC"])
    autos = client.DB.get_key("AUTO_CHATS") or {}
    if chatid not in autos:
        return await event.edit(STRINGS["notin"].format(chatid))  
    del autos[chatid]
    client.DB.set_key("AUTO_CHATS", autos)
    await event.edit(STRINGS["delchat"].format(chatid))
    
@client.Command(command="AutoList")
async def autolist(event):
    await event.edit(client.STRINGS["wait"])
    autos = client.DB.get_key("AUTO_CHATS") or []
    if not autos:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for auto in autos:
        text += f"**{row} -** `{auto}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanAutoList")
async def cleanautolist(event):
    await event.edit(client.STRINGS["wait"])
    autos = client.DB.get_key("AUTO_CHATS") or []
    if not autos:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("AUTO_CHATS")
    await event.edit(STRINGS["clean"])

@client.Command(command="SetAuto")
async def setauto(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["replyMedia"]["NotAll"])
    info = await event.reply_message.save()
    client.DB.set_key("AUTO_MESSAGE", info)
    await event.edit(STRINGS["saveauto"])
 
@client.Command(command="GetAuto")
async def getauto(event):
    await event.edit(client.STRINGS["wait"])
    info = client.DB.get_key("AUTO_MESSAGE")
    if not info:
        return await event.edit(STRINGS["notsave"])
    getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await event.respond(getmsg)
    await event.delete()
    
client.Command(command="SetAutoSleep (\d*)")
async def setautosleep(event):
    await event.edit(STRINGS["wait"])
    sleep = event.pattern_match.group(1)
    if 1 > sleep > 60:
        return await event.edit(STRINGS["nosleep"].format(1, 60))
    sleep = sleep * 60
    client.DB.set_key("AUTO_SLEEP", sleep)
    await event.edit(STRINGS["setsleep"].format(sleep))

@aiocron.crontab("*/1 * * * *")
async def autosender():
    amode = client.DB.get_key("AUTO_ALL") or "off"
    achats = client.DB.get_key("AUTO_CHATS") or []
    amessage = client.DB.get_key("AUTO_MESSAGE") or {}
    if not amessage: return
    if amode == "on":
        for chatid in achats:
            ltime = achats[chatid]
            sleep = client.DB.get_key("AUTO_SLEEP") or 600
            if time.time() >= (ltime + int(sleep)):
                getmsg = await client.get_messages(int(amessage["chat_id"]), ids=int(amessage["msg_id"]))
                getmsg.text = await client.AddVars(getmsg.text)
                try:
                    await client.send_message(chatid, getmsg)
                    achats[chatid] = time.time()
                    client.DB.set_key("AUTO_CHATS", achats)
                    await asyncio.sleep(2)
                except:
                    pass