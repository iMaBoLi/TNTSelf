from FidoSelf import client
import asyncio

__INFO__ = {
    "Category": "Funs",
    "Plugname": "Text Say",
    "Pluginfo": {
        "Help": "To Say Your Message Texts!",
        "Commands": {
            "{CMD}TSay <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="TSay ([\S\s]*)")
async def tsay(event):
    OText = event.pattern_match.group(1)
    Text = ""
    for Part in OText:
        Text += Part
        await event.edit(Text)
        await asyncio.sleep(0.5)
        await event.edit(Text + "|")
        await asyncio.sleep(0.5)
        await event.edit(Text)
        await asyncio.sleep(0.2)
        await event.edit(Text + "|")
        await asyncio.sleep(0.2)
    await event.edit(Text)