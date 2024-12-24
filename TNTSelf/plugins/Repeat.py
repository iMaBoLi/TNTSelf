from TNTSelf import client

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
    "repeatall": "**{STR} The Repeat Mode Has Been {}!**",
    "repeatchat": "**{STR} The Repeat Mode For This Chat Has Been {}!**",
    "newnot": "**{STR} The Text** ( `{}` ) **Already In Repeat List!**",
    "newadd": "**{STR} The Text** ( `{}` ) **Added To Repeat List!**",
    "delnot": "**{STR} The Text** ( `{}` ) **Not In Repeat List!**",
    "del": "**{STR} The Text** ( `{}` ) **Deleted From Repeat List!**",
    "empty": "**{STR} The Repeat List Is Empty!**",
    "list": "**{STR} The Repeat List:**\n\n",
    "aempty": "**{STR} The Repeat List Is Already Empty!**",
    "clean": "**{STR} The Repeat List Is Cleaned!**"
}

@client.Command(command="Repeat (On|Off)")
async def repeatchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = event.client.DB.get_key("REPEAT_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            event.client.DB.set_key("REPEAT_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            event.client.DB.set_key("REPEAT_CHATS", acChats)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["repeatchat"].format(showchange))

@client.Command(command="RepeatAll (On|Off)")
async def repeatall(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("REPEAT_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["repeatall"].format(showchange))
 
@client.Command(command="NewRepeat (.*)")
async def addrepeat(event):
    await event.edit(client.STRINGS["wait"])
    repeats = event.client.DB.get_key("REPEAT_LIST") or []
    newrepeat = str(event.pattern_match.group(1))
    if newrepeat in repeats:
        return await event.edit(client.getstrings(STRINGS)["newnot"].format(newrepeat))  
    repeats.append(newrepeat)
    event.client.DB.set_key("REPEAT_LIST", repeats)
    await event.edit(client.getstrings(STRINGS)["newadd"].format(newrepeat))
    
@client.Command(command="DelRepeat (.*)")
async def delrepeat(event):
    await event.edit(client.STRINGS["wait"])
    repeats = event.client.DB.get_key("REPEAT_LIST") or []
    newrepeat = str(event.pattern_match.group(1))
    if newrepeat not in repeats:
        return await event.edit(client.getstrings(STRINGS)["delnot"].format(newrepeat))  
    repeats.remove(newrepeat)
    event.client.DB.set_key("REPEAT_LIST", repeats)
    await event.edit(client.getstrings(STRINGS)["del"].format(newrepeat))

@client.Command(command="RepeatList")
async def repeatlist(event):
    await event.edit(client.STRINGS["wait"])
    repeats = event.client.DB.get_key("REPEAT_LIST") or []
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
    await event.edit(client.STRINGS["wait"])
    repeats = event.client.DB.get_key("REPEAT_LIST") or []
    if not repeats:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("REPEAT_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])
 
@client.Command(onlysudo=False, allowedits=False)
async def repeat(event):
    if event.is_sudo or event.is_bot or not event.text: return
    remode = event.client.DB.get_key("REPEAT_MODE") or "OFF"
    rechats = event.client.DB.get_key("REPEAT_CHATS") or []
    repeats = event.client.DB.get_key("REPEAT_LIST") or []
    if not repeats: return
    if remode == "ON" or event.chat_id in rechats:
        for repeat in repeats:
            if repeat in event.text:
                await event.respond(repeat)