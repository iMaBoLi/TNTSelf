from FidoSelf import client
from FidoSelf.strings import LANGUAGES, LANGS, install_lang

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetLang (.*)$")
async def setlanguage(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1).lower()
    if lang not in LANGUAGES:
        return await event.edit(client.get_string("Language_1").format(lang))
    client.DB.set_key("LANGUAGE", lang)
    client.lang = lang
    langname = f"{lang} - {LANGS[lang]}"
    await event.edit(client.get_string("Language_2").format(langname)

@client.Cmd(pattern=f"(?i)^\{client.cmd}InstallLang (.*)$")
async def installlanguage(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1).lower()
    install = install_lang(lang)
    if install == "Installed":
        langs = client.DB.get_key("INSTALL_LANGS") or []
        if lang not in langs:
            langs.append(lang)
            client.DB.set_key("INSTALL_LANGS", langs)
        langname = f"{lang} - {LANGS[lang]}"
        return await event.edit(client.get_string("Language_3").format(langname))
    elif install == "Updated":
        langs = client.DB.get_key("INSTALL_LANGS") or []
        if lang not in langs:
            langs.append(lang)
            client.DB.set_key("INSTALL_LANGS", langs)
        langname = f"{lang} - {LANGS[lang]}"
        return await event.edit(client.get_string("Language_4").format(langname))
    elif install == "NotFound":
        return await event.edit(client.get_string("Language_5").format(lang))

@client.Cmd(pattern=f"(?i)^\{client.cmd}LangList$")
async def alllanguages(event):
    await event.edit(client.get_string("Wait"))
    text = client.get_string("Language_6")
    row = 1
    for lang in LANGS:
        text += f"**{row}-** `{lang}` | **{LANGS[lang]}**\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}Languages$")
async def languages(event):
    await event.edit(client.get_string("Wait"))
    text = client.get_string("Language_7")
    row = 1
    for lang in LANGUAGES:
        text += f"**{row}-** `{lang}` | **{LANGS[lang]}**\n"
        row += 1
    await event.edit(text)

category = "Settings"
plugin = "Language"
note = "Install And Setting Bot Language!"
client.HELP.update({
    plugin: {
        "category": category,
        "note": note,
        "commands": {
            "{CMD}SetLang <Text>": "To Setting Bot Language To Other Languages",
            "{CMD}InstallLang <Text>": "To Install New Language In Bot",
            "{CMD}Languages": "To Show Installed Languages",
            "{CMD}LangList": "To Show Available Languages",
        },
    }
})
