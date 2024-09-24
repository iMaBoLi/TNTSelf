from FidoSelf import client
from FidoSelf.functions.strings import STRINGS

STRINGS = {
    "EN": {
        "setlang": "**{STR} The Self Language Was Set To English!**",
    },
    "FA": {
        "setlang": "**{STR} زبان ربات با موفقیت روی فارسی تنظیم شد!**",
    },
}

@client.Command(command="SetLang (En|Fa)")
async def setlanguage(event):
    await event.edit(client.STRINGS["wait"])
    lang = event.pattern_match.group(1).upper()
    client.DB.set_key("LANGUAGE", lang)
    await event.edit(client.getstring(STRINGS, "setlang"))
    setattr(client, "STRINGS", STRINGS[lang])