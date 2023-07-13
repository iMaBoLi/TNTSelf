from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Groups",
    "Name": "Search",
    "Info": {
        "Help": "To Search On Messages In The Chat!",
        "Commands": {
            "{CMD}SRAll <Text>": {
                "Help": "Search On All Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRPhoto <Text>": {
                "Help": "Search On Photo Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRVideo <Text>": {
                "Help": "Search On Video Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRGif <Text>": {
                "Help": "Search On Gif Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRMusic <Text>": {
                "Help": "Search On Music Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRVoice <Text>": {
                "Help": "Search On Voice Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRFile <Text>": {
                "Help": "Search On File Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SRUrl <Text>": {
                "Help": "Search On Url Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "result": "**{STR} Search Result Messages For Text:** ( `{}` )\n{STR} **Filter:** ( `{}` )\n\n",
    "click": "**{STR} Click Here!",
    "notres": "**{STR} No Results Found For Text:** ( `{}` )\n**{STR} Filter:** ( `{}` )"
}

@client.Command(command="SR(All|Photo|Video|Gif|Voice|Music|File|Url) ?(.*)?")
async def searcher(event):
    await event.edit(client.STRINGS["wait"])
    query = str(event.pattern_match.group(2) or "")
    filters = {
        "All": None,
        "Photo": types.InputMessagesFilterPhotos,
        "Video": types.InputMessagesFilterVideo,
        "Gif": types.InputMessagesFilterGif,
        "Voice": types.InputMessagesFilterVoice,
        "Music": types.InputMessagesFilterMusic,
        "File": types.InputMessagesFilterDocument,
        "Url": types.InputMessagesFilterUrl,
    }
    filter = event.pattern_match.group(1).title()
    addfilter = filters[filter]
    text = client.getstrings(STRINGS)["result"].format((query or "---"), filter)
    count = 1
    async for message in client.iter_messages(event.chat_id, search=query, filter=addfilter, limit=40):
        link = await client(functions.channels.ExportMessageLinkRequest(channel=message.chat_id, id=message.id, thread=True))
        name = client.getstrings(STRINGS)["click"]
        text += f"**{count} -** [{name}]({link.link})\n"
        count += 1
    if count < 2:
        text = client.getstrings(STRINGS)["notres"].format((query or "---"), filter)
    await event.edit(text)