from FidoSelf import client

STRINGS = {
    "Change": "**The {} Has Been {}!**",
    "Not": "**The {} iS Already {}!**",
    "Modes": {
        "Name": ["Name Mode", "NAME_MODE"],
        "Bio": ["Bio Mode", "BIO_MODE"],
        "Photo": ["Photo Mode", "PHOTO_MODE"],
        "Dtimer": ["Download Timer Medias", "TIMER_MODE"],
        "Quicks": ["Quicks Mode", "QUICKS_MODE"]
        "Monshi": ["Monshi Self", "MONSHI_MODE"],
        "Autodelete": ["Auto Delete Messages", "AUTO_DELETE_MODE"],
        "Autoreplace": ["Auto Replace Mode", "AUTO_REPLACE_MODE"],
        "Autosay": ["Auto Say Mode", "AUTO_SAY_MODE"],
        "Mutepv": ["Mute Pv", "MUTE_PV"],
        "Lockpv": ["Lock Pv", "LOCK_PV"],
        "Antispampv": ["Anti Spam Pv", "ANTISPAM_PV"],
        "Readall": ["MarkRead All", "READALL_MODE"],
        "Readpv": ["MarkRead Pvs", "READPV_MODE"],
        "Readgp": ["MarkRead Groups", "READGP_MODE"],
        "Readch": ["MarkRead Channels", "READCH_MODE"],
    }
}

ENPAT = ""
for mode in STRINGS["Modes"]:
    ENPAT += mode + "|"
ENPAT = ENPAT[:-1]

@client.Command(command="({ENPAT}) (On|Off)")
async def changer(event):
    await event.edit(client.STRINGS["wait"])
    Mode = event.pattern_match.group(1).title()
    Change = event.pattern_match.group(2).lower()
    EDMode = STRINGS["Modes"][Mode][0]
    DBMode = STRINGS["Modes"][Mode][1]
    stats = client.DB.get_key(DBMode)
    if stats == Change:
        text = STRINGS["Not"].format(EDMode, Change)
        return await event.edit(text)
    client.DB.set_key(DBMode, Change)
    Change = client.STRINGS["On"] if Change == "on" else client.STRINGS["Off"]
    text = STRINGS["Change"].format(EDMode, Change)
    await event.edit(text)