from self import client
from googletrans import Translator

@client.Cmd(pattern=f"(?i)^\{client.cmd}Str (.*)$")
async def translator(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.reply_message or not event.reply_message.text:
        return await event.edit(f"**{client.str} Please Reply To Message For Translate!**")
    dest = event.text.split()[1]
    try:
        translator = Translator()
        trjome = translator.translate(event.reply_message.text, dest=dest.lower())
    except ValueError:
        await event.edit(f"**{client.str} The Input Language Is Not Available!**")
    await event.edit(f"**{client.str} Translated From** ( `{trjome.src}` ) **To** ( `{dest.lower()}` ):\n\n`{trjome.text}`")
