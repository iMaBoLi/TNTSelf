from TNTSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Groups",
    "Name": "Global Search",
    "Info": {
        "Help": "To Search On Messages In All Chats!",
        "Commands": {
            "{CMD}SGAll <Text>": {
                "Help": "Search On All Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGPhoto <Text>": {
                "Help": "Search On Photo Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGVideo <Text>": {
                "Help": "Search On Video Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGGif <Text>": {
                "Help": "Search On Gif Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGMusic <Text>": {
                "Help": "Search On Music Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGVoice <Text>": {
                "Help": "Search On Voice Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGFile <Text>": {
                "Help": "Search On File Messages!",
                "Input": {
                    "<Text>": "Text For Search",
                },
            },
            "{CMD}SGUrl <Text>": {
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
    "result": "**{STR} Global Search Result Messages For Text:** ( `{}` )\n{STR} **Filter:** ( `{}` )\n\n",
    "click": "{STR} Click Here!",
    "notres": "**{STR} No Results Found For Text:** ( `{}` )\n**{STR} Filter:** ( `{}` )"
}

@client.Command(command="SG(All|Photo|Video|Gif|Voice|Music|File|Url) ?(.*)?")
async def globalsearcher(event):
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
    async for message in client.iter_messages(entity=None, search=query, filter=addfilter, limit=40):
        link = "https://t.me/c/" + message.chat_id + "/" + message.id
        name = client.getstrings(STRINGS)["click"]
        text += f"**{count} -** [{name}]({link})\n"
        count += 1
    if count < 2:
        text = client.getstrings(STRINGS)["notres"].format((query or "---"), filter)
    await event.edit(text)
    
