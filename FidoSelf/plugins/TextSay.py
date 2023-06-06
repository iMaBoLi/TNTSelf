from FidoSelf import client
import asyncio

@client.Command(command="TSay ([\S\s]*)")
async def tsay(event):
    text = event.pattern_match.group(1)
    new = ""
    for par in text:
        new += par
        await event.edit(new)
        await asyncio.sleep(0.2)
        await event.edit(new + "|")
        await asyncio.sleep(0.2)
        await event.edit(new)
        await asyncio.sleep(0.2)
        await event.edit(new + "|")
        await asyncio.sleep(0.2)