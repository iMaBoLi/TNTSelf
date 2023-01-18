from FidoSelf import client
from googletrans import Translator

@client.Command(pattern=f"(?i)^\{client.cmd}Str (.*)$")
async def translator(event):
    await event.edit(client.get_string("Wait"))
    if not event.reply_message or not event.reply_message.text:
        return await event.edit(client.get_string("Reply_T"))
    dest = event.text.split()[1]
    try:
        translator = Translator()
        trjome = translator.translate(event.reply_message.text, dest=dest.lower())
    except ValueError:
        await event.edit(client.get_string("Translate_1"))
    await event.edit(client.get_string("Translate_2").format(trjome.src, dest.lower(), trjome.text))
