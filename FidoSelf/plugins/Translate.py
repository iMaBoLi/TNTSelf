from FidoSelf import client
from googletrans import Translator

STRINGS = {
    "not": "**The Entered Language Is Not Available!**",
    "trans": "**Translated From** ( `{}` ) **To** ( `{}` ):\n\n`{}`",
}

@client.Command(command="Str (.*)")
async def translator(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["Text"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["Text"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    dest = event.pattern_match.group(1)
    try:
        translator = Translator()
        trjome = translator.translate(event.reply_message.text, dest=dest.lower())
    except ValueError:
        await event.edit(STRINGS["not"])
    await event.edit(STRINGS["trans"].format(trjome.src, dest.lower(), trjome.text))