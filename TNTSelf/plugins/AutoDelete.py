from TNTSelf import client
import aiocron
import time

__INFO__ = {
    "Category": "Practical",
    "Name": "Auto Delete",
    "Info": {
        "Help": "To Setting Auto Delete Messages In Chats!",
        "Commands": {
            "{CMD}AutoDelete <On-Off>": {
                "Help": "To Turn On-Off Auto Delete",
            },
            "{CMD}SetDeleteSleep <Time>": {
                "Help": "To Set Auto Delete Sleep",
                "Input": {
                    "<Time>": "Time For Set (1-120)mins",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Auto Delete Message Has Been {}!**",
    "nosleep": "**{STR} The Auto Delete Sleep Must Be Between** ( `{}` ) **And** ( `{}` )",
    "setsleep": "**{STR} The Auto Delete Sleep Was Set To** ( `{}` )"
}

@client.Command(command="AutoDelete (On|Off)")
async def delautomode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("AUTODELETE_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))
    
@client.Command(command="SetDeleteSleep (\\d*)")
async def setautodeletesleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = int(event.pattern_match.group(1))
    if 1 > sleep > 120:
        return await event.edit(client.getstrings(STRINGS)["nosleep"].format(1, 60))
    sleep = sleep * 60
    event.client.DB.set_key("AUTODELETE_SLEEP", sleep)
    await event.edit(client.getstrings(STRINGS)["setsleep"].format(sleep))

@client.Command(allowedits=False, checkCmd=True)
async def autodelete(event):
    automode = event.client.DB.get_key("AUTODELETE_MODE") or "OFF"
    if automode == "ON":
        MSGS = event.client.DB.get_key("AUTODELETE_MSGS") or {}
        msginfo = str(event.chat_id) + ":" + str(event.id)
        MSGS.update({msginfo: time.time()})
        event.client.DB.set_key("AUTODELETE_MSGS", MSGS)

@aiocron.crontab("*/20 * * * * *")
async def autodeleter():
    for sinclient in client.clients:
        MSGS = sinclient.DB.get_key("AUTODELETE_MSGS") or {}
        if not MSGS: return
        for msg in MSGS:
            ltime = MSGS[msg]
            sleep = sinclient.DB.get_key("AUTODELETE_SLEEP") or 600
            if time.time() >= (ltime + int(sleep)):
                info = msg.split(":")
                try:
                    getmsg = await sinclient.get_messages(int(info[0]), ids=int(info[1]))
                    await getmsg.delete()
                except:
                    pass
                del MSGS[msg]
                sinclient.DB.set_key("AUTODELETE_MSGS", MSGS)