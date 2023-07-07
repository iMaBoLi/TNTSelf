from FidoSelf import client
from jdatetime import datetime
import aiocron
import random

__INFO__ = {
    "Category": "Manage",
    "Name": "Love",
    "Info": {
        "Help": "To Manage Users On Love List And Send Love Message!",
        "Commands": {
            "{CMD}AddLove": {
                "Help": "To Add User On Love List",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelLove": {
                "Help": "To Delete User From Love List",
                "Getid": "You Can Reply To User Or Input UserID/UserName",
            },
            "{CMD}LoveList": {
                "Help": "To Getting Love List",
            },
            "{CMD}CleanLoveList": {
                "Help": "To Cleaning Love List",
            },
            "{CMD}SetLove": {
                "Help": "To Set Love Message",
                "Reply": ["Message", "Media"],
                "Vars": ["TIME", "DATE", "HEART", "NAME", "MENTION", "USERNAME"],
            },
            "{CMD}DeleteLove": {
                "Help": "To Delete Love Message",
            },
            "{CMD}GetLove": {
                "Help": "To Getting Love Message",
            },
            "{CMD}AddLoveTime <Time>": {
                "Help": "To Add Time To Love Time List",
                "Input": {
                    "<Time>": "Time String Ex -> 23:59",
                },
            },
            "{CMD}DelLoveTime <Time>": {
                "Help": "To Delete Time From Love Time List",
                "Input": {
                    "<Time>": "Time String Ex -> 23:59",
                },
            },
            "{CMD}LoveTimeList": {
                "Help": "To Getting Love Time List",
            },
            "{CMD}CleanLoveTimeList": {
                "Help": "To Cleaning Love Time List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Love Mode Has Been {}!**",
    "notall": "**The User** ( {} ) **Already In Love List!**",
    "add": "**The User** ( {} ) **Is Added To Love List!**",
    "notin": "**The User** ( {} ) **Is Not In Love List!**",
    "del": "**The User** ( {} ) **Deleted From Love List!**",
    "empty": "**The Love List Is Empty!**",
    "list": "**The Love List:**\n\n",
    "aempty": "**The Love List Is Already Empty**",
    "clean": "**The Love List Has Been Cleaned!**",
    "setlove": "**The Love Message Has Been Saved!**",
    "notlove": "**The Love Message Is Not Saved!**",
    "dellove": "**The Love Message Has Been Removed!**",
    "newnot": "**The Time** ( `{}` ) **Already In Love Time List!**",
    "newadd": "**The Time** ( `{}` ) **Added To Love Time List!**",
    "delnot": "**The Time** ( `{}` ) **Not In Love Time List!**",
    "deltime": "**The Time** ( `{}` ) **Deleted From Love Time List!**",
    "emptytime": "**The Love Time List Is Empty!**",
    "listtime": "**The Love Time List:**\n\n",
    "aemptytime": "**The Love Time List Is Already Empty!**",
    "cleantime": "**The Love Time List Is Cleaned!**",
}

@client.Command(command="Love (On|Off)")
async def lovemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("LOVE_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="AddLove ?(.*)?")
async def addlove(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    loves = client.DB.get_key("LOVES") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid in loves:
        return await event.edit(STRINGS["notall"].format(mention))
    loves.append(userid)
    client.DB.set_key("LOVES", loves)
    await event.edit(STRINGS["add"].format(mention))
    
@client.Command(command="DelLove ?(.*)?")
async def dellove(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    loves = client.DB.get_key("LOVES") or []
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    if userid not in loves:
        return await event.edit(STRINGS["notin"].format(mention))  
    loves.remove(userid)
    client.DB.set_key("LOVES", loves)
    await event.edit(STRINGS["del"].format(mention))
    
@client.Command(command="LoveList")
async def lovelist(event):
    await event.edit(client.STRINGS["wait"])
    loves = client.DB.get_key("LOVES") or []
    if not loves:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for love in loves:
        text += f"**{row} -** `{love}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanLoveList")
async def cleanlovelist(event):
    await event.edit(client.STRINGS["wait"])
    loves = client.DB.get_key("LOVES") or []
    if not loves:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("LOVES")
    await event.edit(STRINGS["clean"])

@client.Command(command="SetLove")
async def savelove(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply():
        return await event.edit(reply)
    info = await event.reply_message.save()
    client.DB.set_key("LOVE_MESSAGE", info)
    await event.edit(STRINGS["setlove"])

@client.Command(command="DeleteLove")
async def deletelove(event):
    await event.edit(client.STRINGS["wait"])
    mlove = client.DB.get_key("LOVE_MESSAGE") or {}
    if not mlove:
        return await event.edit(STRINGS["notlove"])
    client.DB.del_key("LOVE_MESSAGE")
    await event.edit(STRINGS["dellove"])

@client.Command(command="GetLove")
async def getlove(event):
    await event.edit(client.STRINGS["wait"])
    mlove = client.DB.get_key("LOVE_MESSAGE") or {}
    if not mlove:
        return await event.edit(STRINGS["notlove"])
    getmsg = await client.get_messages(int(mlove["chat_id"]), ids=int(mlove["msg_id"]))
    await event.respond(getmsg)
    await event.delete()

@client.Command(command="AddLoveTime (.*)")
async def addlovetime(event):
    await event.edit(client.STRINGS["wait"])
    times = client.DB.get_key("LOVE_TIMES") or []
    newtime = str(event.pattern_match.group(1))
    if newtime in times:
        return await event.edit(STRINGS["newnot"].format(newtime))  
    times.append(newtime)
    client.DB.set_key("LOVE_TIMES", times)
    await event.edit(STRINGS["newadd"].format(newtime))
    
@client.Command(command="DelLoveTime (.*)")
async def dellovetime(event):
    await event.edit(client.STRINGS["wait"])
    times = client.DB.get_key("LOVE_TIMES") or []
    newtime = str(event.pattern_match.group(1))
    if newtime not in times:
        return await event.edit(STRINGS["delnot"].format(newtime))  
    times.remove(newtime)
    client.DB.set_key("LOVE_TIMES", times)
    await event.edit(STRINGS["deltime"].format(newtime))

@client.Command(command="LoveTimeList")
async def lovetimelist(event):
    await event.edit(client.STRINGS["wait"])
    times = client.DB.get_key("LOVE_TIMES") or []
    if not times:
        return await event.edit(STRINGS["emptytime"])
    text = STRINGS["listtime"]
    row = 1
    for repeat in times:
        text += f"**{row} -** `{repeat}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanLoveTimeList")
async def cleanlovetimes(event):
    await event.edit(client.STRINGS["wait"])
    times = client.DB.get_key("LOVE_TIMES") or []
    if not times:
        return await event.edit(STRINGS["aemptytime"])
    client.DB.del_key("LOVE_TIMES")
    await event.edit(STRINGS["cleantime"])

@aiocron.crontab("*/1 * * * *")
async def autolove():
    jtime = datetime.now()
    times = client.DB.get_key("LOVE_TIMES") or []
    if jtime.strftime("%H:%M") not in times: return
    lmode = client.DB.get_key("LOVE_MODE") or "OFF"
    if lmode == "ON":
        mlove = client.DB.get_key("LOVE_MESSAGE") or {}
        loves = client.DB.get_key("LOVES") or []
        if not mlove: return
        for love in loves:
            info = await client.get_entity(int(love))
            getmsg = await client.get_messages(int(mlove["chat_id"]), ids=int(mlove["msg_id"]))
            VARS = {
                "TIME": jtime.strftime("%H:%M"),
                "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
                "HEART": random.choice(client.functions.HEARTS),
                "NAME": info.first_name,
                "MENTION": client.functions.mention(info),
                "USERNAME": info.username,
            }
            for VAR in VARS:
                getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
            await client.send_message(int(love), getmsg)