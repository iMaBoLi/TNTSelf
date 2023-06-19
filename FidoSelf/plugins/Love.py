from FidoSelf import client
import aiocron

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Love",
    "Pluginfo": {
        "Help": "To Manage Users On Love List And Send Love Message!",
        "Commands": {
            "{CMD}Love <On-Off>": None,
            "{CMD}AddLove <Reply|Userid|Username>": None,
            "{CMD}DelLove <Reply|Userid|Username>": None,
            "{CMD}LoveList": None,
            "{CMD}CleanLoveList": None,
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
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    loves = client.DB.get_key("LOVES") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
    if userid in loves:
        return await event.edit(STRINGS["notall"].format(mention))
    loves.append(userid)
    client.DB.set_key("LOVES", loves)
    await event.edit(STRINGS["add"].format(mention))
    
@client.Command(command="DelLove ?(.*)?"))
async def dellove(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    loves = client.DB.get_key("LOVES") or []
    info = await client.get_entity(userid)
    mention = client.mention(info)
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
    if not event.is_reply:
        return await event.edit(client.STRINGS["replyMedia"]["NotAll"])
    info = await event.reply_message.save()
    client.DB.set_key("LOVE_MESSAGE", info)
    await event.edit(STRINGS["setlove"])

@client.Command(command="GetLove")
async def getlove(event):
    await event.edit(client.STRINGS["wait"])
    mlove = client.DB.get_key("LOVE_MESSAGE") or {}
    if not mlove:
        return await event.edit(STRINGS["notlove"])
    getmsg = await client.get_messages(int(mlove["chat_id"]), ids=int(mlove["msg_id"]))
    await event.respond(getmsg)
    await event.delete()
    
@aiocron.crontab("*/24 * * * * *")
async def autolove():
    lmode = client.DB.get_key("LOVE_MODE") or "OFF"
    if lmode == "ON":
        mlove = client.DB.get_key("LOVE_MESSAGE") or {}
        loves = client.DB.get_key("LOVES") or []
        for love in loves:
            if mlove:
                getmsg = await client.get_messages(int(mlove["chat_id"]), ids=int(mlove["msg_id"]))
                getmsg.text = await client.AddVars(getmsg.text)
                await client.send_message(int(love), getmsg)
            else:
                await client.send_message(int(love), "**- 00:00 ❤️**")