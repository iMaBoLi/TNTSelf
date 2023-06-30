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
    try:
        result = wikipedia.summary(query)
    except:
        return await event.edit(STRINGS["not"].format(query))
    if len(result) > 3900:
        result = result[:3900]
    text = STRINGS["info"].format(query, result)
    await event.edit(text=text)