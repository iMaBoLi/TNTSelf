from FidoSelf import client

__INFO__ = {
    "Category": "Pv",
    "Name": "Filter Pv",
    "Info": {
        "Help": "To Filter Words In Pv And Delete!",
        "Commands": {
            "{CMD}AddFilterPv <Text>": None,
            "{CMD}DelFilterPv <Text>": None,
            "{CMD}FilterPvList": None,
            "{CMD}CleanFilterPvList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
        "notall": "**The Word** ( `{}` ) **Already In Words Filter Pv List!**",
        "add": "**The Word** ( `{}` ) **Is Added To Words Filter Pv List!**",
        "notin": "**The Word** ( `{}` ) **Is Not In Words Filter Pv List!**",
        "del": "**The Word** ( `{}` ) **Deleted From Words Filter Pv List!**",
        "empty": "**The Words Filter Pv List Is Empty!**",
        "list": "**The Words Filter Pv List:**\n\n",
        "aempty": "**The Words Filter Pv List Is Already Empty!**",
        "clean": "**The Words Filter Pv List Has Been Cleaned!**",
}

@client.Command(command="AddFilterPv (.*)")
async def addfilterpv(event):
    await event.edit(client.STRINGS["wait"])
    word = str(event.pattern_match.group(1))
    filterpvs = client.DB.get_key("FILTERPV_WORDS") or []
    if word in filterpvs:
        return await event.edit(STRINGS["notall"].format(word))
    filterpvs.append(word)
    client.DB.set_key("FILTERPV_WORDS", filterpvs)
    await event.edit(STRINGS["add"].format(word))
    
@client.Command(command="DelFilterPv (.*)")
async def delfilterpv(event):
    await event.edit(client.STRINGS["wait"])
    word = str(event.pattern_match.group(1))
    filterpvs = client.DB.get_key("FILTERPV_WORDS") or []
    if word not in filterpvs:
        return await event.edit(STRINGS["notin"].format(word))
    filterpvs.remove(word)
    client.DB.set_key("FILTERPV_WORDS", filterpvs)
    await event.edit(STRINGS["del"].format(word))
    
@client.Command(command="FilterPvList")
async def filterpvlist(event):
    await event.edit(client.STRINGS["wait"])
    filterpvs = client.DB.get_key("FILTERPV_WORDS") or []
    if not filterpvs:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for word in filterpvs:
        text += f"**{row} -** `{word}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanFilterPvList")
async def cleanfilterpv(event):
    await event.edit(client.STRINGS["wait"])
    filterpvs = client.DB.get_key("FILTERPV_WORDS") or []
    if not filterpvs:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("FILTERPV_WORDS")
    await event.edit(STRINGS["clean"])
    
@client.Command(onlysudo=False, allowedits=False)
async def filterpv(event):
    if not event.text or not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    words = client.DB.get_key("FILTERPV_WORDS") or []
    if not words: return
    for word in words:
        if word in event.text:
            await event.delete()