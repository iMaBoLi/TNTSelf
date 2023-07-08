from FidoSelf import client
from googletrans import Translator
import googletrans

__INFO__ = {
    "Category": "Tools",
    "Name": "Translate",
    "Info": {
        "Help": "To Translate Your Texts!",
        "Commands": {
            "{CMD}STr <Lang> <Reply(Text)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notlang": "**{STR} The Language** ( `{}` ) **Is Not Available!**",
    "translate": "**{STR} Translated From** ( `{}` ) **To** ( `{}` ):\n\n`{}`"
}

@client.Command(command="Str (.*)")
async def translator(event):
    await event.edit(client.STRINGS["wait"])
    if not (event.reply_message or event.reply_message.text):
        return await event.edit(client.STRINGS["replytext"])
    dest = event.pattern_match.group(1).lower()
    if dest not in googletrans.LANGUAGES:
        return await event.edit(client.getstrings(STRINGS)["notlang"].format(dest))
    translator = Translator()
    trjome = translator.translate(event.reply_message.text, dest=dest)
    await event.edit(client.getstrings(STRINGS)["translate"].format(trjome.src, dest.lower(), trjome.text))