from FidoSelf import client

STRINGS = {
    "EN": {
        "change": "^{STR} The Language Was Changed To English!$",
        "already": "^{STR} The Language Is Already English!$",
    },
    "FA": {
        "change": "^{STR} زبان با موفقیت به  فارسی تغییر کرد!$",
        "already": "^{STR} زبان ربات از قبل فارسی است!$",
    },
}

@client.Command(
    commands={
        "EN": "Set(En|Fa)",
        "FA": "Set(En|Fa)",
     }
)
async def language(event):
    text = client.get_string("wait")
    await event.edit(text)
    lang = event.pattern_match.group(1).upper()
    if lang == client.LANG:
        text = client.get_string("already", STRINGS)
        return await event.edit(text)
    client.DB.set_key("LANGUAGE", lang)
    client.LANG = lang
    load_plugins(client.PLUGINS, reload=True)
    text = client.get_string("change", STRINGS)
    await event.edit(text)
