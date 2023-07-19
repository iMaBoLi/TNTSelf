from FidoSelf import client
from shazamio import Shazam
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Search Music",
    "Info": {
        "Help": "To Search Music By Query And Send Music!",
        "Commands": {
            "{CMD}SMusic <Text>": {
                "Help": "To Search Music",
                "Input": {
                    "<Text>": "Your Query To Search",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notres": "**{STR} The Music With Name** ( `{}` ) **Is Not Finded!**",
    "caption": "**{STR} Title:** ( `{}` )\n**{STR} Artist:** ( `{}` )\n**{STR} Size:** ( `{}` )",
}

@client.Command(command="SMusic (.*)")
async def searchmusic(event):
    await event.edit(client.STRINGS["wait"])
    query = event.pattern_match.group(1)
    result = await client.inline_query("@DeezerMusicBot", query)
    if not result.result.results:
        return await event.edit(client.getstrings(STRINGS)["notres"].format(query))
    result = result.result.results[0]
    size = client.functions.convert_bytes(result.document.size)
    caption = client.getstrings(STRINGS)["caption"].format(result.title, result.description, size)
    await client.send_file(event.chat_id, result.document, caption=caption)
    await event.delete()