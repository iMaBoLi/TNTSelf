from FidoSelf import client
import asyncio

__INFO__ = {
    "Category": "Funs",
    "Plugname": "Text Say",
    "Pluginfo": {
        "Help": "To Say Your Message Texts!",
        "Commands": {
            "{CMD}TSay <Text>": None,
            "{CMD}TSay <Reply(Text)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**Please Reply To Text Or Enter Text!**",
}

@client.Command(command="TSay ?([\S\s]*)?")
async def tsay(event):
    inputtext = str(event.pattern_match.group(1) or "")
    if not inputtext or not event.reply_message and not event.reply_message.text:
        return await event.edit(STRINGS["not"])
    OText = inputtext if inputtext else event.reply_message.text
    Text = ""
    for Part in OText:
        Text += Part
        await event.edit(Text)
        await asyncio.sleep(0.5)