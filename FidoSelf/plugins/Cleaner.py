from FidoSelf import client

LISTS = {
    "NAMES": ["Names", "Namelist"],
    "BIOS": ["Bios", "Biolist"],
    "PHOTOS": ["Photos", "Photolist"],
    "FONTS": ["Fonts", "Fontlist"],
    "TEXT_TIMES": ["Texttimes", "Texttimelist"],
    "BLACKS": ["Blacks", "Blacklist"],
    "WHITES": ["Whites", "Whitelist"],
    "ECHOS": ["Echos", "Echolist"],
    "EMOJIES": ["Emojis", "Emojilist"],
    "SAVES": ["Saves", "Savelist"],
    "FILTER_PVS": ["Filterpvs", "Filterpvlist"],
}
Pattern = ""
for LIST in LISTS:
    Pats = LISTS[LIST]
    for Pat in Pats:
        Pattern += Pat + "|"
Pattern = Pattern[:-1]

@client.Cmd(pattern=f"(?i)^\{client.cmd}Clean ({Pattern})$")
async def cleaner(event):
    await event.edit(client.get_string("Wait"))
    inlist = event.pattern_match.group(1).title()
    for LIST in LISTS: 
        if inlist in LISTS[LIST]: break
    lists = client.DB.get_key(LIST) or None
    mode = client.get_string("Cleaner")[LIST]
    if not lists:
        return await event.edit(client.get_string("Cleaner_Not").format(mode))
    client.DB.del_key(LIST)
    await event.edit(client.get_string("Cleaner_Main").format(mode))
