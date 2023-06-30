from FidoSelf import client
import wikipedia

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Wikipedia",
    "Pluginfo": {
        "Help": "To Search A Note On Wikipedia!",
        "Commands": {
            "{CMD}SWiki <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**The Wikipedia For** ( `{}` ) **Is Not Finded!**",
    "info": "**Title:** ( `{}` )\n\n`{}`",
}

@client.Command(command="SWiki (.*)")
async def wikisearch(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    result = wikipedia.summary(query)
    if not result:
        return await event.edit(STRINGS["not"])
    if len(result) > 3000:
        result = result[:3000]
    text = STRINGS["info"].format(query, result)
    await event.edit(text=text)