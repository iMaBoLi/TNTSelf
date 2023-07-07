from FidoSelf import client
from googletrans import Translator
import googletrans

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
    "change": "**The Auto Translate Mode Has Been {}!**",
    "notlang": "**The Language** ( `{}` ) **Is Not Available!**",
    "setlang": "**The Auto Translate Language Was Set To** ( `{}` )",
}

@client.Command(command="AutoTr (On|Off)")
async def settrauto(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("AUTOTR_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="SetTrLang (.*)")
async def settrlang(event):
    await event.edit(client.STRINGS["wait"])
    lang = event.pattern_match.group(1).lower()
    if lang not in googletrans.LANGUAGES:
        return await event.edit(STRINGS["notlang"].format(lang))
    client.DB.set_key("AUTOTR_LANG", lang)
    await event.edit(STRINGS["setlang"].format(lang))

@client.Command(allowedits=False)
async def autotr(event):
    if event.checkCmd() or not event.text: return
    autotr = client.DB.get_key("AUTOTR_MODE") or "OFF"
    if autotr == "ON":
        autolang = client.DB.get_key("AUTOTR_LANG") or "fa"
        translator = Translator()
        trjome = translator.translate(event.text, dest=autolang.lower())
        if trjome.src != autolang and trjome.text != event.text:
            await event.edit(trjome.text)