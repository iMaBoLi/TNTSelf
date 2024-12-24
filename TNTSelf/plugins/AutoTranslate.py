from TNTSelf import client
from deep_translator import GoogleTranslator

__INFO__ = {
    "Category": "Practical",
    "Name": "Auto Translate",
    "Info": {
        "Help": "To Translate Your Texts And Edit Messages!",
        "Commands": {
            "{CMD}AutoTr <On-Off>": None,
            "{CMD}SetTrLang <Lang>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Auto Translate Mode Has Been {}!**",
    "notlang": "**{STR} The Language** ( `{}` ) **Is Not Available!**",
    "setlang": "**{STR} The Auto Translate Language Was Set To** ( `{}` )"
}

@client.Command(command="AutoTr (On|Off)")
async def settrauto(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("AUTOTR_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="SetTrLang (.*)")
async def settrlang(event):
    await event.edit(client.STRINGS["wait"])
    lang = event.pattern_match.group(1).lower()
    if lang not in client.functions.TRLANGS:
        return await event.edit(client.getstrings(STRINGS)["notlang"].format(lang))
    event.client.DB.set_key("AUTOTR_LANG", lang)
    await event.edit(client.getstrings(STRINGS)["setlang"].format(lang))

@client.Command(allowedits=False, checkCmd=True)
async def autotr(event):
    if not event.text: return
    autotr = event.client.DB.get_key("AUTOTR_MODE") or "OFF"
    if autotr == "ON":
        autolang = event.client.DB.get_key("AUTOTR_LANG") or "fa"
        try:
            translator = GoogleTranslator(source="auto", target=autolang)
            trjome = translator.translate(event.text)
            if trjome != event.text:
                await event.edit(trjome)
        except:
            pass