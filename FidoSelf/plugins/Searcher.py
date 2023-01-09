from FidoSelf import client
from telethon import functions, types

@client.Cmd(pattern=f"(?i)^\{client.cmd}SR(All|Photo|Video|Gif|Voice|Music|File|Url) ?(.*)?$")
async def searcher(event):
    await event.edit(client.get_string("Wait"))
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
    infilter = client.get_string("FilterType")[filter]
    filter = filters[filter]
    text = client.get_string("Searcher_1").format((query or "---"), infilter)
    count = 1
    async for message in client.iter_messages(event.chat_id, search=query, filter=filter, limit=40):
        link = await client(functions.channels.ExportMessageLinkRequest(channel=event.chat_id, id=message.id, thread=True))
        name = client.get_string("Searcher_2")
        text += f"**{count} -** [{name}]({link.link})\n"
        count += 1
    if count < 2:
        text = client.get_string("Searcher_3").format((query or "---"), infilter)
    await event.edit(text)
