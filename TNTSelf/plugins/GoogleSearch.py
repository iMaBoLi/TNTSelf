from TNTSelf import client
from googlesearch import search as GSearch

__INFO__ = {
    "Category": "Usage",
    "Name": "Google Search",
    "Info": {
        "Help": "To Search Your Text On Google!",
        "Commands": {
            "{CMD}SGoogle <Text>": {
                "Help": "Search On Google!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notsearch": "**{STR} The Google Search For** ( `{}` ) **Is Not Founded!**",
    "getsearch": "**{STR} Google Search For:** ( `{}` )\n\n",
}

@client.Command(command="SGoogle (.*)")
async def googlesearch(event):
    await event.edit(client.STRINGS["wait"])
    query = str(event.pattern_match.group(1))
    Gsearch = GSearch(query, advanced=True, num_results=20)
    if not Gsearch:
        return await event.edit(client.getstrings(STRINGS)["notsearch"].format(query))
    text = client.getstrings(STRINGS)["getsearch"].format(query)
    row = 1
    for result in Gsearch:
        title = f"[{result.title}]({result.url})"
        description = result.description[:200]
        text += f"**{row} -** {title}\n( `{description}` )\n\n"
        row += 1
    await event.edit(text)