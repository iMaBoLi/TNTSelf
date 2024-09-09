from FidoSelf import client
import wikipedia

__INFO__ = {
    "Category": "Funs",
    "Name": "Wikipedia",
    "Info": {
        "Help": "To Search A Note On Wikipedia!",
        "Commands": {
            "{CMD}SWiki <Text>": {
                "Help": "To Search On Wikipedia",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**{STR} The Wikipedia For** ( `{}` ) **Is Not Finded!**",
    "info": "**{STR} Query:** ( `{}` )\n\n**{STR} Title:** ( `{}` )\n\n`{}`"
}

@client.Command(command="SWiki (.*)")
async def wikisearch(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    search = wikipedia.search(query)[0]
    result = wikipedia.summary(search)
    if not result:
        return await event.edit(client.getstrings(STRINGS)["not"].format(query))
    if len(result) > 3800:
        result = result[:3800] + "  ....."
    text = client.getstrings(STRINGS)["info"].format(query, search, result)
    await event.edit(text=text)