from FidoSelf import client
import wikipedia

__INFO__ = {
    "Category": "Funs",
    "Name": "Wikipedia",
    "Info": {
        "Help": "To Search A Note On Wikipedia!",
        "Commands": {
            "{CMD}SWiki <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**The Wikipedia For** ( `{}` ) **Is Not Finded!**",
    "info": "**Query:** ( `{}` )\n\n**Title:** ( `{}` )\n\n`{}`",
}

@client.Command(command="SWiki (.*)")
async def wikisearch(event):
    await event.edit(client.getstrings()["wait"])
    query = event.pattern_match.group(1)
    search = wikipedia.search(query)[0]
    if not result:
        return await event.edit(client.getstrings(STRINGS)["not"].format(query))
    result = wikipedia.summary(search)
    if len(result) > 3900:
        result = result[:3900]
    text = client.getstrings(STRINGS)["info"].format(query, search, result)
    await event.edit(text=text)