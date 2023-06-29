from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Group",
    "Plugname": "Searcher",
    "Pluginfo": {
        "Help": "To Search On Messages In The Chat!",
        "Commands": {
            "{CMD}SRAll <Text>": "Search On All Messages!",
            "{CMD}SRPhoto <Text>": "Search On Photo Messages!",
            "{CMD}SRVideo <Text>": "Search On Video Messages!",
            "{CMD}SRGif <Text>": "Search On Gif Messages!",
            "{CMD}SRVoice <Text>": "Search On Voice Messages!",
            "{CMD}SRMusic <Text>": "Search On Music Messages!",
            "{CMD}SRFile <Text>": "Search On File Messages!",
            "{CMD}SRUrl <Text>": "Search On Url Messages!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "result": "**Search Result Messages For Text:** ( `{}` )\n**Filter:** ( `{}` )\n\n",
    "click": "Click Here!",
    "not": "**No Results Found For Text:** ( `{}` )\n**Filter:** ( `{}` )",
}

@client.Command(command="SR(All|Photo|Video|Gif|Voice|Music|File|Url) (.*)")
async def searcher(event):
    await event.edit(client.STRINGS["wait"])
    query = str(event.pattern_match.group(2))
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
    text = STRINGS["result"].format((query or "---"), filter)
    count = 1
    async for message in client.iter_messages(event.chat_id, search=query, filter=addfilter, limit=40):
        link = await client(functions.channels.ExportMessageLinkRequest(channel=message.chat_id, id=message.id, thread=True))
        name = STRINGS["click"]
        text += f"**{count} -** [{name}]({link.link})\n"
        count += 1
    if count < 2:
        text = STRINGS["not"].format((query or "---"), filter)
    await event.edit(text)