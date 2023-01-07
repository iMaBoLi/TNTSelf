from FidoSelf import client
from telethon import functions, types

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(All|Photo|Video|Gif|Doc|Music|Voice|Url) ?(.*)?$")
async def searcher(event):
    await event.edit(client.get_string("Wait"))
    query = str(event.pattern_match.group(2) or "")
    filters = {
        "All": None,
        "Photo": types.InputMessagesFilterPhotos,
        "Video": types.InputMessagesFilterVideo,
        "Gif": types.InputMessagesFilterGif,
        "Voice": types.InputMessagesFilterDocument,
        "Music": types.InputMessagesFilterMusic,
        "Voice": types.InputMessagesFilterVoice,
        "Url": types.InputMessagesFilterUrl,
    }
    filter = event.pattern_match.group(1).title()
    filter = filters[filter]
    text = client.get_string("Searcher_1").format((query or "---"))
    async for message in client.iter_messages(event.chat_id, search=query, filter=filter, limit=50):
        link = await client(functions.channels.ExportMessageLinkRequest(channel=event.chat_id, id=message.id, thread=True))
        text += client.get_string("Searcher_2").format(link.link)
    await event.edit(text)
