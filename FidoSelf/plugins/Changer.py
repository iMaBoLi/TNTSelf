from FidoSelf import client

Modes = {
    "Name": "NAME_MODE",
    "Bio": "BIO_MODE",
    "Photo": "PHOTO_MODE",
    "DTimer": "TIMER_MODE",
    "Quicks": "QUICKS_MODE",
    "Monshi": "MONSHI_MODE",
    "AutoDelete": "AUTO_DELETE_MODE",
    "AutoReplace": "AUTO_REPLACE_MODE",
}
Pattern = ""
for mode in Modes:
    Pattern += mode + "|"
Pattern = Pattern[:-1]

@client.Cmd(pattern=f"(?i)^\{client.cmd}({Pattern}) (On|Off)$")
async def autodelete(event):
    await event.edit(client.get_string("Wait"))
    Mode = event.pattern_match.group(1).title()
    Change = event.pattern_match.group(2).lower()   
    client.DB.set_key(Modes[Mode], Change)
    Mode = client.get_string("Changer")[Mode]
    Change = client.get_string("Change_1") if Change == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("Changer_Main").format(Mode, Change))
