from TNTSelf import client
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException

__INFO__ = {
    "Category": "Tools",
    "Name": "Translate",
    "Info": {
        "Help": "To Translate Your Texts!",
        "Commands": {
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
    "translate": "**{STR} Translated To** ( `{}` ):\n\n`{}`",
}

@client.Command(command="STr (.*)")
async def translattext(event):
    await event.edit(client.STRINGS["wait"])
    tolang = event.pattern_match.group(1).lower()
    if not event.reply_message or not event.reply_message.raw_text:
        return await event.edit(client.STRINGS["replytext"])
    text = event.reply_message.raw_text
    try:
        translator = GoogleTranslator(source="auto", target=tolang)
        trjome = translator.translate(text)
    except LanguageNotSupportedException:
        return await event.edit(client.getstrings(STRINGS)["notlang"].format(tolang))
    await event.edit(client.getstrings(STRINGS)["translate"].format(tolang, trjome))