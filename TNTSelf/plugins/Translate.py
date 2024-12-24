from TNTSelf import client
from deep_translator import GoogleTranslator
import os

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
            "{CMD}TRLangs": {
                "Help": "To Get Languages",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notlang": "**{STR} The Language** ( `{}` ) **Is Not Available!**",
    "translate": "**{STR} Translated To** ( `{}` ):\n\n`{}`",
    "trfile": "**{STR} The Translator Languages!**",
}

@client.Command(command="STr (.*)")
async def translattext(event):
    await event.edit(client.STRINGS["wait"])
    tolang = event.pattern_match.group(1).lower()
    if not event.reply_message or not event.reply_message.raw_text:
        return await event.edit(client.STRINGS["replytext"])
    if tolang not in client.functions.TRLANGS:
        return await event.edit(client.getstrings(STRINGS)["notlang"].format(tolang))
    text = event.reply_message.raw_text
    translator = GoogleTranslator(source="auto", target=tolang)
    trjome = translator.translate(text)
    await event.edit(client.getstrings(STRINGS)["translate"].format(tolang, trjome))
    
@client.Command(command="TRLangs")
async def translang(event):
    await event.edit(client.STRINGS["wait"])
    data = ""
    for lang in client.functions.TRLANGS:
        data += f"{client.functions.TRLANGS[lang].title()} -> {lang}\n"
    trfile = event.client.PATH + "TRLangs.txt"
    open(trfile, "w").write(data)
    caption = client.getstrings(STRINGS)["trfile"]
    await event.client.send_file(event.chat_id, trfile, caption=caption)
    os.remove(trfile)
    await event.delete()