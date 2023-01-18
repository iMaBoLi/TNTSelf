from FidoSelf import client
from FidoSelf.languages import install_lang, LANGUAGES, LANGS, MAINLANGS

@client.Command(pattern=f"(?i)^\{client.cmd}SetLang (.*)$")
async def setlanguage(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1).lower()
    if lang not in LANGUAGES:
        return await event.edit(client.get_string("Language_1").format(lang))
    client.DB.set_key("LANGUAGE", lang)
    client.lang = lang
    langname = f"{lang} - {LANGS[lang].title()}"
    await event.edit(client.get_string("Language_2").format(langname))

@client.Command(pattern=f"(?i)^\{client.cmd}InstallLang (.*)$")
async def installlanguage(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1).lower()
    if lang in MAINLANGS:
        return await event.edit(client.get_string("Language_15"))
    if lang not in LANGS:
        return await event.edit(client.get_string("Language_3").format(lang))
    langname = f"{lang} - {LANGS[lang].title()}"
    await event.edit(client.get_string("Language_4").format(langname))
    install = await client.loop.run_in_executor(None, install_lang, lang)
    langs = client.DB.get_key("INSTALL_LANGS") or []
    if lang not in langs:
        langs.append(lang)
        client.DB.set_key("INSTALL_LANGS", langs)
    if install == "Installed":
        await event.edit(client.get_string("Language_5").format(langname))
    elif install == "Updated":
        await event.edit(client.get_string("Language_6").format(langname))

@client.Command(pattern=f"(?i)^\{client.cmd}RemoveLang (.*)$")
async def removelanguage(event):
    await event.edit(client.get_string("Wait"))
    lang = event.pattern_match.group(1).lower()
    if lang in MAINLANGS:
        return await event.edit(client.get_string("Language_15"))
    if lang not in LANGUAGES:
        return await event.edit(client.get_string("Language_7").format(lang))
    langname = f"{lang} - {LANGS[lang].title()}"
    langs = client.DB.get_key("INSTALL_LANGS") or []
    if lang in langs:
        langs.remove(lang)
        client.DB.set_key("INSTALL_LANGS", langs)
    del LANGUAGES[lang]
    await event.edit(client.get_string("Language_8").format(langname))

@client.Command(pattern=f"(?i)^\{client.cmd}ReloadLangs$")
async def removelanguage(event):
    await event.edit(client.get_string("Wait"))
    others = client.DB.get_key("INSTALL_LANGS") or []
    if not others:
        return await event.edit(client.get_string("Language_9"))
    await event.edit(client.get_string("Language_10"))
    client.loop.create_task(reload(event, others))

async def reload(event, others):
    langnames = "\n"
    for lang in others:
        install_lang(lang)
        langname = f"{lang} - {LANGS[lang].title()}"
        await event.edit(client.get_string("Language_11").format(langname))
        langnames += langname + "\n"
    await event.edit(client.get_string("Language_12").format(langnames))

@client.Command(pattern=f"(?i)^\{client.cmd}LangList$")
async def alllanguages(event):
    await event.edit(client.get_string("Wait"))
    text = client.get_string("Language_13")
    row = 1
    for lang in LANGS:
        text += f"**{row}-** `{lang}`|{LANGS[lang].title()}\n"
        row += 1
    await event.edit(text)

@client.Command(pattern=f"(?i)^\{client.cmd}Languages$")
async def languages(event):
    await event.edit(client.get_string("Wait"))
    text = client.get_string("Language_14")
    row = 1
    for lang in LANGUAGES:
        text += f"**{row}-** `{lang}`|{LANGS[lang].title()}\n"
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
            "{CMD}RemoveLang <Text>": "To Remove A Language In Bot",
            "{CMD}ReloadLangs": "To Reload And Install Saved Languages In Bot",
            "{CMD}Languages": "To Show Installed Languages",
            "{CMD}LangList": "To Show Available Languages",
        },
    }
})
