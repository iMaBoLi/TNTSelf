from FidoSelf import client
from googletrans import Translator
import googletrans

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Translate",
    "Pluginfo": {
        "Help": "To Translate Your Texts!",
        "Commands": {
            "{CMD}STr <Lang> <Reply(Text)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notlang": "**The Language** ( `{}` ) **Is Not Available!**",
    "translate": "**Translated From** ( `{}` ) **To** ( `{}` ):\n\n`{}`",
}

@client.Command(command="Str (.*)")
async def translator(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or not event.reply_message.text:
        medias = client.STRINGS["replyMedia"]
        media = medias["Text"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    dest = event.pattern_match.group(1).lower()
    if dest not in googletrans.LANGUAGES:
        return await event.edit(STRINGS["notlang"].format(dest))
    translator = Translator()
    trjome = translator.translate(event.reply_message.text, dest=dest)
    await event.edit(STRINGS["translate"].format(trjome.src, dest.lower(), trjome.text))