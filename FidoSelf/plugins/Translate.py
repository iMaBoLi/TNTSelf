from FidoSelf import client
from googletrans import Translator
import googletrans

__INFO__ = {
    "Category": "Tools",
    "Name": "Translate",
    "Info": {
        "Help": "To Translate Your Texts!",
        "Commands": {
            "{CMD}STr <Lang>:<Text>": {
                "Help": "To Translate Text",
                "Input": {
                    "<Lang>": "Tranlate Language",
                    "<Lang>": "Tranlate Text",
                },
            },
            "{CMD}STr <Lang>": {
                "Help": "To Translate Text",
                "Input": {
                    "<Lang>": "Tranlate Language",
                },
                "Reply": ["Text"]
            },
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
    data = event.pattern_match.group(1)
    dest = data.split(":")[0].lower()
    text = data.split(":")[1] if len(data) > 1 else None
    if not text:
        if not (event.reply_message or event.reply_message.text):
            return await event.edit(client.STRINGS["replytext"])
        text = event.reply_message.text
    if dest not in googletrans.LANGUAGES:
        return await event.edit(client.getstrings(STRINGS)["notlang"].format(dest))
    translator = Translator()
    trjome = translator.translate(text, dest=dest)
    await event.edit(client.getstrings(STRINGS)["translate"].format(trjome.src, dest.lower(), trjome.text))