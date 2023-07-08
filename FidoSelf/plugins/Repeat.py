from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Name": "Repeat",
    "Info": {
        "Help": "To Setting Repeater And Send Messages Again!",
        "Commands": {
            "{CMD}Repeat <On-Off>": None,
            "{CMD}RepeatAll <On-Off>": None,
            "{CMD}NewRepeat <Text>": None,
            "{CMD}DelRepeat <Text>": None,
            "{CMD}RepeatList": None,
            "{CMD}CleanRepeatList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "repeatall": "**The Repeat Mode Has Been {}!**",
    "repeatchat": "**The Repeat Mode For This Chat Has Been {}!**",
    "newnot": "**The Text** ( `{}` ) **Already In Repeat List!**",
    "newadd": "**The Text** ( `{}` ) **Added To Repeat List!**",
    "delnot": "**The Text** ( `{}` ) **Not In Repeat List!**",
    "del": "**The Text** ( `{}` ) **Deleted From Repeat List!**",
    "empty": "**The Repeat List Is Empty!**",
    "list": "**The Repeat List:**\n\n",
    "aempty": "**The Repeat List Is Already Empty!**",
    "clean": "**The Repeat List Is Cleaned!**",
}

@client.Command(command="Repeat (On|Off)")
async def repeatchat(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = client.DB.get_key("REPEAT_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("REPEAT_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("REPEAT_CHATS", acChats)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["repeatchat"].format(showchange))

@client.Command(command="RepeatAll (On|Off)")
async def repeatall(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("REPEAT_MODE", change)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["repeatall"].format(showchange))
 
@client.Command(command="NewRepeat (.*)")
async def addrepeat(event):
    await event.edit(client.getstrings()["wait"])
    repeats = client.DB.get_key("REPEAT_LIST") or []
    newrepeat = str(event.pattern_match.group(1))
    if newrepeat in repeats:
        return await event.edit(client.getstrings(STRINGS)["newnot"].format(newrepeat))  
    repeats.append(newrepeat)
    client.DB.set_key("REPEAT_LIST", repeats)
    await event.edit(client.getstrings(STRINGS)["newadd"].format(newrepeat))
    
@client.Command(command="DelRepeat (.*)")
async def delrepeat(event):
    await event.edit(client.getstrings()["wait"])
    repeats = client.DB.get_key("REPEAT_LIST") or []
    newrepeat = str(event.pattern_match.group(1))
    if newrepeat not in repeats:
        return await event.edit(client.getstrings(STRINGS)["delnot"].format(newrepeat))  
    repeats.remove(newrepeat)
    client.DB.set_key("REPEAT_LIST", repeats)
    await event.edit(client.getstrings(STRINGS)["del"].format(newrepeat))

@client.Command(command="RepeatList")
async def repeatlist(event):
    await event.edit(client.getstrings()["wait"])
    repeats = client.DB.get_key("REPEAT_LIST") or []
    if not repeats:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for repeat in repeats:
        text += f"**{row} -** `{repeat}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanRepeatList")
async def cleanrepeats(event):
    await event.edit(client.getstrings()["wait"])
    repeats = client.DB.get_key("REPEAT_LIST") or []
    if not repeats:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("REPEAT_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])
 
@client.Command(onlysudo=False, allowedits=False)
async def repeat(event):
    if event.is_sudo or event.is_bot or not event.text: return
    remode = client.DB.get_key("REPEAT_MODE") or "OFF"
    rechats = client.DB.get_key("REPEAT_CHATS") or []
    repeats = client.DB.get_key("REPEAT_LIST") or []
    if not repeats: return
    if remode == "ON" or event.chat_id in rechats:
        for repeat in repeats:
            if repeat in event.text:
                await event.respond(repeat)