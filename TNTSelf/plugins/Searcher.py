from TNTSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Groups",
    "Name": "Search",
    "Info": {
        "Help": "To Search On Messages In The Chat!",
        "Commands": {
            "{CMD}SR<Type> <Text>": {
                "Help": "Search On Messages",
                "Input": {
                    "<Type>": "Message Type For Search",
                    "<Text>": "Text For Search",
                },
                "Vars": ["All", "Photo", "Video", "Gif", "Voice", "Music", "File", "Url"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "result": "**{STR} Search Result Messages For Text:** ( `{}` )\n{STR} **Filter:** ( `{}` )\n\n",
    "click": "Click Here!",
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
    async for message in event.client.iter_messages(event.chat_id, search=query, filter=addfilter, limit=40):
        link = "https://t.me/c/" + message.chat_id + "/" + message.id
        name = client.getstrings(STRINGS)["click"]
        text += f"**{count} -** [{name}]({link})\n"
        count += 1
    if count < 2:
        text = client.getstrings(STRINGS)["notres"].format((query or "---"), filter)
    await event.edit(text)